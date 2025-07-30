"""Shard tests to support parallelism across multiple machines."""

import hashlib
from typing import Iterable, List, Sequence
import xml.etree.ElementTree as ET

from _pytest import junitxml
from _pytest import nodes  # for type checking only
from pytest import Item


def _shard_by_duration(items: List[dict], num_bins: int):
    items.sort(reverse=True, key=lambda x: x["time"])

    bin_loads = [0] * num_bins

    bin_assignments = []
    for item in items:
        min_load_bin = min(range(num_bins), key=lambda i: bin_loads[i])

        bin_assignments.append(min_load_bin)
        bin_loads[min_load_bin] += item["time"]

    return bin_assignments


def positive_int(x) -> int:
    x = int(x)
    if x < 0:
        raise ValueError(f"Argument {x} must be positive")
    return x


def pytest_addoption(parser):
    """Add pytest-shard specific configuration parameters."""
    group = parser.getgroup("shard")
    group.addoption(
        "--shard-id",
        dest="shard_id",
        type=positive_int,
        default=0,
        help="Number of this shard.",
    )
    group.addoption(
        "--num-shards",
        dest="num_shards",
        type=positive_int,
        default=1,
        help="Total number of shards.",
    )
    group.addoption(
        "--shard-by-duration",
        dest="shard_by_duration",
        action="store_true",
        default=False,
        help="Whether to shard by duration or not.",
    )


def pytest_report_collectionfinish(config, items: Sequence[nodes.Node]) -> str:
    """Log how many and, if verbose, which items are tested in this shard."""
    msg = f"Running {len(items)} items in this shard"
    if config.option.verbose > 0 and config.getoption("num_shards") > 1:
        msg += ": " + ", ".join([item.nodeid for item in items])
    return msg


def sha256hash(x: str) -> int:
    return int.from_bytes(hashlib.sha256(x.encode()).digest(), "little")


def duration_shard(items: Iterable[Item], num_shards: int):
    item_address = [junitxml.mangle_test_address(i.nodeid) for i in items]
    root = ET.parse("durations.xml").getroot()
    data = []
    for e in root.findall("*/testcase"):
        data.append(e.attrib)

    for d in data:
        d["time"] = float(d["time"])

    data = sorted(
        data, key=lambda x: item_address.index([x["classname"], x["name"]])
    )

    shard_ids = _shard_by_duration(data, num_shards)
    return shard_ids


def filter_items_by_shard(
    items: Iterable[Item],
    shard_id: int,
    num_shards: int,
    shard_by_duration: bool,
) -> Sequence[Item]:
    """Computes `items` that should be tested in `shard_id` out of `num_shards` total shards."""
    if shard_by_duration:
        shards = duration_shard(items, num_shards)
    else:
        shards = [sha256hash(item.nodeid) % num_shards for item in items]
    new_items = []
    for shard, item in zip(shards, items):
        if shard == shard_id:
            new_items.append(item)
    return new_items


def pytest_collection_modifyitems(config, items: List[Item]):
    """Mutate the collection to consist of just items to be tested in this shard."""
    shard_id = config.getoption("shard_id")
    shard_total = config.getoption("num_shards")
    shard_by_duration = config.getoption("shard_by_duration")
    if shard_id >= shard_total:
        raise ValueError(
            "shard_num = f{shard_num} must be less than shard_total = f{shard_total}"
        )

    items[:] = filter_items_by_shard(
        items, shard_id, shard_total, shard_by_duration
    )
