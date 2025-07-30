"""
Environment variable decorator module.
"""

from inspect import _empty, signature
from os import getenv
from typing import (
    Any,
    Callable,
    Generic,
    TypeVar,
    get_args,
    get_origin,
    cast,
    overload,
    Union,
)
import types
import sys


T = TypeVar("T")


class env(Generic[T]):  # noqa: N801
    def __init__(
        self,
        var_name: str,
        *,
        default: T | None = None,
        parser: Callable[[str], T] | None = None,
    ):
        """
        Initialize the env descriptor.

        Args:
            var_name: The name of the environment variable
            default: The default value if the environment variable is not set
            parser: A function to parse the string value to the desired type

        Note:
            Requiredness is inferred from the type annotation:
            - If the type is Optional[T], Union[T, None], or T | None, it's not required
            - If a default value is provided, it's not required
            - Otherwise, it's required
        """
        self.var_name = var_name
        self.func: Callable[..., Any] | None = None
        self.parser = parser
        self._var_type = None  # The original type annotation (for optionality checks)
        self._unwrapped_type = None  # The unwrapped type (for conversion)
        self.default = default

    def __set_name__(self, owner, name):
        from os import getenv

        self.name = name

        # Determine the variable type if not already done
        if self._var_type is None:
            self._var_type, self._unwrapped_type = self._determine_var_type()

        # Check if this is a required environment variable
        if not self._is_optional_type(self._var_type) and self.default is None:
            # Get the prefix from the owner class
            prefix = getattr(owner, "prefix", "")
            env_var_name = prefix + self.var_name

            # Check if the environment variable exists
            if getenv(env_var_name) is None:
                msg = f"Environment variable '{env_var_name}' is required but not set"
                raise RuntimeError(msg)

    @overload
    def __get__(self, instance: None, owner: type[Any] | None = None) -> T: ...

    @overload
    def __get__(self, instance: object, owner: type[Any] | None = None) -> T: ...

    def __get__(self, instance: object | None, owner: type[Any] | None = None) -> T:
        if self.func is None:
            msg = (
                "The env class must be used as a decorator: @env('VAR_NAME') "
                "or with a type parameter: @env[type]('VAR_NAME'). "
                "Please refer to the documentation for correct usage."
            )
            raise AttributeError(msg)

        # Get the prefix from the owner class
        prefix = getattr(owner, "prefix", "")
        env_var_name = prefix + self.var_name

        # Determine the target type if not already cached
        if self._var_type is None:
            self._var_type, self._unwrapped_type = self._determine_var_type()

        # Determine if the environment variable is required based on type and default
        # If type is Optional or Union with None, it's not required
        if self._is_optional_type(self._var_type):
            is_required = False
        # For edge cases: if we're using a non-optional type with default=None,
        # we should treat it as not required (this is for backward compatibility)
        # If any default value is provided, it's not required
        elif self.default is not None:
            is_required = False
        # Otherwise, it's required
        else:
            is_required = True

        env_var_value = getenv(env_var_name, default=self.default)
        if env_var_value is None and is_required:
            msg = f"Environment variable '{env_var_name}' is required"
            raise ValueError(msg)

        if env_var_value is None:
            value = env_var_value
        elif self.parser is not None:
            value = self.parser(env_var_value)
        else:
            # Use the unwrapped type for conversion, not the original type
            # This allows Optional[int] to use int for conversion
            value = self._unwrapped_type(env_var_value)

        return cast(T, value)

    def __call__(self, func: Callable[..., Any]):
        self.func = func
        return self

    # Caching functionality has been removed

    def _determine_var_type(self) -> tuple[Any, Any]:
        """Determine the target type in priority order:
        1. Explicit generic parameter via __orig_class__ (env[Path])
        2. Return type annotation of the decorated function
        3. Fallback to str

        For Optional[X] and Union[X, None] types, extracts X for unwrapped_type.

        Returns:
            A tuple of (original_type, unwrapped_type) where:
            - original_type: The original type annotation (used for optionality checks)
            - unwrapped_type: The unwrapped type (used for conversion)
        """
        # First determine the type from generic parameter or function annotation
        orig = getattr(self, "__orig_class__", None)
        if orig is not None:
            args = get_args(orig)
            if args:
                type_hint = args[0]
            else:
                return str, str
        else:
            if self.func is None:
                msg = (
                    "The env class must be used as a decorator: @env('VAR_NAME') "
                    "or with a type parameter: @env[type]('VAR_NAME'). "
                    "Please refer to the documentation for correct usage."
                )
                raise RuntimeError(msg)

            ret_type = signature(self.func).return_annotation
            type_hint = ret_type if ret_type != _empty else str

        # Keep the original type for optionality checks
        original_type = type_hint
        unwrapped_type = type_hint

        # Extract the actual type for conversions
        origin = get_origin(type_hint)
        args = get_args(type_hint)

        if origin is Union and type(None) in args:
            # For Union[X, None] or Optional[X], get the non-None type
            non_none_args = [arg for arg in args if arg is not type(None)]
            if len(non_none_args) == 1:
                unwrapped_type = non_none_args[0]

        # Handle Python 3.10+ syntax: X | None
        elif sys.version_info >= (3, 10) and isinstance(type_hint, types.UnionType):
            args = get_args(type_hint)
            if type(None) in args:
                non_none_args = [arg for arg in args if arg is not type(None)]
                if len(non_none_args) == 1:
                    unwrapped_type = non_none_args[0]

        return original_type, unwrapped_type

    @staticmethod
    def _is_optional_type(type_hint: Any) -> bool:
        """Check if a type hint is Optional[T], Union[T, None], or T | None.

        Args:
            type_hint: The type hint to check

        Returns:
            True if the type is optional, False otherwise
        """
        # Handle Union[T, None], Optional[T], or T | None
        origin = get_origin(type_hint)
        args = get_args(type_hint)
        if origin is Union:
            return type(None) in args
        if sys.version_info >= (3, 10) and isinstance(type_hint, types.UnionType):
            return type(None) in get_args(type_hint)
        return False
