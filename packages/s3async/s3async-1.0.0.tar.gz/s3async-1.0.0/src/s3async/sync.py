"""Sync related functionalities"""

from typing import Any, AsyncGenerator, Callable, Generator, List, Optional, Tuple, Union
from pathlib import Path
import os
import asyncio
from aiobotocore.client import AioBaseClient  # type: ignore
from s3async.delete import delete_object_async
from s3async.list import list_files, list_keys_async
from s3async.log import LOGGER
from s3async.get import (
    get_object_async,
)
from s3async.put import put_object_async, s3_to_s3_async
from s3async.tag import get_etag_async, get_tags_async, get_timestamp_async
from s3async.utils import (
    compute_file_hash_async,
    get_aioclient,
    is_s3_path,
    VALID_SYNC_METHODS,
    provide_aioclient,
    parse_datetime,
)

# pylint: disable=R0913,R0914

CompareResult = Optional[Tuple[str, str, Optional[str]]]


def sync_files(  # noqa: PLR0913
    src_path: Union[Path, str],
    dst_path: Union[Path, str],
    recursive: bool = True,
    method: str = "etag",
    regex_filter: Optional[str] = None,
    delete: bool = False,
) -> Tuple[List[str], List[str]]:
    """Sync from source path to destination path. One or both of the paths needs to be S3 path.
    The sync uses either timestamp, ETag or MD5 hash in separate `hash` tag to determine if a sync is needed.
    Note that ETag and the hash-tag are usually equal. ETag is however not guaranteed
    to be the MD5 hash in all situations, e.g. if multipart upload was used."""

    if method not in VALID_SYNC_METHODS:
        raise ValueError(f"Invalid sync method received - must be one of {VALID_SYNC_METHODS}")

    if is_s3_path(src_path) and is_s3_path(dst_path):
        LOGGER.debug("S3 to S3 sync from %s to %s", src_path, dst_path)
        return asyncio.run(
            _sync_s3_to_s3(
                str(src_path),
                str(dst_path),
                recursive=recursive,
                method=method,
                regex_filter=regex_filter,
                delete=delete,
            )
        )
    if is_s3_path(src_path) and not is_s3_path(dst_path):
        LOGGER.debug("S3 to local sync from %s to %s", src_path, dst_path)
        return asyncio.run(
            _sync_s3_to_local(
                str(src_path),
                Path(dst_path),
                recursive=recursive,
                method=method,
                regex_filter=regex_filter,
                delete=delete,
            )
        )
    if not is_s3_path(src_path) and is_s3_path(dst_path):
        LOGGER.debug("Local to S3 sync from %s to %s", src_path, dst_path)
        return asyncio.run(
            _sync_local_to_s3(
                Path(src_path),
                str(dst_path),
                recursive=recursive,
                method=method,
                regex_filter=regex_filter,
                delete=delete,
            )
        )
    raise ValueError("At least one of the inputs needs to be valid S3 path")


@provide_aioclient
async def _get_s3_fingerprint(path: str, method: str, client: Optional[AioBaseClient] = None) -> Optional[str]:
    """Get fingerprint aka timestamp or one of the hashes from tags"""
    if client is None:
        raise ValueError("Client not set")

    if method == "etag":
        return await get_etag_async(path, client)
    if method == "hash":
        tags = await get_tags_async(path, client)
        return tags.get("hash") if tags else None
    if method == "timestamp":
        timestamp = await get_timestamp_async(path, client)
        return str(parse_datetime(timestamp).timestamp()) if timestamp else None
    raise ValueError("Invalid method")


async def _get_local_fingerprint(
    path: Path, method: str, semaphore: Optional[asyncio.Semaphore] = None
) -> Optional[str]:
    """Get fingerprint aka date modified or md5 hash"""

    if method in ["etag", "hash"]:
        return await compute_file_hash_async(path, semaphore) if path.is_file() else None
    if method == "timestamp":
        return str(path.stat().st_mtime) if path.is_file() else None
    raise ValueError("Invalid method")


