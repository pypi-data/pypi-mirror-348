"""CLI functionalities"""

from datetime import datetime
from typing import Optional
from pathlib import Path
import os
import logging
from time import time
import click
from s3async import (
    get_etag,
    get_tag,
    get_tags,
    get_timestamp,
    put_tag,
    sync_files,
)
from s3async.copy import cp
from s3async.delete import delete_object_batch, list_and_delete_object_versions
from s3async.list import list_key_versions, list_keys
from s3async.utils import compute_file_hash, VALID_SYNC_METHODS
from s3async.log import LOGGER


# pylint: disable=R0913,R0914


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option(
    "-p", "--profile", type=click.STRING, help="AWS-profile to use. Can also be set by AWS_PROFILE env-variable."
)
def cli(verbose: int, profile: Optional[str]) -> None:
    """Utility functions for working with S3"""
    if verbose == 0:
        LOGGER.setLevel(logging.WARNING)
    if verbose == 1:
        LOGGER.setLevel(logging.INFO)
    if verbose > 1:
        LOGGER.setLevel(logging.DEBUG)
    if profile:
        os.environ["AWS_PROFILE"] = profile


@cli.command("cp")
@click.argument("src-path", type=click.STRING)
@click.argument("dst-path", type=click.STRING)
def cp_cli(src_path: str, dst_path: str) -> None:
    """Copy S3 object"""
    method, result = cp(src_path, dst_path)
    click.echo(f"{method} {src_path} -> {result}")


@cli.command("rm")
@click.argument("s3-path", type=click.STRING)
@click.option("--recursive", is_flag=True, type=click.BOOL, default=False)
@click.option("--versions", is_flag=True, type=click.BOOL, default=False)
def rm_cli(s3_path: str, recursive: bool, versions: bool) -> None:
    """Delete S3 object"""
    if versions:
        if recursive:
            results_ver = list_and_delete_object_versions(s3_path, recursive=True)
        else:
            results_ver = list_and_delete_object_versions(s3_path, recursive=False)
        for path, version in results_ver:
            click.echo(f"DELETE {path} (version: {version})")
    else:
        if recursive:
            s3_objects = list_keys(s3_path, recursive=True)
            results = delete_object_batch(s3_objects)
        else:
            results = delete_object_batch([s3_path])
        for result in results:
            click.echo(f"DELETE {result}")


@cli.command("ls")
@click.argument("s3-path", type=click.STRING)
@click.option("-r", "--regexp", type=click.STRING, default=None, help="Regular expression filter to apply to results")
@click.option(
    "-ts",
    "--time-start",
    type=click.STRING,
    default=None,
    help="Select only objects with LastModified date more recent than value (inclusive)",
)
@click.option(
    "-te",
    "--time-end",
    type=click.STRING,
    default=None,
    help="Selects only objects with LastModified date older than value (exclusive)",
)
@click.option("-c", "--contains", type=click.STRING, default=None, help="Select only keys that contain value")
@click.option("-e", "--ends-with", type=click.STRING, default=None, help="Select only keys that end with value")
@click.option("-r", "--regexp", type=click.STRING, default=None, help="Regular expression filter to apply to results")
@click.option("--recursive", is_flag=True, type=click.BOOL, default=False)
@click.option("--versions", is_flag=True, type=click.BOOL, default=False)
@click.option("--original", is_flag=True, type=click.BOOL, default=False, help="Only retrieve the original version")
def ls_cli(  # noqa: PLR0913
    s3_path: str,
    regexp: Optional[str],
    recursive: bool,
    versions: bool,
    original: bool,
    time_start: Optional[str],
    time_end: Optional[str],
    contains: Optional[str],
    ends_with: Optional[str],
) -> None:
    """List s3 object paths"""

    if (time_start or time_end or contains) and not recursive:
        raise click.BadOptionUsage("--recursive", "Using filters other than regexp requires using recursive mode")

    try:
        tss = datetime.fromisoformat(time_start) if time_start else None
        tse = datetime.fromisoformat(time_end) if time_end else None
    except ValueError:
        raise click.BadParameter("Unable to parse timestamp")  # pylint: disable=W0707

    if original and not versions:
        versions = True

    if versions and any([time_start, time_end, contains, ends_with]):
        raise click.BadOptionUsage(
            "--versions", "Using filters other than regexp with --versions is currently not supported"
        )

    if versions:
        key_ver = list_key_versions(s3_path, regex_filter=regexp, recursive=recursive, only_original=original)
        for key, ver, last_modified, is_latest in key_ver:
            latest_str = " [LATEST]" if is_latest else ""
            click.echo(f" {key} (version: {ver} {last_modified}){latest_str}")
    else:
        keys = list_keys(
            s3_path,
            regex_filter=regexp,
            recursive=recursive,
            contains_filter=contains,
            endswith_filter=ends_with,
            time_start=tss,
            time_end=tse,
        )
        for key in keys:
            click.echo(key)


