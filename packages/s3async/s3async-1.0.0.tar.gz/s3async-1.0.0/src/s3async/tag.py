"""Metadata & tagging related functionalities"""

from typing import Any, Dict, Optional
import asyncio
import datetime
from botocore.exceptions import ClientError  # type: ignore
from aiobotocore.client import AioBaseClient  # type: ignore
from s3async.log import LOGGER
from s3async.utils import parse_s3_path, provide_aioclient


@provide_aioclient
async def get_tags_async(s3_path: str, client: Optional[AioBaseClient] = None) -> Optional[Dict[str, Any]]:
    """Get s3 object tag asynchronously"""
    if client is None:
        raise ValueError("Client not set")
    bucket, key = parse_s3_path(s3_path)
    try:
        resp = await client.get_object_tagging(Bucket=bucket, Key=key)
        tags = resp.get("TagSet", [])
        return {tag["Key"]: str(tag["Value"]) for tag in tags}
    except ClientError as err:
        err_resp: Dict[str, Any] = err.response
        err_code = err_resp.get("Error", {}).get("Code")
        # We expect to get MethodNotAllowed error for versioned S3 bucket Delete Markers, i.e. deleted file.
        # Suppress warning
        if err_code == "MethodNotAllowed":
            return None
        # Suppress warning if key does not exist
        if err_code in ("404", "NoSuchKey"):
            return None
        LOGGER.error("%s (%s)", err, s3_path)
        raise err


@provide_aioclient
async def put_tag_async(s3_path: str, name: str, val: str, client: Optional[AioBaseClient] = None) -> None:
    """Put s3 object tag asynchronously"""
    if client is None:
        raise ValueError("Client not set")
    bucket, key = parse_s3_path(s3_path)
    try:
        existing_tags: Optional[Dict[str, Any]] = await get_tags_async(s3_path)
        if existing_tags and name in existing_tags:
            del existing_tags[name]
        existing_payload = [{"Key": key, "Value": val} for key, val in existing_tags.items()] if existing_tags else {}
        await client.put_object_tagging(
            Bucket=bucket,
            Key=key,
            Tagging={
                "TagSet": [
                    *existing_payload,
                    {
                        "Key": name,
                        "Value": val,
                    },
                ]
            },
        )
    except ClientError as err:
        LOGGER.warning(err)


def put_tag(s3_path: str, name: str, val: str) -> None:
    """Put s3 object tag"""
    asyncio.run(put_tag_async(s3_path, name, val))


@provide_aioclient
async def get_etag_async(s3_path: str, client: Optional[AioBaseClient] = None) -> Optional[str]:
    """Get ETag of an object asynchronously"""
    if client is None:
        raise ValueError("Client not set")
    bucket, key = parse_s3_path(s3_path)
    try:
        resp: Dict[str, Any] = await client.head_object(Bucket=bucket, Key=key)
    except ClientError as err:
        err_resp: Dict[str, Any] = err.response
        err_code = err_resp.get("Error", {}).get("Code")
        if err_code in ("404", "NoSuchKey"):
            return None
        LOGGER.error(err)
        raise err
    return str(resp.get("ETag", "")).strip('"')


@provide_aioclient
async def get_timestamp_async(s3_path: str, client: Optional[AioBaseClient] = None) -> Optional[str]:
    """Get timestamp of an object asynchronously"""
    if client is None:
        raise ValueError("Client not set")
    bucket, key = parse_s3_path(s3_path)
    try:
        resp: Dict[str, Any] = await client.head_object(Bucket=bucket, Key=key)
        ts = resp.get("LastModified")
        if ts and isinstance(ts, datetime.datetime):
            return ts.isoformat().replace("+00:00", "Z")
        return ts
    except ClientError as err:
        err_resp: Dict[str, Any] = err.response
        err_code = err_resp.get("Error", {}).get("Code")
        if err_code in ("404", "NoSuchKey"):
            return None
        LOGGER.error(err)
        raise err


def get_etag(s3_path: str) -> Optional[str]:
    """Get s3 object ETag"""
    etag: Optional[str] = asyncio.run(get_etag_async(s3_path))
    return etag


def get_tag(s3_path: str, tag: str) -> Optional[str]:
    """Get s3 object tag by name"""
    tags: Optional[Dict[str, Any]] = asyncio.run(get_tags_async(s3_path))
    if tags:
        return tags.get(tag)
    return None


def get_tags(s3_path: str) -> Optional[Dict[str, Any]]:
    """Get s3 object tag by name"""
    tags: Optional[Dict[str, Any]] = asyncio.run(get_tags_async(s3_path))
    return tags


def get_timestamp(s3_path: str) -> Optional[str]:
    """Get s3 object timestamp"""
    timestamp: Optional[str] = asyncio.run(get_timestamp_async(s3_path))
    return timestamp
