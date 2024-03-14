#!/usr/bin/env python3
"""
Task 9
"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    length of element
    """
    return [(i, len(i)) for i in lst]
