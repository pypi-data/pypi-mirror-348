import typing
import os
import json
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class PathCache:
    VALUE_TYPE = typing.NamedTuple(
        "Value",
        [
            ("value", typing.Any),
            ("mtime", float),
            ("method", typing.Callable[[str], typing.Any]),
        ],
    )
    _cache: dict[str, VALUE_TYPE] = {}
    _customLoads: dict[str, typing.Callable[[str], typing.Any]] = {}

    @classmethod
    def register(cls, path: str | None = None):
        """Decorator to register a function as a custom loader.

        Usage:
            @PathCache.register("config.json")
            def load_config(path: str):
                return json.load(open(path))
        """

        def decorator(func: Callable[[str], Any]):
            nonlocal path
            if path is None:
                # If no path provided, use function name
                path = func.__name__
            cls._customLoads[path] = func
            return func

        return decorator

    @classmethod
    def defaultLoad(cls, path: str, method: str | None = None):
        if method == "plain":
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        elif method == "json":
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        elif path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        elif method is None:
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()

            if data.startswith("{") and data.endswith("}"):
                return json.loads(data)
            elif data.startswith("[") and data.endswith("]"):
                return json.loads(data)
            else:
                return data

        else:
            raise ValueError(f"Invalid method: {method}")

    @classmethod
    def getContents(cls, path: str, method: str | None = None) -> typing.Any:
        assert os.path.exists(path), f"Path {path} does not exist"
        assert os.path.isfile(path), f"Path {path} is not a file"

        path = os.path.abspath(path)
        cached = cls._cache.get(path)
        if cached is not None and cached.mtime == os.path.getmtime(path):
            return cached.value

        if method in cls._customLoads:
            value = cls._customLoads[method](path)
        else:
            value = cls.defaultLoad(path, method)

        cls._cache[path] = cls.VALUE_TYPE(value, os.path.getmtime(path), method)
        return value

    @classmethod
    def clear(cls, path: str | None = None) -> None:
        """Clear cache for a specific path or all paths."""
        if path:
            cls._cache.pop(path, None)
        else:
            cls._cache.clear()


class MtimeProp:
    """
    A caching mechanism that only tracks file modification times.
    Primary usage is as a property decorator that automatically tracks file changes.

    Basic usage:
        # As a property decorator (primary usage)
        class MyClass:
            @MtimeProp("config.json")
            def config(self):
                # Your code here - MtimeProp only tracks if file changed
                return load_config()

        # The property will automatically:
        # 1. Check file mtime on each access
        # 2. Re-run the method if file changed

        # Can also be used as a descriptor
        class MyClass:
            path = "config.json"
            data = MtimeProp("path")  # Uses instance's path attribute

        # Or with direct path
        class MyClass:
            data = MtimeProp("config.json")  # Uses direct path
    """

    def __init__(self, path: str):
        """Initialize as a descriptor with a path."""
        self.path = path
        self._func = None

    def __call__(self, func: Callable[[], Any]) -> "MtimeProp":
        """Property decorator - register the function as a generator."""
        self._func = func
        return self

    def _evaluate_path(self, obj: Any) -> str:
        """Evaluate path string, resolving any variable references."""
        try:
            # First check if path is an instance attribute
            if hasattr(obj, self.path):
                return getattr(obj, self.path)

            # If path contains no dots or exists as is, return it
            if "." not in self.path or os.path.exists(self.path):
                return self.path

            # Split path and evaluate first part if it contains dots
            parts = self.path.split("/")
            first_part = parts[0]

            if "." in first_part:
                # Build evaluation string for variable reference
                var_parts = first_part.split(".")
                eval_str = "obj." + ".".join(var_parts)
                first_part = str(eval(eval_str))

            # Reconstruct path
            return os.path.join(first_part, *parts[1:])

        except Exception as e:
            raise ValueError(f"Could not evaluate path '{self.path}': {e}")

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        """Descriptor protocol - check if file has changed."""
        if obj is None:
            return self

        # Evaluate path if it contains variable references
        actual_path = self._evaluate_path(obj)

        # If used as property decorator
        if self._func is not None:
            # Check if file has changed
            try:
                current_mtime = os.path.getmtime(actual_path)
                cached = PathCache._cache.get(actual_path)

                # If no cache or mtime changed, run the function
                if cached is None or cached.mtime != current_mtime:
                    value = self._func(obj)
                    PathCache._cache[actual_path] = PathCache.VALUE_TYPE(
                        value, current_mtime, None
                    )
                    return value

                # Return cached value
                return cached.value

            except OSError:
                # If file doesn't exist, just run the function
                return self._func(obj)

        # If used as descriptor, just check if file exists
        assert os.path.exists(actual_path), f"Path {actual_path} does not exist"
        return actual_path

    @classmethod
    def get(cls, path: str) -> str:
        """Get the path if it exists."""
        assert os.path.exists(path), f"Path {path} does not exist"
        return path

    @classmethod
    def clear(cls, path: str | None = None) -> None:
        """Clear cache for a specific path or all paths."""
        PathCache.clear(path)
