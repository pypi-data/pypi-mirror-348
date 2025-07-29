"""Delete operations"""

from copy import deepcopy
from functools import reduce
from typing import Any, Dict, List, Optional, Tuple
import asyncio
from botocore.exceptions import ClientError  # type: ignore
from aiobotocore.client import AioBaseClient  # type: ignore
from s3async.list import list_versions_async
from s3async.log import LOGGER
from s3async.utils import (
    parse_s3_path,
    get_client,
    provide_aioclient,
)


def delete_object_batch(s3_paths: List[str]) -> List[str]:
    """Delete batch of S3 objects"""

    def _deletes_by_bucket(results: Dict[str, List[Dict[str, str]]], s3_path: str) -> Dict[str, List[Dict[str, str]]]:
        bucket, key = parse_s3_path(s3_path)
        if bucket not in results:
            results[bucket] = [{"Key": key}]
        else:
            results[bucket].append({"Key": key})
        return results

    deletes_by_bucket: Dict[str, List[Dict[str, str]]] = reduce(_deletes_by_bucket, s3_paths, {})

    client = get_client()
    for bucket, deletes in deletes_by_bucket.items():
        while len(deletes) > 0:
            del_batch = deletes[:1000]
            deletes = deletes[1000:]  # noqa: PLW2901
            client.delete_objects(Bucket=bucket, Delete={"Objects": del_batch})
    return s3_paths


def list_and_delete_object_versions(
    s3_path: str, regex_filter: Optional[str] = None, recursive: bool = True
) -> List[Tuple[str, str]]:
    """List object versions and delete them iteratively using async generator"""

    @provide_aioclient
    async def _list_and_delete_object_versions(
        client: Optional[AioBaseClient] = None,
    ) -> List[Tuple[List[str], List[str]]]:
        reqs = []
        batch_size = 50
        batch_key: List[str] = []
        batch_ver: List[str] = []
        async for key, ver, _, _ in list_versions_async(s3_path, regex_filter, recursive, client=client):
            if len(batch_key) > batch_size:
                reqs.append(
                    asyncio.create_task(delete_object_versions_async(deepcopy(batch_key), deepcopy(batch_ver), client))
                )
                batch_key = []
                batch_ver = []
            batch_key.append(key)
            batch_ver.append(ver)
        if len(batch_key) > 0:
            reqs.append(asyncio.create_task(delete_object_versions_async(batch_key, batch_ver, client)))
        results = await asyncio.gather(*reqs)
        return results

    results = asyncio.run(_list_and_delete_object_versions())
    flattened = [item for sublist in [list(zip(*batch)) for batch in results] for item in sublist]
    return flattened


@provide_aioclient
async def delete_object_versions_async(
    paths: List[str], versions: List[str], client: Optional[AioBaseClient] = None
) -> Tuple[List[str], List[str]]:
    """Delete multiple object versions, async function"""
    if client is None:
        raise ValueError("Client not set")

    def _deletes_by_bucket(
        results: Dict[str, List[Dict[str, str]]], path_version: Tuple[str, str]
    ) -> Dict[str, List[Dict[str, str]]]:
        s3_path, version = path_version
        bucket, key = parse_s3_path(s3_path)
        if bucket not in results:
            results[bucket] = [{"Key": key, "VersionId": version}]
        else:
            results[bucket].append({"Key": key, "VersionId": version})
        return results

    paths_versions = list(zip(paths, versions))
    deletes_by_bucket: Dict[str, List[Dict[str, str]]] = reduce(_deletes_by_bucket, paths_versions, {})

    for bucket, deletes in deletes_by_bucket.items():
        await client.delete_objects(Bucket=bucket, Delete={"Objects": deletes})
    return paths, versions


def delete_object_versions(s3_paths: List[str], versions: List[str]) -> List[str]:
    """Delete multiple S3 object versions"""

    def _deletes_by_bucket(
        results: Dict[str, List[Dict[str, str]]], path_version: Tuple[str, str]
    ) -> Dict[str, List[Dict[str, str]]]:
        s3_path, version = path_version
        bucket, key = parse_s3_path(s3_path)
        if bucket not in results:
            results[bucket] = [{"Key": key, "VersionId": version}]
        else:
            results[bucket].append({"Key": key, "VersionId": version})
        return results

    paths_versions = list(zip(s3_paths, versions))
    deletes_by_bucket: Dict[str, List[Dict[str, str]]] = reduce(_deletes_by_bucket, paths_versions, {})

    client = get_client()
    for bucket, deletes in deletes_by_bucket.items():
        client.delete_objects(Bucket=bucket, Delete={"Objects": deletes})
    return s3_paths


@provide_aioclient
async def delete_object_async(
    s3_path: str, version: Optional[str] = None, client: Optional[AioBaseClient] = None
) -> bool:
    """Async S3 file object delete"""
    if client is None:
        raise ValueError("Client not set")
    bucket, key = parse_s3_path(s3_path)
    try:
        extra: Dict[str, Any] = {}
        if version:
            extra = {**extra, "VersionId": version}
        await client.delete_object(Bucket=bucket, Key=key, **extra)
        LOGGER.debug("Deleting key %s", s3_path)
    except ClientError as err:
        err_resp: Dict[str, Any] = err.response
        err_code = err_resp.get("Error", {}).get("Code")
        if err_code in ("404", "NoSuchKey"):
            return False
        LOGGER.error(err)
        raise err
    return True
