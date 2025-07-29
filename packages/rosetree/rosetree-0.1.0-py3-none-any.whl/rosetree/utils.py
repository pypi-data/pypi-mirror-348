from collections.abc import Iterable
from itertools import accumulate, chain
from typing import Hashable, Mapping, TypeVar


K = TypeVar('K', bound=Hashable)
V = TypeVar('V')


def merge_dicts(d1: Mapping[K, V], d2: Mapping[K, V]) -> dict[K, V]:
    """Merges two dictionaries together, raising a KeyError if any key appears in both dictionaries."""
    common_keys = set(d1) & set(d2)
    if common_keys:
        raise KeyError(f'Duplicate keys found: {common_keys}')
    # Merge the dictionaries
    return {**d1, **d2}

def cumsums(xs: Iterable[float]) -> list[float]:
    """Computes cumulative sums of a sequence of numbers, starting with 0."""
    return list(accumulate(chain([0.0], xs)))
