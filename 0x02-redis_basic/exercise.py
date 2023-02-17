#!/usr/bin/env python3
"""This creates a Cache class"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """This counts how many times a method is called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """returns a wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """This stores the history of inputs and outputs for a
    particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """this wraps the decorated function and returns a wrapper"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper

def replay(fn: Callable):
    '''This displays the history of calls to a function'''
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode('utf-8'))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode('utf-8')
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    """This stores an instance of the Redis client as private variable"""
    def __init__(self):
        """initializes the class"""
        self._redis = redis.Redis()
        self._redis.flushdb

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """This stores a data in the redis database"""
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn=None) -> Union[str, bytes, int, float]:
        """This get a data with the key - key, and convert the
        data into its original type"""
        data = self._redis.get(key)
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """This convert the bytes data into a string"""
        data = self._redis.get(key)
        return str(data.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """This converts the bytes data into an int"""
        data = self._redis.get(key)
        return int(data.decode('utf-8'))


if __name__ == '__main__':
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(123)
    replay(cache.store)
