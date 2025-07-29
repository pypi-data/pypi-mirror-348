"""List operations"""

from datetime import datetime
from functools import reduce
from typing import AsyncGenerator, Dict, Generator, List, Optional, Tuple
from pathlib import Path
import asyncio
from aiobotocore.client import AioBaseClient  # type: ignore
from s3async.model import KeyVersionInfo
from s3async.utils import (
    join_path,
    regex_match,
    parse_s3_path,
    provide_aioclient,
)


def list_key_versions(
    s3_path: str, regex_filter: Optional[str] = None, recursive: bool = True, only_original: bool = False
) -> List[KeyVersionInfo]:
    """List keys and object versions"""

    @provide_aioclient
    async def _get_result(client: Optional[AioBaseClient] = None) -> List[KeyVersionInfo]:
        return [
            key_ver
            async for key_ver in list_versions_async(
                s3_path, regex_filter=regex_filter, recursive=recursive, only_original=only_original, client=client
            )
        ]

    if not s3_path.endswith("/"):
        s3_path = f"{s3_path}/"
    return asyncio.run(_get_result())


def list_keys(  # noqa: PLR0913
    s3_path: str,
    regex_filter: Optional[str] = None,
    recursive: bool = True,
    time_start: Optional[datetime] = None,
    time_end: Optional[datetime] = None,
    contains_filter: Optional[str] = None,
    endswith_filter: Optional[str] = None,
    client: Optional[AioBaseClient] = None,
) -> List[str]:
    """List keys"""

    @provide_aioclient
    async def _get_result(client: Optional[AioBaseClient] = None) -> List[str]:
        return [
            key
            async for key in list_keys_async(
                s3_path,
                regex_filter=regex_filter,
                recursive=recursive,
                time_start=time_start,
                time_end=time_end,
                contains_filter=contains_filter,
                endswith_filter=endswith_filter,
                client=client,
            )
        ]

    if not s3_path.endswith("/"):
        s3_path = f"{s3_path}/"
    return asyncio.run(_get_result(client=client))


def _get_jmespath_query(
    time_start: Optional[datetime] = None,
    time_end: Optional[datetime] = None,
    contains_filter: Optional[str] = None,
    endswith_filter: Optional[str] = None,
) -> str:
    """Turn various filters into a single JMESPath query string"""
    queries = []
    if time_start:
        ts_start = time_start.isoformat(sep=" ", timespec="seconds")
        queries.append(f"to_string(LastModified) >= '\"{ts_start}\"'")
    if time_end:
        ts_end = time_end.isoformat(sep=" ", timespec="seconds")
        queries.append(f"to_string(LastModified) < '\"{ts_end}\"'")
    if endswith_filter:
        queries.append(f"ends_with(Key, '{endswith_filter}')")
    if contains_filter:
        queries.append(f"contains(Key, '{contains_filter}')")

    if len(queries) == 0:
        return ""

    query_string = " && ".join(queries)
    return f"Contents[?{query_string}].Key"


async def list_keys_async(  # noqa: PLR0913
    s3_path: str,
    regex_filter: Optional[str] = None,
    recursive: bool = True,
    time_start: Optional[datetime] = None,
    time_end: Optional[datetime] = None,
    contains_filter: Optional[str] = None,
    endswith_filter: Optional[str] = None,
    client: Optional[AioBaseClient] = None,
) -> AsyncGenerator[str, None]:
    """List all S3 keys in bucket/prefix/ and optionally filter with LastModified date or regexp"""

    async def _list_keys(queue: asyncio.Queue, path: str) -> None:  # type: ignore
        if client is None:
            raise ValueError("Client not set")
        bucket, prefix = parse_s3_path(path)
        paginator = client.get_paginator("list_objects_v2")
        iterator = (
            paginator.paginate(Bucket=bucket, Prefix=prefix)
            if recursive
            else paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/")
        )

        query = _get_jmespath_query(time_start, time_end, contains_filter, endswith_filter)

        if not recursive and query:
            raise ValueError("using search filters other than regexp requires recursive mode")

        if not query:
            query = "Contents[*].Key"

        filtered = iterator.search(query)
        async for result in filtered:
            if result is None:
                continue
            key = result
            if regex_filter is not None:
                if regex_match(regex_filter, key):
                    await queue.put(f"s3://{bucket}/{key}")
            else:
                await queue.put(f"s3://{bucket}/{key}")

    que: asyncio.Queue = asyncio.Queue()  # type: ignore
    list_task = asyncio.create_task(_list_keys(que, s3_path))

    while True:
        try:
            key = que.get_nowait()
            yield key
        except asyncio.QueueEmpty:
            if list_task.done() or list_task.cancelled():
                if err := list_task.exception():
                    raise err  # pylint: disable=W0707
                return
            await asyncio.sleep(1)