async def _should_delete_local_to_s3(path: Path, target: str) -> Optional[str]:
    """Check if local path exists"""
    return target if not path.is_file() else None


async def _should_delete_s3_to_local(key: str, target: Path, client: AioBaseClient) -> Optional[Path]:
    """Check if local path exists"""
    return target if await get_etag_async(key, client) is None else None


async def _should_delete_s3_to_s3(key: str, target: str, client: AioBaseClient) -> Optional[str]:
    """Check if local path exists"""
    return target if await get_etag_async(key, client) is None else None


def _needs_sync(
    src_fp: Union[Optional[str], Optional[int]],
    dst_fp: Union[Optional[str], Optional[int]],
    method: str,
) -> bool:
    # needs_sync is a list of tuples (src_path, dst_path, epoch).
    if method == "timestamp":
        return src_fp is None or dst_fp is None or int(float(dst_fp)) < int(float(src_fp))
    return src_fp is None or dst_fp is None or dst_fp != src_fp


def check(
    src_paths: Union[List[Path], List[str]],
    dst_paths: Union[List[Path], List[str]],
    method: str = "etag",
) -> Tuple[List[str], List[str]]:
    """Check need to sync between two file lists. This is a sync-wrapper for check_async.
    If more control over the client definitions is needed, switch to the async version."""
    return asyncio.run(check_async(src_paths, dst_paths, method=method))


@provide_aioclient
async def check_async(
    src_paths: Union[List[Path], List[str]],
    dst_paths: Union[List[Path], List[str]],
    method: str = "etag",
    client: Optional[AioBaseClient] = None,
    dst_client: Optional[AioBaseClient] = None,
) -> Tuple[List[str], List[str]]:
    """Check need to sync between two file lists"""
    if len(src_paths) != len(dst_paths):
        raise ValueError("Input path lists must be of equal length")
    if method not in VALID_SYNC_METHODS:
        raise ValueError("Invalid sync method")

    src_s3_paths = list(filter(is_s3_path, src_paths))
    dst_s3_paths = list(filter(is_s3_path, dst_paths))

    if len(src_s3_paths) > 0 and not len(src_s3_paths) == len(src_paths):
        raise ValueError("Mixed path types (s3, local) not allowed")
    if len(dst_s3_paths) > 0 and not len(dst_s3_paths) == len(dst_paths):
        raise ValueError("Mixed path types (s3, local) not allowed")

    src_type = "s3" if len(src_s3_paths) == len(src_paths) else "local"
    dst_type = "s3" if len(dst_s3_paths) == len(dst_paths) else "local"

    compare_func: Optional[Callable[..., Any]] = None

    if src_type == "local" and dst_type == "s3":
        compare_func = _compare_local_s3
    elif src_type == "s3" and dst_type == "local":
        compare_func = _compare_s3_local
    elif src_type == "s3" and dst_type == "s3":
        compare_func = _compare_s3_s3

    if not compare_func:
        raise ValueError("Unknown combination")

    semaphore = asyncio.Semaphore(100)

    reqs: List[asyncio.Task[Any]] = [
        asyncio.create_task(
            compare_func(path, dst_paths[i], method=method, client=client, dst_client=dst_client, semaphore=semaphore)
        )
        for i, path in enumerate(src_paths)
    ]

    results = list(filter(bool, await asyncio.gather(*reqs)))
    if len(results) > 0:
        sync_src, sync_dst, _ = list(zip(*results))
        return sync_src, sync_dst
    return [], []


async def _compare_s3_local(  # noqa: PLR0913
    s3_path: str,
    local_path: Path,
    method: str,
    client: AioBaseClient,
    dst_client: Optional[AioBaseClient] = None,
    semaphore: Optional[asyncio.Semaphore] = None,
) -> CompareResult:
    del dst_client
    dst_fp = await _get_local_fingerprint(local_path, method=method, semaphore=semaphore)
    if dst_fp is None:
        return s3_path, str(local_path), None
    src_fp = await _get_s3_fingerprint(s3_path, method=method, client=client)
    if _needs_sync(src_fp, dst_fp, method=method):
        return s3_path, str(local_path), src_fp
    return None


