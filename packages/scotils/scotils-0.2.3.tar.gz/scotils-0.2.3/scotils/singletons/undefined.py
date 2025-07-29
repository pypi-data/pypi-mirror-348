"""Inspired by JavaScript's optional chaining. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining"""

from threading import Lock


class UndefinedType:
    """A singleton type that mimics None, evaluating to False and absorbing method calls."""

    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __bool__(self):
        """Evaluate to False"""
        return False

    def __str__(self):
        return "UndefinedType"

    def __getattr__(self, _):
        """Return self on any attempt to get an attribute"""

        def method(*args, **kwargs):
            return self

        return method

    def __getitem__(self, _) -> "UndefinedType":
        """Return self on any attempt to subscript UndefinedType"""
        return self

    def __call__(self, *args, **kwargs) -> "UndefinedType":
        """Return self on any attempt to call UndefinedType"""
        return self


Undefined = UndefinedType()


class UndefinedDict(dict):
    """A dictionary that return Undefined for any missing keys."""

    def __getitem__(self, key):
        # Return Undefined if key doesn't exist, otherwise return the value
        return self.get(key, Undefined)

    def __missing__(self, _):
        return Undefined

    def get(self, key, default=None):
        # Override get to return Undefined for missing keys unless a different default is provided
        return (
            super().get(key, Undefined)
            if default is None
            else super().get(key, default)
        )
