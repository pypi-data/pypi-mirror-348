import json
from typing import Any, Literal, Optional

from typing_extensions import NotRequired, TypedDict

from ormy.exceptions import InternalError

# ----------------------- #

VERTEX_DIRECTION = Literal["in", "out", "any"]
CONDITIONAL = list[str | list[str]]
DOC_CLAUSE = "doc"
VERTEX_CLAUSE = "v"
EDGE_CLAUSE = "e"
PATH_CLAUSE = "p"

# ....................... #


class CollectionIteratorParameters(TypedDict):
    """
    Collection iterator specification

    Attributes:
        doc_clause (str, optional): Document clause
    """

    doc_clause: NotRequired[str]


# ....................... #


class GraphIteratorParameters(TypedDict):
    """
    Graph iterator specification

    Attributes:
        start_vertex (str): Start vertex
        vertex_clause (str, optional): Vertex clause
        edge_clause (str, optional): Edge clause
        path_clause (str, optional): Path clause
        direction (str, optional): Direction of the query
        min_depth (int, optional): Minimum depth
        max_depth (int, optional): Maximum depth
    """

    start_vertex: str
    vertex_clause: NotRequired[str]
    edge_clause: NotRequired[str]
    path_clause: NotRequired[str]
    direction: NotRequired[VERTEX_DIRECTION]
    min_depth: NotRequired[int]
    max_depth: NotRequired[int]


# ....................... #

_col_iterator_defaults: CollectionIteratorParameters = {
    "doc_clause": DOC_CLAUSE,
}

_graph_iterator_defaults: GraphIteratorParameters = {
    "start_vertex": "__dummy__",
    "vertex_clause": VERTEX_CLAUSE,
    "edge_clause": EDGE_CLAUSE,
    "path_clause": PATH_CLAUSE,
    "direction": "any",
    "min_depth": 1,
    "max_depth": 1,
}

# ....................... #


class CollectionQueryParameters(TypedDict, total=False):
    """
    Collection query specification

    Attributes:
        filters (list[str | list[str]], optional): Filter expressions to apply to the query. Defaults to None
        limit (int, optional): Limit the number of results. Defaults to None
        offset (int, optional): Offset the results. Defaults to None
        sort (list[str], optional): Sort the results. Defaults to None
        return_clause (str, optional): Return clause. Defaults to None
        options (dict[str, Any], optional): Options to pass to the query. Defaults to None
    """

    filters: Optional[CONDITIONAL]
    limit: Optional[int]
    offset: Optional[int]
    sort: Optional[list[str]]
    return_clause: Optional[str]
    options: Optional[dict[str, Any]]


# ....................... #


class GraphQueryParameters(TypedDict, total=False):
    """
    Graph query specification

    Attributes:
        filters (list[str | list[str]], optional): Filter expressions to apply to the query. Defaults to None
        prunes (list[str | list[str]], optional): Prune expressions to apply to the query. Defaults to None
        limit (int, optional): Limit the number of results. Defaults to None
        offset (int, optional): Offset the results. Defaults to None
        sort (list[str], optional): Sort the results. Defaults to None
        return_clause (str, optional): Return clause. Defaults to None
        options (dict[str, Any], optional): Options to pass to the query. Defaults to None
    """

    filters: Optional[CONDITIONAL]
    prunes: Optional[CONDITIONAL]
    limit: Optional[int]
    offset: Optional[int]
    sort: Optional[list[str]]
    return_clause: Optional[str]
    options: Optional[dict[str, Any]]


# ....................... #


