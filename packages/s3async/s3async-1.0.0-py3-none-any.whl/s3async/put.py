"""Put operations"""

from pathlib import Path
from typing import Any, Optional, Dict, List, Union, cast
import asyncio
import json
import aiofiles
from botocore.exceptions import ClientError  # type: ignore
from aiobotocore.client import AioBaseClient  # type: ignore
from s3async.log import LOGGER
from s3async.model import ObjectMetadata
from s3async.tag import put_tag_async
from s3async.utils import (
    join_path,
    compute_hash,
    parse_s3_path,
    get_client,
    provide_aioclient,
)


def put_object_batch(
    input_paths: List[Path],
    s3_path: Union[str, List[str]],
    set_hash: bool = False,
    metadata: Optional[ObjectMetadata] = None,
) -> List[str]:
    """Put batch of objects to S3 asynchronously"""

    @provide_aioclient
    async def _put_object_batch(
        input_paths: List[Path],
        target_paths: List[str],
        client: Optional[AioBaseClient] = None,
        metadata: Optional[ObjectMetadata] = None,
    ) -> List[str]:
        if client is None:
            raise ValueError("Client not set")
        tasks = []
        invalid_paths = list(filter(lambda x: x is None or not x.is_file(), input_paths))
        if len(invalid_paths) > 0:
            LOGGER.error("Invalid input path in %s", invalid_paths)
            raise ValueError("Received invalid input path")
        tasks = [
            put_object_async(path, target_paths[i], client, set_hash=set_hash, metadata=metadata)
            for i, path in enumerate(input_paths)
        ]
        responses = await asyncio.gather(*tasks)
        return cast(List[str], responses)

    if isinstance(s3_path, str):
        s3_paths = [join_path(s3_path, path.name) for path in input_paths]
    else:
        s3_paths = s3_path
    if len(input_paths) != len(s3_paths):
        raise ValueError("Output path must be a single S3 prefix or a list of prefixes matching the input path length")

    result: List[str] = asyncio.run(_put_object_batch(input_paths, s3_paths, metadata=metadata))
    return result


def put_json(data: Dict[str, Any], s3_path: str) -> str:
    """Write JSON data to S3"""
    client = get_client()
    bucket, key = parse_s3_path(s3_path)
    client.put_object(Bucket=bucket, Key=key, Body=json.dumps(data).encode("utf"))
    return s3_path


def put_object(in_path: Path, s3_path: str) -> str:
    """Write file data to S3"""
    client = get_client()
    bucket, key = parse_s3_path(s3_path)
    with open(in_path, "rb") as in_file:
        data = in_file.read()
        client.put_object(Bucket=bucket, Key=key, Body=data)
    return s3_path


@provide_aioclient
async def s3_to_s3_async(  # noqa: PLR0913
    src_path: str,
    dst_path: str,
    client: Optional[AioBaseClient] = None,
    dst_client: Optional[AioBaseClient] = None,
    set_hash: bool = False,
    version: Optional[str] = None,
    metadata: Optional[ObjectMetadata] = None,
) -> Optional[str]:
    """Async S3 to S3 file object upload"""
    if client is None:
        raise ValueError("Client not set")
    if dst_client is None:
        dst_client = client
    src_bucket, src_key = parse_s3_path(src_path)
    dst_bucket, dst_key = parse_s3_path(dst_path)
    LOGGER.debug("Copying data from %s to %s", src_path, dst_path)
    try:
        extra: Dict[str, Any] = {}
        if version:
            extra = {**extra, "VersionId": version}
        response = await client.get_object(Bucket=src_bucket, Key=src_key, **extra)
        body = await response["Body"].read()
        meta = metadata.as_dict() if metadata else {}
        await dst_client.put_object(Body=body, Bucket=dst_bucket, Key=dst_key, **meta)
        if set_hash:
            hashval = compute_hash(body)
            await put_tag_async(src_path, "hash", hashval)
            await put_tag_async(dst_path, "hash", hashval)
    except ClientError as err:
        err_resp: Dict[str, Any] = err.response
        err_code = err_resp.get("Error", {}).get("Code")
        if err_code in ("404", "NoSuchKey"):
            return None
        LOGGER.error(err)
        raise err
    return dst_path


@provide_aioclient
async def put_object_async(
    src_path: Path,
    dst_path: str,
    client: Optional[AioBaseClient] = None,
    set_hash: bool = False,
    metadata: Optional[ObjectMetadata] = None,
) -> Optional[str]:
    """Async local to S3 file object upload"""
    if client is None:
        raise ValueError("Client not set")
    bucket, key = parse_s3_path(dst_path)
    LOGGER.debug("Copying data from %s to %s", src_path, dst_path)
    try:
        async with aiofiles.open(Path(src_path), "rb") as in_file:
            data = await in_file.read()
            meta = metadata.as_dict() if metadata else {}
            await client.put_object(Body=data, Bucket=bucket, Key=key, **meta)
            if set_hash:
                hashval = compute_hash(data)
                await put_tag_async(dst_path, "hash", hashval, client)
    except ClientError as err:
        err_resp: Dict[str, Any] = err.response
        err_code = err_resp.get("Error", {}).get("Code")
        if err_code in ("404", "NoSuchKey"):
            return None
        LOGGER.error(err)
        raise err
    return dst_path
