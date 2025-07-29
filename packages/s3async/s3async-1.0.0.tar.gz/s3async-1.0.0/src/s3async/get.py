"""Basic file / object IO operations"""

from typing import Any, Dict, List, Optional, Union, cast
import os
from pathlib import Path
import shutil
import asyncio
import json
from tempfile import TemporaryDirectory
import aiofiles
from botocore.exceptions import ClientError  # type: ignore
from aiobotocore.client import AioBaseClient  # type: ignore
from s3async.log import LOGGER
from s3async.utils import (
    parse_s3_path,
    get_client,
    provide_aioclient,
)


# pylint: disable=R0914


@provide_aioclient
async def get_object_async(
    src_path: str, dst_path: Path, version: Optional[str] = None, client: Optional[AioBaseClient] = None
) -> Optional[Path]:
    """Async S3 file object download"""
    if client is None:
        raise ValueError("Client not set")
    bucket, key = parse_s3_path(src_path)
    try:
        extra: Dict[str, Any] = {}
        if version:
            extra = {**extra, "VersionId": version}
        res = await client.get_object(Bucket=bucket, Key=key, **extra)
        LOGGER.debug("Copying data from %s to %s", src_path, dst_path)
        dst_path.parent.mkdir(exist_ok=True, parents=True)
        async with aiofiles.open(Path(dst_path), "wb") as out_file:
            data = await res["Body"].read()
            await out_file.write(data)
    except ClientError as err:
        err_resp: Dict[str, Any] = err.response
        err_code = err_resp.get("Error", {}).get("Code")
        if err_code in ("404", "NoSuchKey"):
            return None
        LOGGER.error(err)
        raise err
    return dst_path


def get_object_batch(
    s3_paths: List[str], out_path: Union[Path, List[Path]], versions: Optional[List[str]] = None
) -> List[Path]:
    """Get batch of objects from S3 asynchronously."""

    @provide_aioclient
    async def _get_object_batch(
        s3_paths: List[str],
        output_paths: List[Path],
        versions: Optional[List[str]] = None,
        client: Optional[AioBaseClient] = None,
    ) -> List[Path]:  # pylint: disable=R0914
        if client is None:
            raise ValueError("Client not set")
        results = []
        tasks = []
        for i, path in enumerate(s3_paths):
            version = versions[i] if versions else None
            target_path = output_paths[i]
            tasks.append(get_object_async(path, target_path, version=version, client=client))
        results = await asyncio.gather(*tasks)
        return results

    if isinstance(out_path, Path):
        if Path(out_path).is_file():
            raise ValueError("Single output path must not be a file")
        out_paths = [Path(out_path, os.path.basename(path)) for path in s3_paths]
        Path(out_path).mkdir(parents=True, exist_ok=True)
    else:
        out_paths = out_path
        for path in out_paths:
            path.parent.mkdir(parents=True, exist_ok=True)
    if len(out_paths) != len(s3_paths):
        raise ValueError("Output path must be a single path or a list of paths matching the input path length")

    result: List[Path] = asyncio.run(_get_object_batch(s3_paths, out_paths, versions=versions))
    return result


def get_json(s3_path: str) -> Dict[str, Any]:
    """Get JSON from S3 object"""
    bucket, key = parse_s3_path(s3_path)
    client = get_client()
    with TemporaryDirectory() as tmpdir:
        out_file = Path(tmpdir, Path(key).name)
        client.download_file(Bucket=bucket, Key=key, Filename=str(out_file))
        return cast(Dict[str, Any], json.loads(out_file.read_text(encoding="utf8")))


def get_object(s3_path: str, out_path: Path) -> Path:
    """Download object into a specific local path"""
    bucket, key = parse_s3_path(s3_path)
    client = get_client()
    with TemporaryDirectory() as tmpdir:
        out_file = Path(tmpdir, Path(key).name)
        client.download_file(Bucket=bucket, Key=key, Filename=str(out_file))
        shutil.copyfile(out_file, out_path)
        return Path(out_path)
