from typing import Any, Callable, Optional, Protocol, Set
from functools import wraps
from django.core.cache import cache as django_cache
from general_manager.cache.cacheTracker import DependencyTracker
from general_manager.cache.dependencyIndex import record_dependencies, Dependency
from general_manager.cache.modelDependencyCollector import ModelDependencyCollector
from general_manager.auxiliary.makeCacheKey import make_cache_key


class CacheBackend(Protocol):
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None: ...


RecordFn = Callable[[str, Set[Dependency]], None]


def cached(
    timeout: Optional[int] = None,
    cache_backend: CacheBackend = django_cache,
    record_fn: RecordFn = record_dependencies,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = make_cache_key(func, args, kwargs)

            result = cache_backend.get(key)
            if result is not None:
                return result

            with DependencyTracker() as dependencies:
                result = func(*args, **kwargs)
                ModelDependencyCollector.addArgs(dependencies, args, kwargs)

            cache_backend.set(key, result, timeout)

            if dependencies and timeout is None:
                record_fn(key, dependencies)

            return result

        return wrapper

    return decorator