async def _s3_to_local_needs_sync_filter(
    keys: AsyncGenerator[str, None],
    src_path: str,
    target_path: Path,
    method: str,
    client: AioBaseClient,
) -> AsyncGenerator[CompareResult, None]:
    tasks = []
    # Create a semaphore to set a hard bound for the number of files we open for hash computations
    semaphore = asyncio.Semaphore(100)
    async for s3_path in keys:
        relative_s3_path = s3_path.replace(src_path, "")
        local_path = Path(target_path, relative_s3_path.lstrip("/"))
        tasks.append(
            asyncio.create_task(_compare_s3_local(s3_path, local_path, method, client=client, semaphore=semaphore))
        )
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)  # type: ignore
        for task in done:
            result = task.result()
            if result:
                yield result


async def _compare_local_s3(  # noqa: PLR0913
    local_path: Path,
    s3_path: str,
    method: str,
    client: AioBaseClient,
    dst_client: Optional[AioBaseClient] = None,
    semaphore: Optional[asyncio.Semaphore] = None,
) -> CompareResult:
    del dst_client
    dst_fp = await _get_s3_fingerprint(s3_path, method=method, client=client)
    if dst_fp is None:
        return str(local_path), s3_path, None
    src_fp = await _get_local_fingerprint(local_path, method=method, semaphore=semaphore)
    if _needs_sync(src_fp, dst_fp, method=method):
        return str(local_path), s3_path, src_fp
    return None


async def _local_to_s3_needs_sync_filter(
    paths: Generator[Path, None, None],
    src_path: Path,
    dst_path: str,
    method: str,
    client: AioBaseClient,
) -> AsyncGenerator[CompareResult, None]:
    tasks = []
    # Create a semaphore to set a hard bound for the number of files we open for hash computations
    semaphore = asyncio.Semaphore(100)
    for path in paths:
        file_relative = path.relative_to(Path(src_path))
        s3_path = os.path.join(dst_path, file_relative)
        tasks.append(
            asyncio.create_task(_compare_local_s3(path, s3_path, method=method, client=client, semaphore=semaphore))
        )
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)  # type: ignore
        for task in done:
            result = task.result()
            if result:
                yield result


async def _local_to_s3_needs_delete_filter(
    keys: AsyncGenerator[str, None], src_path: Path, dst_path: str
) -> AsyncGenerator[str, None]:
    tasks = []
    async for s3_path in keys:
        relative_s3_path = s3_path.replace(dst_path, "")
        local_path = Path(src_path, relative_s3_path.lstrip("/"))
        tasks.append(asyncio.create_task(_should_delete_local_to_s3(local_path, s3_path)))
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)  # type: ignore
        for task in done:
            result = task.result()
            if result:
                yield result


async def _s3_to_local_needs_delete_filter(
    paths: Generator[Path, None, None], src_path: str, dst_path: Path, client: AioBaseClient
) -> AsyncGenerator[Path, None]:
    tasks = []
    for path in paths:
        file_relative = path.relative_to(dst_path)
        s3_path = os.path.join(src_path, file_relative)
        tasks.append(asyncio.create_task(_should_delete_s3_to_local(s3_path, path, client)))
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)  # type: ignore
        for task in done:
            result = task.result()
            if result:
                yield result


async def _s3_to_s3_needs_delete_filter(
    keys: AsyncGenerator[str, None],
    src_path: str,
    dst_path: str,
    client: AioBaseClient,
) -> AsyncGenerator[str, None]:
    tasks = []
    async for s3_path in keys:
        relative_s3_path = s3_path.replace(dst_path, "")
        target_s3_path = os.path.join(src_path, relative_s3_path)
        tasks.append(asyncio.create_task(_should_delete_s3_to_s3(target_s3_path, s3_path, client=client)))
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)  # type: ignore
        for task in done:
            result = task.result()
            if result:
                yield result


