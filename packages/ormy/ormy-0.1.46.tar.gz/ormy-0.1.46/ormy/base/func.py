import hashlib
import json
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any, Optional
from uuid import UUID, uuid4

# ----------------------- #


def utcnow() -> int:
    """
    Returns the current UTC datetime as a Unix timestamp.

    Returns:
        int: The current datetime as a Unix timestamp.
    """

    return int(datetime.now(UTC).timestamp())


# ....................... #


def timestamp_to_datetime(t: int | float) -> datetime:
    """
    Converts a Unix timestamp to a datetime object.

    Args:
        dt (int): The Unix timestamp to convert.

    Returns:
        datetime: The datetime object representing the given timestamp.
    """

    return datetime.fromtimestamp(float(t), tz=UTC)


# ....................... #


def datetime_to_timestamp(dt: datetime) -> int:
    """
    Converts a datetime object to a Unix timestamp.

    Args:
        dt (datetime): The datetime object to convert.

    Returns:
        int: The Unix timestamp representing the given datetime.
    """

    return int(dt.timestamp())


# ----------------------- #
# Hash utils


def hash_from_any(val: Any) -> str:
    """
    Calculate the MD5 hash of a given value.

    If the value is not a string, it will be converted to a JSON string representation before hashing.

    Args:
        val (Any): The value to calculate the hash for.

    Returns:
        str: The MD5 hash of the value.
    """

    if not isinstance(val, str):
        val = json.dumps(val)

    hex_string = hashlib.md5(val.encode()).hexdigest()
    return hex_string


# ....................... #


def hex_uuid4_from_string(val: str) -> str:
    """
    Converts a string value to a UUIDv4 and returns its hexadecimal representation.

    Args:
        val (str): The string value to convert to a UUIDv4.

    Returns:
        str: The hexadecimal representation of the UUIDv4.
    """

    return UUID(hex=hash_from_any(val), version=4).hex


# ....................... #


def hex_uuid4(val: Optional[str] = None) -> str:
    """
    Generate a hexadecimal representation of a UUID version 4.

    Args:
        val (str, optional): A string value to generate the UUID from. Defaults to None.

    Returns:
        str: A hexadecimal representation of the generated UUID.

    """

    return hex_uuid4_from_string(val) if val else uuid4().hex


# ....................... #


def cast_types(value: Any) -> Any:
    """
    Recursively convert all ints to floats in nested structures.
    """

    if isinstance(value, int):
        return float(value)

    elif isinstance(value, list):
        return [cast_types(item) for item in value]

    elif isinstance(value, tuple):
        return tuple(cast_types(item) for item in value)

    elif isinstance(value, dict):
        return {k: cast_types(v) for k, v in value.items()}

    else:
        return value


# ....................... #


def dict_hash_difference(source: dict, target: dict) -> dict:
    """
    Calculate the difference between two dictionaries based on target keys.

    Args:
        source (dict): The source dictionary.
        target (dict): The target dictionary.

    Returns:
        dict: The difference between the two dictionaries.
    """

    source = cast_types(deepcopy(source))
    target = cast_types(deepcopy(target))

    diff = {}

    for k, v in target.items():
        if k in source and hash_from_any(source[k]) != hash_from_any(v):
            diff[k] = v

    return diff


# ....................... #


def dict_direct_difference(source: dict, target: dict) -> dict:
    """
    Calculate the difference between two dictionaries based on target keys.

    Args:
        source (dict): The source dictionary.
        target (dict): The target dictionary.
    """

    diff = {}

    for k, v in target.items():
        if k in source and source[k] != v:
            diff[k] = v

    return diff
