from typing import Any, Callable, Dict, Iterable, TypeVar


def get_meta(instance: Any) -> Dict[str, Any]:
    """
    Returns object pjrpc metadata.
    """

    return getattr(instance, '__pjrpc_meta__', {})


def set_meta(instance: Any, **meta: Any) -> Dict[str, Any]:
    """
    Updates object pjrpc metadata.
    """

    if not hasattr(instance, '__pjrpc_meta__'):
        instance.__pjrpc_meta__ = {}

    instance.__pjrpc_meta__.update(meta)

    return instance.__pjrpc_meta__


def remove_prefix(s: str, prefix: str) -> str:
    """
    Removes a prefix from a string.

    :param s: string to be processed
    :param prefix: prefix to be removed
    :return: processed string
    """

    if s.startswith(prefix):
        return s[len(prefix):]
    else:
        return s


def remove_suffix(s: str, suffix: str) -> str:
    """
    Removes a suffix from a string.

    :param s: string to be processed
    :param suffix: suffix to be removed
    :return: processed string
    """

    if suffix and s.endswith(suffix):
        return s[0:-len(suffix)]
    else:
        return s


def join_path(path: str, *paths: str) -> str:
    result = path
    for path in paths:
        if path:
            result = f'{result.rstrip("/")}/{path.lstrip("/")}'

    return result


T = TypeVar('T')
K = TypeVar('K')


def unique(*iterables: Iterable[T], key: Callable[[T], K]) -> Iterable[T]:
    items_map: Dict[K, T] = {}
    for iterable in iterables:
        for item in iterable:
            items_map[key(item)] = item

    return items_map.values()
