import typing
from typing import get_origin, get_args, Union, Optional


def check_typedict_vars(typedict: typing._TypedDict, data: dict):
    for key, value in typedict.__annotations__.items():
        if key not in data:
            raise ValueError(f"Key {key} not found in data")

        # Get the origin type (Optional, Union, etc.) and its arguments
        origin = get_origin(value)
        args = get_args(value)

        if origin is Optional:
            # For Optional, check if value is None or matches the inner type
            if data[key] is None:
                continue
            inner_type = args[0]
            if not isinstance(data[key], inner_type):
                raise ValueError(f"Key {key} is not of type {value}")
        elif origin is Union:
            # For Union, check if value matches any of the union types
            if not any(isinstance(data[key], t) for t in args):
                raise ValueError(f"Key {key} is not of any type in {value}")
        else:
            # Regular type check
            if not isinstance(data[key], value):
                raise ValueError(f"Key {key} is not of type {value}")
    return True
