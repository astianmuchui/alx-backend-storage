#!/usr/bin/env python3
"""
Exercise
"""

import redis
import uuid
from typing import Union, Callable, Optional, List
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Count calls decorator
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Call history decorator
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        self._redis.rpush(key, str(args))
        return method(self, *args, **kwargs)

    return wrapper


def decode_utf8(data: bytes) -> str:
    """
    Decode utf-8
    """
    return data.decode('utf-8')


class Cache:
    """
    Cache class
    """

    def __init__(self):
        """
        Constructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get_int(self, key: str) -> int:
        """
        Get int from redis
        """
        return int(self.get(key))

    def get_str(self, key: str) -> str:
        """
        Get string from redis
        """
        return self.get(key)

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Union[str, bytes, int, float]:
        """
        Get data from redis
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data
