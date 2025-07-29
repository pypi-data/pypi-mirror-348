# (C) 2025 Fujitsu Limited

import re

from fujitsu_quantum.types import is_single_value

_snake_to_camel_pattern = re.compile(r'_([a-z])')


def snake_to_camel(snake_str: str) -> str:
    return _snake_to_camel_pattern.sub(lambda m: m.group(1).upper(), snake_str)


def snake_to_camel_keys(val: dict):
    if isinstance(val, dict):
        return {snake_to_camel(k): snake_to_camel_keys(v) for k, v in val.items()}
    else:
        return val


# From https://stackoverflow.com/a/1176023
_camel_to_snake_pattern = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')


def camel_to_snake(camel_str: str) -> str:
    return _camel_to_snake_pattern.sub('_', camel_str).lower()


def camel_to_snake_keys(val: dict):
    if isinstance(val, dict):
        return {camel_to_snake(k): camel_to_snake_keys(v) for k, v in val.items()}
    else:
        return val


def remove_none_values(dict_value: dict):
    return {k: v for k, v in dict_value.items() if v is not None}


def numpy_to_python_types(value):
    return getattr(value, "tolist", lambda: value)()


def operator_coef_numpy_to_python_types(operator):
    """Note that conversion is done in-place."""

    # To avoid unnecessary for-loops over many terms in the given operator (which may take long time),
    # perform the conversion only if the type of the first coefficient is a numpy type.
    if is_single_value('operator', operator):
        if hasattr(operator[0][1], 'tolist'):  # numpy objects have tolist()
            for i, term in enumerate(operator):
                operator[i] = (term[0], numpy_to_python_types(term[1]))
    else:
        if hasattr(operator[0][0][1], 'tolist'):
            for one_op in operator:
                for i, term in enumerate(one_op):
                    one_op[i] = (term[0], numpy_to_python_types(term[1]))


def find_duplicates(list_value: list) -> set:
    seen = set()
    duplicates = set()
    for item in list_value:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return duplicates