async def _compare_s3_s3(  # noqa: PLR0913
    s3_path: str,
    target_s3_path: str,
    method: str,
    client: Optional[AioBaseClient] = None,
    dst_client: Optional[AioBaseClient] = None,
    semaphore: Optional[asyncio.Semaphore] = None,
) -> CompareResult:
    if dst_client is None:
        dst_client = client
    del semaphore
    dst_fp = await _get_s3_fingerprint(target_s3_path, method=method, client=dst_client)
    if dst_fp is None:
        return s3_path, target_s3_path, None
    src_fp = await _get_s3_fingerprint(s3_path, method=method, client=client)
    if _needs_sync(src_fp, dst_fp, method=method):
        return s3_path, target_s3_path, src_fp
    return None


async def _s3_to_s3_needs_sync_filter(  # noqa: PLR0913
    keys: AsyncGenerator[str, None],
    src_path: str,
    dst_path: str,
    method: str,
    client: AioBaseClient,
    dst_client: Optional[AioBaseClient] = None,
) -> AsyncGenerator[CompareResult, None]:
    """Filter to-be-synced keys s3 => s3"""
    if dst_client is None:
        dst_client = client

    tasks = []
    async for s3_path in keys:
        relative_s3_path = s3_path.replace(src_path, "")
        target_s3_path = os.path.join(dst_path, relative_s3_path)
        tasks.append(
            asyncio.create_task(
                _compare_s3_s3(s3_path, target_s3_path, method=method, client=client, dst_client=dst_client)
            )
        )
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)  # type: ignore
        for task in done:
            result = task.result()
            if result:
                yield result


@provide_aioclient
async def _sync_local_to_s3(  # noqa: PLR0913
    src_path: Path,
    dst_path: str,
    method: str,
    client: Optional[AioBaseClient] = None,
    recursive: bool = True,
    regex_filter: Optional[str] = None,
    delete: bool = False,
) -> Tuple[List[str], List[str]]:
    """Sync local folder to S3. Returns the list of modified files."""

    async def _put_with_sema(
        sema: asyncio.Semaphore,
        src_path: Path,
        dst_path: str,
        client: Optional[AioBaseClient] = None,
        set_hash: bool = False,
    ) -> Optional[str]:
        await sema.acquire()
        try:
            res = await put_object_async(src_path, dst_path, client=client, set_hash=set_hash)
        finally:
            sema.release()
        return res

    if client is None:
        raise ValueError("Client not set")

    if not str(dst_path).endswith("/"):
        dst_path = str(dst_path) + "/"

    reqs = []
    src_paths = []

    files_iter = list_files(Path(src_path), recursive=recursive, regex_filter=regex_filter)
    needs_sync = _local_to_s3_needs_sync_filter(files_iter, src_path, dst_path, method=method, client=client)
    sema = asyncio.Semaphore(100)
    async for local_path, s3_path, _ in needs_sync:  # type: ignore
        set_hash = method == "hash"
        src_paths.append(local_path)
        LOGGER.info("sync %s -> %s", local_path, s3_path)
        reqs.append(
            asyncio.create_task(_put_with_sema(sema, Path(local_path), str(s3_path), client=client, set_hash=set_hash))
        )
    results = await asyncio.gather(*reqs)

    if delete:
        deletes = []
        existing = list_keys_async(dst_path, regex_filter=regex_filter, recursive=recursive, client=client)
        needs_delete = _local_to_s3_needs_delete_filter(existing, src_path, dst_path)
        async for item in needs_delete:
            LOGGER.info("delete %s", item)
            deletes.append(asyncio.create_task(delete_object_async(item, client=client)))
        await asyncio.gather(*deletes)

    return src_paths, results


