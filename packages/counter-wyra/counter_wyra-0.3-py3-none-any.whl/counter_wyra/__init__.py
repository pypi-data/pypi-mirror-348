"""A random Counter thing I made for no reason at all"""
# Copyright (C) Arnay Kumar
# This project is under the WTFPL License.
from typing import Any, Union


class Counter:
    """A class that implements a counter with various arithmetic operations."""
    def __init__(self, count: int = None) -> None:
        if count:
            self.count = count
        else:
            self.count = 0

    def increment(self, count: int = None) -> None:
        """
        Increments the src by one or whatever count is.

        :param count:
        :return:
        """
        try:
            if count:
                self.count += count
            else:
                self.count += 1
        except TypeError as exc:
            raise TypeError("Incorrect type") from exc

    def decrement(self, count: int = None) -> None:
        """
        Decrements the src by one or whatever count is.

        :param count:
        :return:
        """
        if count:
            self.count -= count
        else:
            self.count -= 1

    def __str__(self) -> str:
        return str(self.count)

    def __int__(self) -> int:
        return int(self.count)

    def __sub__(self, other) -> Union[float, Any]:
        if isinstance(other, int):
            return self.count - other
        if isinstance(other, Counter):
            return self.count - other.count
        raise TypeError('Can only add integers or Counter objects')

    def __add__(self, other) -> Union[float, Any]:
        if isinstance(other, int):
            return self.count + other
        if isinstance(other, Counter):
            return self.count + other.count
        raise TypeError('Can only add integers or Counter objects')

    def __repr__(self) -> str:
        return str(f"Counter({self.count})")

    def __truediv__(self, other) -> Union[float, Any]:
        try:
            if isinstance(other, int):
                return self.count / other
            if isinstance(other, Counter):
                return self.count / other.count
            raise TypeError('Can only divide integers or Counter objects')
        except ZeroDivisionError:
            return "It is not possible to divide by zero"

    def __floordiv__(self, other) -> Union[float, Any]:
        try:
            if isinstance(other, int):
                return self.count // other
            if isinstance(other, Counter):
                return self.count // other.count
            raise TypeError('Can only floor divide integers or Counter objects')
        except ZeroDivisionError:
            return "It is not possible to floor divide by zero"

    def __mod__(self, other) -> Union[float, Any]:
        try:
            if isinstance(other, int):
                return self.count % other
            if isinstance(other, Counter):
                return self.count % other.count
            raise TypeError('Can only Divide integers or Counter objects')
        except ZeroDivisionError:
            return "It is not possible to divide by zero"