def _filter_oldest_timestamp(data: List[KeyVersionInfo]) -> List[KeyVersionInfo]:
    """Filter data by only including oldest timestamp"""

    def _versions_by_key(acc: Dict[str, List[KeyVersionInfo]], item: KeyVersionInfo) -> Dict[str, List[KeyVersionInfo]]:
        key, _, _, _ = item
        if key in acc:
            acc[key].append(item)
        else:
            acc[key] = [item]
        return acc

    def _reduce_to_latest(acc: List[KeyVersionInfo], item: List[KeyVersionInfo]) -> List[KeyVersionInfo]:
        timestamps = [entry[2] for entry in item]
        min_idx = timestamps.index(min(timestamps))
        acc.append(item[min_idx])
        return acc

    versions: Dict[str, List[KeyVersionInfo]] = reduce(_versions_by_key, data, {})
    versions_list = [val for _, val in versions.items()]
    return reduce(_reduce_to_latest, versions_list, [])


async def list_versions_async(
    s3_path: str,
    regex_filter: Optional[str] = None,
    recursive: bool = True,
    only_original: bool = False,
    client: Optional[AioBaseClient] = None,
) -> AsyncGenerator[Tuple[str, str, datetime, bool], None]:
    """List all S3 keys and their versions in bucket/prefix/ and optionally filter with regexp"""

    async def _list_versions(queue: asyncio.Queue, path: str) -> None:  # type: ignore
        if client is None:
            raise ValueError("Client not set")
        bucket, prefix = parse_s3_path(path)
        result = await client.list_object_versions(Bucket=bucket, Prefix=prefix, Delimiter="/")
        if "Versions" in result:
            # If we provided regex filter, apply to any keys found in this prefix
            if regex_filter is not None:
                pattern = regex_filter
                filtered = list(filter(lambda x: regex_match(pattern, x["Key"]), result["Versions"]))
            else:
                filtered = result["Versions"]
            filtered = list(filter(lambda x: x["Size"] > 0, filtered))
            data = list(
                map(
                    lambda x: (f"s3://{bucket}/" + str(x["Key"]), x["VersionId"], x["LastModified"], x["IsLatest"]),
                    filtered,
                )
            )
            if only_original:
                data = _filter_oldest_timestamp(data)
            for key_version in data:
                await queue.put(key_version)
        if recursive and "CommonPrefixes" in result:
            # If result object has CommonPrefixes, we have found "subfolders"
            # Walk through those recursively and yield keys to upstream.
            reqs = []
            for x in result["CommonPrefixes"]:
                new_path = join_path(bucket, x["Prefix"])
                reqs.append(_list_versions(queue, new_path))
            await asyncio.gather(*reqs)

    que: asyncio.Queue = asyncio.Queue()  # type: ignore
    list_task = asyncio.create_task(_list_versions(que, s3_path))

    while True:
        try:
            key = que.get_nowait()
            yield key
        except asyncio.QueueEmpty:
            if list_task.done() or list_task.cancelled():
                if err := list_task.exception():
                    raise err  # pylint: disable=W0707
                return
            await asyncio.sleep(1)


def list_files(path: Path, recursive: bool = False, regex_filter: Optional[str] = None) -> Generator[Path, None, None]:
    """List files in a path returning absolute paths"""
    if recursive:
        result_iter = Path(path).rglob("*")
    else:
        result_iter = Path(path).glob("*")
    for result in result_iter:
        if result.is_file():
            if regex_filter:
                if not regex_match(regex_filter, str(result)):
                    continue
            yield result