@provide_aioclient
async def _sync_s3_to_s3(  # noqa: PLR0913
    src_path: str,
    dst_path: str,
    method: str,
    client: Optional[AioBaseClient] = None,
    recursive: bool = True,
    regex_filter: Optional[str] = None,
    delete: bool = False,
) -> Tuple[List[str], List[str]]:
    """Sync S3 to S3. Returns the list of modified files."""

    async def _work(dst_client: Optional[AioBaseClient] = None) -> Tuple[List[str], List[str]]:
        reqs: List[Any] = []
        src_paths = []
        keys_iter = list_keys_async(src_path, recursive=recursive, client=client, regex_filter=regex_filter)
        needs_sync = _s3_to_s3_needs_sync_filter(
            keys_iter, src_path, dst_path, method=method, client=client, dst_client=dst_client
        )
        async for src_s3_path, dst_s3_path, _ in needs_sync:  # type: ignore
            src_paths.append(src_s3_path)
            set_hash = method == "hash"
            LOGGER.info("sync %s -> %s", src_s3_path, dst_s3_path)
            reqs.append(
                asyncio.create_task(
                    s3_to_s3_async(src_s3_path, dst_s3_path, client, set_hash=set_hash, dst_client=dst_client),
                )
            )

        results = await asyncio.gather(*reqs)

        if delete:
            deletes = []
            existing = list_keys_async(dst_path, regex_filter=regex_filter, recursive=recursive, client=client)
            needs_delete = _s3_to_s3_needs_delete_filter(existing, src_path, dst_path, client=client)
            async for item in needs_delete:
                LOGGER.info("delete %s", item)
                deletes.append(asyncio.create_task(delete_object_async(item, client=client)))
            await asyncio.gather(*deletes)

        return src_paths, results

    if client is None:
        raise ValueError("Client not set")
    if not src_path.endswith("/"):
        src_path += "/"
    if not dst_path.endswith("/"):
        dst_path += "/"

    dst_profile = os.getenv("AWS_DST_PROFILE")
    dst_ctx = get_aioclient(dst_profile, os.getenv("AWS_ENDPOINT")) if dst_profile else None

    if dst_ctx:
        async with dst_ctx as dst_client:
            return await _work(dst_client)
    return await _work()


@provide_aioclient
async def _sync_s3_to_local(  # noqa: PLR0913
    src_path: str,
    dst_path: Union[Path, str],
    method: str,
    client: Optional[AioBaseClient] = None,
    recursive: bool = True,
    regex_filter: Optional[str] = None,
    delete: bool = False,
) -> Tuple[List[str], List[str]]:
    """Sync S3 to local folder. Returns the list of modified files."""

    async def _get_with_sema(
        sema: asyncio.Semaphore,
        src_path: str,
        dst_path: Path,
        client: Optional[AioBaseClient] = None,
    ) -> Optional[Path]:
        await sema.acquire()
        try:
            res = await get_object_async(src_path, dst_path, client=client)
        finally:
            sema.release()
        return res

    if client is None:
        raise ValueError("Client not set")

    if not src_path.endswith("/"):
        src_path += "/"

    reqs = []
    times = []
    src_paths = []
    keys_iter = list_keys_async(src_path, recursive=recursive, client=client, regex_filter=regex_filter)
    needs_sync = _s3_to_local_needs_sync_filter(keys_iter, src_path, Path(dst_path), method=method, client=client)
    sema = asyncio.Semaphore(100)
    async for s3_path, local_path, src_fp in needs_sync:  # type: ignore
        src_paths.append(local_path)
        reqs.append(asyncio.create_task(_get_with_sema(sema, s3_path, Path(local_path), client=client)))
        LOGGER.info("sync %s -> %s", s3_path, local_path)
        if method == "timestamp":
            times.append(src_fp)

    results = await asyncio.gather(*reqs)
    if method == "timestamp":
        for i, path in enumerate(results):
            timestamp = times[i]
            if timestamp:
                utime = int(float(timestamp))
                os.utime(Path(path).resolve(), (utime, utime))
            else:
                LOGGER.warning("Unable to set date modified for synced file correctly")

    if delete:
        existing = list_files(Path(dst_path), regex_filter=regex_filter, recursive=recursive)
        needs_delete = _s3_to_local_needs_delete_filter(existing, src_path, Path(dst_path), client=client)
        async for item in needs_delete:
            LOGGER.info("delete %s", item)
            item.unlink()

    return src_paths, results
