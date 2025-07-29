from typing import Any, Awaitable, Callable, ParamSpec, TypeVar

from pydantic import BaseModel

# ----------------------- #

P = ParamSpec("P")
R = TypeVar("R")

AsyncCallable = Callable[P, Awaitable[R]]
AbstractData = BaseModel | dict[str, Any]

# ----------------------- #

__all__ = ["AsyncCallable", "AbstractData"]
