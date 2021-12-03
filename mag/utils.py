# -*- coding: UTF-8 -*-
""""
Created on 11/11/2021
Utils for core.

:author:     Martin Dočekal
"""
from bisect import bisect_left
from typing import Optional, Sequence


def bin_search(s: Sequence[float], x: float) -> Optional[int]:
    """
    Returns index of searched value or None if nothing was found.

    :param s: sorted sequence
    :param x: the value that should be searched
    :return: index of searched value in sequence or None when nothing was found.
    """

    pos = bisect_left(s, x)
    if pos < len(s) and s[pos] == x:
        return pos

    return None