class ArangoQueryBuilder:
    """
    ArangoDB query builder
    """

    @staticmethod
    def _build_conditional_expression(exs: CONDITIONAL) -> str:
        """
        Build a conditional expression

        Args:
            exs (list[str | list[str]]): List of expressions

        Returns:
            expr (str): Conditional expression

        """

        inner = []

        for e in exs:
            if isinstance(e, list):
                inner.append(" OR ".join(e))

            else:
                inner.append(e)

        return " AND ".join(inner)

    # ....................... #

    @classmethod
    def _build_filters(cls, filters: Optional[CONDITIONAL] = None):
        """
        Build a filter expression

        Args:
            filters (list[str | list[str]], optional): Filter expressions to apply to the query. Defaults to None

        Returns:
            filter (str): Filter expression
        """

        if filters is None or not filters:
            return ""

        return "FILTER " + cls._build_conditional_expression(filters)

    # ....................... #

    @classmethod
    def _build_prunes(cls, prunes: Optional[CONDITIONAL] = None):
        """
        Build a prune expression

        Args:
            prunes (list[str | list[str]], optional): Prune expressions to apply to the query. Defaults to None

        Returns:
            prune (str): Prune expression
        """

        if prunes is None or not prunes:
            return ""

        return "PRUNE " + cls._build_conditional_expression(prunes)

    # ....................... #

    @staticmethod
    def _build_return(fallback: str, return_clause: Optional[str] = None):
        """
        Build a return expression

        Args:
            fallback (str): Fallback return clause
            return_clause (str, optional): Return clause. Defaults to None

        Returns:
            res (str): Return expression
        """

        if return_clause is None:
            return_clause = fallback

        return f"RETURN {return_clause}"

    # ....................... #

    @staticmethod
    def _build_options(options: Optional[dict[str, Any]] = None):
        """
        Build an options expression

        Args:
            options (dict[str, Any], optional): Options to pass to the query. Defaults to None

        Returns:
            res (str): Options expression
        """

        if options is None or not options:
            return ""

        return "OPTIONS " + json.dumps(options)

    # ....................... #

    @staticmethod
    def _build_sort(sort: Optional[list[str]] = None):
        """
        Build a sort expression

        Args:
            sort (list[str], optional): Sort expressions to apply to the query. Defaults to None

        Returns:
            res (str): Sort expression
        """

        if sort is None or not sort:
            return ""

        return "SORT " + ", ".join(sort)

    # ....................... #

    @staticmethod
    def _build_limit(limit: Optional[int] = None, offset: Optional[int] = None):
        """
        Build a limit expression

        Args:
            limit (int, optional): Limit the number of results. Defaults to None
            offset (int, optional): Offset the results. Defaults to None

        Returns:
            res (str): Limit expression
        """

        if limit is None and offset is None:
            return ""

        elif limit is None:
            raise InternalError("Limit must be provided when offset is provided")

        elif offset is None:
            return f"LIMIT {limit}"

        else:
            return f"LIMIT {offset}, {limit}"

    # ....................... #

    @staticmethod
    def _build_collection_iterator(
        collection: str,
        spec: CollectionIteratorParameters,
    ):
        """
        Build a collection iterator expression

        Args:
            spec (CollectionIterator): Collection iterator specification
        """

        _spec: CollectionIteratorParameters = {**_col_iterator_defaults, **spec}

        return _spec, f"FOR {_spec['doc_clause']} IN {collection}"

    # ....................... #

    @staticmethod
    def _build_graph_iterator(
        graph: str,
        spec: GraphIteratorParameters,
    ):
        """
        Build a graph iterator expression

        Args:
            spec (GraphIterator): Graph iterator specification

        Returns:
            res (str): Graph iterator expression
        """

        _spec: GraphIteratorParameters = {**_graph_iterator_defaults, **spec}

        if _spec["max_depth"] < _spec["min_depth"]:
            raise InternalError("Max depth must be greater or equal to min depth")

        match _spec["direction"]:
            case "in":
                _t = "INBOUND"
            case "out":
                _t = "OUTBOUND"
            case "any":
                _t = "ANY"

        start_vertex = _spec["start_vertex"]

        _d = f'{_t} "{start_vertex}"'
        _v = _spec["vertex_clause"]
        _e = _spec["edge_clause"]
        _p = _spec["path_clause"]
        _g = f'GRAPH "{graph}"'

        return (
            _spec,
            f"FOR {_v}, {_e}, {_p} IN {_spec['min_depth']}..{_spec['max_depth']} {_d} {_g}",
        )

    # ....................... #

    @staticmethod
    def build_projection_expression(fields: list[str], doc_clause: str = DOC_CLAUSE):
        """
        Build a projection expression

        Args:
            fields (list[str]): Fields to project
            doc_clause (str, optional): Document clause. Defaults to "doc"

        Returns:
            clause (str): Projection expression
        """

        clause = (
            "{"
            + ", ".join(
                [
                    f"{f}: HAS({doc_clause}, '{f}') ? {doc_clause}.{f} : null"
                    for f in fields
                ]
            )
            + "}"
        )

        return clause

    # ....................... #

    @classmethod
    def build_collection_query(
        cls,
        collection: str,
        iterator: CollectionIteratorParameters,
        parameters: CollectionQueryParameters,
    ):
        """
        Build a collection query for ArangoDB

        Args:
            collection (str): Collection to iterate over
            iterator (CollectionIteratorParameters): Collection iterator specification
            parameters (CollectionQueryParameters): Collection query parameters

        Returns:
            q (str): Collection query
        """

        _spec, _iterator = cls._build_collection_iterator(collection, iterator)

        _filter = cls._build_filters(parameters.get("filters", None))
        _return = cls._build_return(
            _spec["doc_clause"],
            parameters.get("return_clause", None),
        )
        _opts = cls._build_options(parameters.get("options", None))
        _sort = cls._build_sort(parameters.get("sort", None))
        _limit = cls._build_limit(
            parameters.get("limit", None),
            parameters.get("offset", None),
        )

        q = f"""
            {_iterator}
            {_filter}
            {_opts}
            {_sort}
            {_limit}
            {_return}
        """

        return q

    # ....................... #

    @classmethod
    def build_graph_query(
        cls,
        graph: str,
        iterator: GraphIteratorParameters,
        parameters: GraphQueryParameters,
    ):
        """
        Build a graph query for ArangoDB

        Args:
            graph (str): Graph to iterate over
            iterator (GraphIteratorParameters): Graph iterator specification
            parameters (GraphQueryParameters): Graph query parameters

        Returns:
            q (str): AQL query to execute
        """

        _spec, _iterator = cls._build_graph_iterator(
            graph,
            iterator,
        )
        _fallback = (
            "{"
            + f"""
            v: {_spec["vertex_clause"]},
            e: {_spec["edge_clause"]},
            p: {_spec["path_clause"]}
        """
            + "}"
        )

        _filter = cls._build_filters(parameters.get("filters", None))
        _prune = cls._build_prunes(parameters.get("prunes", None))
        _return = cls._build_return(
            _fallback,
            parameters.get("return_clause", None),
        )
        _opts = cls._build_options(parameters.get("options", None))
        _sort = cls._build_sort(parameters.get("sort", None))
        _limit = cls._build_limit(
            parameters.get("limit", None),
            parameters.get("offset", None),
        )

        q = f"""
            {_iterator}
                {_prune}
                {_opts}
                {_filter}
                {_sort}
                {_limit}
                {_return}
            """

        return q
