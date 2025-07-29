import re
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Annotated, Any, Literal, Optional, cast

from pydantic import BaseModel, Field
from typing_extensions import NotRequired, TypedDict

from ormy.base.decorator import json_schema_modifier, remove_description
from ormy.base.generic import TabularData
from ormy.base.pydantic import TableResponse
from ormy.exceptions import InternalError

# ----------------------- #


@json_schema_modifier(remove_description)
class SortOrder(StrEnum):
    """
    Order of the sort

    Attributes:
        asc (str): Ascending Order
        desc (str): Descending Order
    """

    asc = "asc"
    desc = "desc"


# ....................... #


@json_schema_modifier(remove_description)
class SortField(BaseModel):
    """
    Sort field model

    Attributes:
        key (str): Key of the field
        default (bool): Whether the Field is the default sort field
    """

    key: str
    default: bool = False


# ----------------------- #
# TODO: add filter operators (mb use a separate uniform interface)


class FilterABC(ABC, BaseModel):
    """
    Abstract Base Class for Search Filters

    Attributes:
        key (str): Key of the filter
        value (Any, optional): The filter value
        type (str): The filter type
    """

    key: str
    value: Optional[Any] = None
    type: str = "abc"
    negated: bool = False

    # ....................... #

    @abstractmethod
    def build(self) -> Optional[str]: ...


# ....................... #


@json_schema_modifier(remove_description)
class RawFilter(FilterABC):
    """
    Raw filter

    Attributes:
        key (str): Key of the filter (not used)
        value (str): The filter value
    """

    key: str = "raw"
    value: str | list[str]
    type: Literal["raw"] = "raw"

    # ....................... #

    @staticmethod
    def _prepare_str(x: str):
        return re.sub(r"\s+", " ", x).strip()

    # ....................... #

    def build(self):
        if isinstance(self.value, str):
            value = self._prepare_str(self.value)

        else:
            value = [self._prepare_str(x) for x in self.value]

        return value


# ....................... #


class RawFilterDict(TypedDict):
    key: NotRequired[str]
    value: str | list[str | list[str]]
    type: Literal["raw"]
    negated: NotRequired[bool]


# ....................... #


@json_schema_modifier(remove_description)
class BooleanFilter(FilterABC):
    """
    Boolean filter

    Attributes:
        key (str): Key of the filter
        value (bool): The filter value
    """

    value: Optional[bool] = None
    type: Literal["boolean"] = "boolean"

    # ....................... #

    def build(self):
        if self.value is not None:
            return f"{self.key} = {str(self.value).lower()}"

        return None


# ....................... #


class BooleanFilterDict(TypedDict):
    key: str
    value: NotRequired[bool]
    type: Literal["boolean"]
    negated: NotRequired[bool]


# ....................... #


@json_schema_modifier(remove_description)
class NumberFilter(FilterABC):
    """
    Numeric filter

    Attributes:
        key (str): Key of the filter
        value (Tuple[float | None, float | None]): The filter value
    """

    value: tuple[Optional[float], Optional[float]] = (None, None)
    type: Literal["number"] = "number"

    # ....................... #

    def build(self):
        low, high = self.value

        if low is None and high is not None:
            return f"{self.key} <= {high}"

        if low is not None and high is None:
            return f"{self.key} >= {low}"

        if low is not None and high is not None:
            return f"{self.key} {low} TO {high}"

        return None


# ....................... #


class NumberFilterDict(TypedDict):
    key: str
    value: NotRequired[tuple[Optional[float], Optional[float]]]
    type: Literal["number"]
    negated: NotRequired[bool]


# ....................... #


@json_schema_modifier(remove_description)
class DatetimeFilter(FilterABC):
    """
    Datetime filter

    Attributes:
        key (str): Key of the filter
        value (Tuple[int | None, int | None]): The filter value
    """

    value: tuple[Optional[int], Optional[int]] = (None, None)
    type: Literal["datetime"] = "datetime"

    # ....................... #

    def build(self):
        low, high = self.value

        if low is None and high is not None:
            return f"{self.key} <= {high}"

        if low is not None and high is None:
            return f"{self.key} >= {low}"

        if low is not None and high is not None:
            return f"{self.key} {low} TO {high}"

        return None


# ....................... #


class DatetimeFilterDict(TypedDict):
    key: str
    value: NotRequired[tuple[Optional[int], Optional[int]]]
    type: Literal["datetime"]
    negated: NotRequired[bool]


# ....................... #


@json_schema_modifier(remove_description)
class ArrayFilter(FilterABC):
    """
    Array filter

    Attributes:
        key (str): Key of the filter
        value (list[Any]): The filter value
    """

    value: list[Any] = []
    type: Literal["array"] = "array"

    # ....................... #

    def build(self):
        if self.negated:
            op = "NOT IN"

        else:
            op = "IN"

        if self.value:
            return f"{self.key} {op} {self.value}"

        return None


# ....................... #


class ArrayFilterDict(TypedDict):
    key: str
    value: NotRequired[list[Any]]
    type: Literal["array"]
    negated: NotRequired[bool]


# ....................... #

AnyFilter = Annotated[
    BooleanFilter | NumberFilter | DatetimeFilter | ArrayFilter | RawFilter,
    Field(discriminator="type"),
]

# ....................... #

AnyFilterDict = (
    BooleanFilterDict
    | NumberFilterDict
    | DatetimeFilterDict
    | ArrayFilterDict
    | RawFilterDict
)

# ----------------------- #


class SearchRequest(BaseModel):
    query: str = ""
    sort: Optional[str] = None
    order: SortOrder = SortOrder.desc
    filters: list[AnyFilter] = []


# ....................... #


class SearchRequestDict(TypedDict):
    query: str
    sort: NotRequired[str]
    order: NotRequired[SortOrder]
    filters: NotRequired[list[AnyFilterDict]]


# ----------------------- #


class SearchResponse(TableResponse):
    @classmethod
    def from_search_results(cls, res: Any, federated: bool = False):
        """Create a SearchResponse from a search results"""

        from meilisearch_python_sdk.models.search import (
            SearchResults,
            SearchResultsFederated,
        )

        # Type hints to supress mypy errors
        _res: SearchResults | SearchResultsFederated
        offset: int | None
        size: int | None
        count: int | None
        page: int | None

        if federated:
            _res = cast(SearchResultsFederated, res)
            offset = _res.offset
            size = _res.limit
            count = _res.estimated_total_hits or 0

            if offset is None or size is None:
                raise InternalError("Offset and size must be provided")

            else:
                page = offset // size + 1

        else:
            _res = cast(SearchResults, res)
            size = _res.hits_per_page
            page = _res.page
            count = _res.total_hits

            if size is None or page is None or count is None:
                raise InternalError("Size, page and count must be provided")

        if federated:
            for h in _res.hits:
                fed = h.pop("_federation")
                index_uid = fed["indexUid"]
                h["_index_uid"] = index_uid

        hits = TabularData(_res.hits)

        return cls(hits=hits, size=size, page=page, count=count)


# ....................... #


@json_schema_modifier(remove_description)
class MeilisearchReference(BaseModel):
    """
    Meilisearch reference model

    Attributes:
        sort (list[ormy.extension.meilisearch.schema.SortField]): The sort fields
        filters (list[ormy.extension.meilisearch.schema.AnyFilter]): The filters
    """

    sort: list[SortField] = []
    filters: list[AnyFilter] = []
