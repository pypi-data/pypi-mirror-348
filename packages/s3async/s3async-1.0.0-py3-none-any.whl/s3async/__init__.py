"""Helper functions for interacting with s3 using async for batched operations."""

__version__ = "1.0.0"  # NOTE Use `bump2version patch` to bump versions correctly

# Expose key functions at module top level
from s3async.list import list_keys, list_key_versions
from s3async.put import put_object, put_json, put_object_batch
from s3async.get import get_json, get_object, get_object_batch
from s3async.delete import delete_object_batch, list_and_delete_object_versions, delete_object_versions
from s3async.tag import get_etag, get_tag, get_tags, get_timestamp, put_tag
from s3async.copy import cp
from s3async.sync import sync_files

__all__ = [
    "list_key_versions",
    "list_keys",
    "put_json",
    "put_object",
    "put_object_batch",
    "get_json",
    "get_object",
    "get_object_batch",
    "delete_object_batch",
    "list_and_delete_object_versions",
    "delete_object_versions",
    "get_etag",
    "get_tag",
    "get_tags",
    "get_timestamp",
    "put_tag",
    "cp",
    "sync_files",
]
