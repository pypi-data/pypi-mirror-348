from typing import Dict, List, Optional, Set, Tuple, Union


def ensure_list(s: Optional[Union[str, List[str], Tuple[str], Set[str]]]) -> List[str]:
    """

    :param s:
    :return:
    """
    result_ = []
    if isinstance(s, (list, tuple)):
        for s_ in s:
            if isinstance(s_, str):
                result_.append(s_)
            elif isinstance(s_, tuple):
                result_.extend([s__ for s__ in s_])
            elif isinstance(s_, list):
                result_.extend(s_)
    return result_


def check_values_in_list(source_value, allowed_values):
    """
    return True is all items in source_value are present in allowed_values

    :param source_value:
    :param allowed_values:
    :return: True | False
    """
    if not allowed_values:
        return True

    # log.debug("Checking for '{}' in {}", source_value, allowed_values)
    source_value = ensure_list(source_value)
    if all(val in allowed_values for val in source_value):
        return True
    return False


def merge_dict(original: Dict, to_add: Dict) -> None:
    """Merge a new map of configuration recursively with an older one."""
    for k, v in to_add.items():
        if isinstance(v, dict) and k in original and isinstance(original[k], dict):
            merge_dict(original[k], v)
        elif isinstance(v, list) and k in original and isinstance(original[k], list):
            original[k].extend(v)
        else:
            original[k] = v