@cli.command("hash")
@click.argument("file-path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def hash_cli(file_path: Path) -> None:
    """Computes a MD5 digest of a file"""
    hashval = compute_file_hash(file_path)
    click.echo(hashval)


@cli.command("sync")
@click.argument("in-path", type=click.STRING)
@click.argument("out-path", type=click.STRING)
@click.option("--recursive", is_flag=True, default=False, help="Include subfolders or prefixes in sync")
@click.option(
    "--delete",
    is_flag=True,
    default=False,
    help="""Delete existing files present in the output path that are not present in the input path
 (respects both --recursive and --regexp)""",
)
@click.option("-r", "--regexp", type=click.STRING, default=None, help="Regular expression filter to apply to results")
@click.option(
    "--method",
    default="etag",
    type=click.Choice(VALID_SYNC_METHODS),
    help="Method used to decide if a sync is required or not. "
    "`etag` uses the built-in ETag and compares against local file MD5 hashes "
    "(note that ETag is not always guaranteed to be MD5 hash). "
    "`hash` uses a custom tag containing the file MD5 digest. "
    "`timestamp` uses exact timestamp comparison",
)
@click.option(
    "-p",
    "--dst-profile",
    type=click.STRING,
    help="Destination bucket AWS-profile to use, if different from source profile. "
    "Can also be set by AWS_DST_PROFILE env-variable.",
)
def sync_cli(  # noqa: PLR0913
    in_path: str,
    out_path: Path,
    recursive: bool,
    method: str,
    regexp: Optional[str],
    delete: bool,
    dst_profile: Optional[str],
) -> None:
    """Sync objects between local and S3 path or two S3 paths"""

    start = time()
    if dst_profile:
        os.environ["AWS_DST_PROFILE"] = dst_profile

    src_files, dst_files = sync_files(
        in_path, out_path, recursive=recursive, method=method, regex_filter=regexp, delete=delete
    )
    results = list(zip(src_files, dst_files))
    duration = time() - start
    if len(results) == 0:
        click.echo("Nothing to sync")
    else:
        click.echo(f"Synced {len(results)} files in {duration:.2f}")


@cli.group("tag")
def tag_cli() -> None:
    """Set and get object tags"""


@tag_cli.command("set")
@click.argument("s3-path", type=click.STRING)
@click.argument("name", type=click.STRING)
@click.argument("val", type=click.STRING)
def set_cli(s3_path: str, name: str, val: str) -> None:
    """Set tag"""
    put_tag(s3_path, name, val)
    click.echo("Done")


@tag_cli.command("get")
@click.argument("s3-path", type=click.STRING)
@click.argument("name", type=click.STRING)
def get_cli(s3_path: str, name: str) -> None:
    """Get tag"""
    tag_value = get_tag(s3_path, name)
    click.echo(tag_value)


@tag_cli.command("ls")
@click.argument("s3-path", type=click.STRING)
def ls_tags_cli(s3_path: str) -> None:
    """List all tags"""
    tags = get_tags(s3_path)
    click.echo(tags)


@cli.group("meta")
def meta_cli() -> None:
    """Get object metadata information"""


@meta_cli.command("timestamp")
@click.argument("s3-path", type=click.STRING)
def timestamp_cli(s3_path: str) -> None:
    """Get object modified timestamp"""
    timestamp = get_timestamp(s3_path)
    click.echo(timestamp)


@meta_cli.command("etag")
@click.argument("s3-path", type=click.STRING)
def etag_cli(s3_path: str) -> None:
    """Get object ETag"""
    etag = get_etag(s3_path)
    click.echo(etag)
