"""Copy abstraction"""

from typing import Optional, Tuple, Union
from pathlib import Path
import asyncio
from s3async.get import get_object_async
from s3async.log import LOGGER
from s3async.model import ObjectMetadata, OptionalPathLike
from s3async.put import put_object_async, s3_to_s3_async
from s3async.utils import is_s3_path


def cp(
    src_path: Union[Path, str],
    dst_path: Union[Path, str],
    version: Optional[str] = None,
    metadata: Optional[ObjectMetadata] = None,
) -> Tuple[Union[Path, str], OptionalPathLike]:
    """Copy from source path to destination path. One or both of the paths needs to be S3 path."""

    if is_s3_path(src_path) and is_s3_path(dst_path):
        LOGGER.debug("S3 to S3 cp from %s to %s", src_path, dst_path)
        return "PUT", asyncio.run(s3_to_s3_async(str(src_path), str(dst_path), metadata=metadata))
    if is_s3_path(src_path) and not is_s3_path(dst_path):
        LOGGER.debug("S3 to local cp from %s to %s", src_path, dst_path)
        return "GET", asyncio.run(get_object_async(str(src_path), Path(dst_path), version=version))
    if not is_s3_path(src_path) and is_s3_path(dst_path):
        LOGGER.debug("Local to S3 cp from %s to %s", src_path, dst_path)
        return "PUT", asyncio.run(put_object_async(Path(src_path), str(dst_path), metadata=metadata))
    raise ValueError("At least one of the inputs needs to be valid S3 path")
