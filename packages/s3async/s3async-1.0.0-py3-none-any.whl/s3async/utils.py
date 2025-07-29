"""Utilities"""

import asyncio
from datetime import datetime, timezone
import os
from typing import Optional, Any, Tuple, TypeVar, Union
from pathlib import Path
import hashlib
import re
from urllib.parse import urlparse

import functools
import aiofiles
import boto3  # type: ignore
import aiobotocore  # type: ignore
from aiobotocore.session import AioSession  # type: ignore
from aiobotocore.client import AioBaseClient  # type: ignore

from s3async.log import LOGGER


# pylint: disable=W0603

_CLIENT: Optional[Any] = None
VALID_SYNC_METHODS = ["hash", "etag", "timestamp"]

T = TypeVar("T")


def provide_aioclient(func: T) -> T:
    """Creates aiobotocore client for wrapped functions if it is not provided in input arguments already.
    Use AWS_PROFILE env-variable to override the default profile
    Use AWS_ENDPOINT env-variable to override the default AWS endpoint url (e.g. for testing purposes)
    """

    @functools.wraps(func)  # type: ignore
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        clientargs = list(filter(lambda x: isinstance(x, AioBaseClient), args))
        if len(clientargs) > 0 or ("client" in kwargs and kwargs["client"] is not None):
            return await func(*args, **kwargs)  # type: ignore
        endpoint = os.getenv("AWS_ENDPOINT")
        async with get_aioclient(endpoint=endpoint) as client:
            kwargs["client"] = client
            return await func(*args, **kwargs)  # type: ignore

    return wrapper  # type: ignore


def get_aioclient(profile: Optional[str] = None, endpoint: Optional[str] = None) -> AioBaseClient:
    """Creates a new aiobotocore client creator context."""
    session = _get_aiosession(profile)
    cfg = aiobotocore.config.AioConfig(max_pool_connections=10)
    return session.create_client("s3", config=cfg, endpoint_url=endpoint)


def get_client() -> Any:
    """Get s3 client. Use AWS_ENDPOINT env-variable to override
    the default AWS endpoint url (e.g. for testing purposes)"""
    global _CLIENT  # noqa: PLW0603
    if _CLIENT is None:
        LOGGER.debug("Created S3 client")
        endpoint = os.getenv("AWS_ENDPOINT")
        _CLIENT = boto3.client("s3", endpoint_url=endpoint)
    return _CLIENT


def _get_aiosession(profile: Optional[str] = None) -> AioSession:
    """Get aiobotocore session"""
    return aiobotocore.session.AioSession(profile=profile)


def compute_file_hash(in_path: Path) -> str:
    """Compute SHA256 hash of a file"""
    return asyncio.run(compute_file_hash_async(in_path))


async def compute_file_hash_async(in_path: Path, semaphore: Optional[asyncio.Semaphore] = None) -> str:
    """Compute SHA256 hash of a file"""
    hashval = hashlib.md5()  # nosec
    if semaphore is None:
        semaphore = asyncio.Semaphore(100)
    async with semaphore:
        async with aiofiles.open(Path(in_path), "rb") as in_file:
            # Read and update hash string value in blocks of 32K
            while byte_block := await in_file.read(32767):
                if byte_block == b"":
                    break
                hashval.update(byte_block)
            return hashval.hexdigest()


def compute_hash(data: bytes) -> str:
    """Compute SHA256 hash of a file"""
    hashval = hashlib.md5(data)  # nosec
    return hashval.hexdigest()


def parse_s3_path(path: str) -> Tuple[str, str]:
    """Parse S3 path into tuple of bucket and key"""
    if not is_s3_path(path):
        raise ValueError("Invalid S3 path")
    parsed = urlparse(str(path), allow_fragments=False)
    return parsed.netloc, parsed.path.lstrip("/")


def is_s3_path(path: Union[Path, str]) -> bool:
    """Parse S3 path into tuple of bucket and key"""
    parsed = urlparse(str(path), allow_fragments=False)
    return parsed.scheme == "s3"


def join_path(*paths: Union[Path, str], ensure_protocol: bool = True) -> str:
    """Join s3 path parts"""
    # Random string that we can use as escape sequence for leading slashes with relative safety
    escape_sequence = "©@aª«5"

    def _escape_leading_slash(path: Union[str, Path]) -> Union[str, Path]:
        orig_is_path = isinstance(path, Path)
        path = str(path)
        if path.startswith("/"):
            path = escape_sequence + path[1:]
        return Path(path) if orig_is_path else path

    # Escape leading slashes to work around os.path.join limitations
    escaped = list(map(_escape_leading_slash, paths))
    result = os.path.join(*escaped)
    if ensure_protocol:
        if not result.startswith("s3://"):
            result = os.path.join("s3://", result)
    unescaped = result.replace(escape_sequence, "/")

    return unescaped


def regex_match(regexp: str, string: str, group: Optional[int] = None) -> str:
    """Regular expression match that returns the specified subexpression group or whole match if group == 0.
    If group is not specified, returns the first matching subexpression from regexp search
    or if no subexpressions are defined, the whole matching string.
    """
    m = re.search(regexp, string)
    if m:
        if group is None:
            if len(m.groups()) > 0:
                return m.group(1)
            return m.group(0)
        return m.group(group)
    return ""


def snake_to_pascal_case(val: str) -> str:
    """Convert snake_case string to PascalCase string"""
    return "".join(x.capitalize() for x in val.lower().split("_"))


def parse_datetime(val: Union[datetime, str]) -> datetime:
    """Parse isoformatted timestamp"""
    if isinstance(val, datetime):
        return val
    if isinstance(val, str):
        if val.endswith("Z"):
            return datetime.fromisoformat(val.replace("Z", "")).replace(tzinfo=timezone.utc)
        else:
            return datetime.fromisoformat(val)
    raise ValueError("invalid datetime")
