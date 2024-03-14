#!/usr/bin/env python3
"""
Task 10
"""
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    safe first element
    """
    if lst:
        return lst[0]
    else:
        return None
