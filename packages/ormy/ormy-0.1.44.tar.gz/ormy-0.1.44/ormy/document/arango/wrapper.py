from typing import Any, ClassVar, Literal, Optional, Self, Sequence, cast

from pydantic import BaseModel, Field

from ormy.exceptions import (
    BadRequest,
    Conflict,
    ModuleNotFound,
    NotFound,
)

try:
    from arango.client import ArangoClient
    from arango.cursor import Cursor
    from arango.database import StandardDatabase
except ImportError as e:
    raise ModuleNotFound(extra="arango", packages=["python-arango"]) from e

from ormy._abc import AbstractABC
from ormy._abc.registry import Registry
from ormy.base.generic import TabularData
from ormy.base.typing import AbstractData
from ormy.document._abc import SyncDocumentABC

from .builder import (
    CONDITIONAL,
    ArangoQueryBuilder,
    CollectionIteratorParameters,
    CollectionQueryParameters,
    GraphIteratorParameters,
    GraphQueryParameters,
)
from .config import ArangoConfig, ArangoGraphConfig

# ----------------------- #


def _execute_query(
    db: StandardDatabase,
    query: str,
    bind_vars: dict[str, Any] = {},
    batch_size: int = 1000,
    arango_kwargs: dict[str, Any] = {},
):
    """
    Execute a raw query against ArangoDB

    Args:
        db (StandardDatabase): ArangoDB database
        query (str): AQL query to execute
        bind_vars (dict[str, Any], optional): Bind variables
        batch_size (int, optional): Batch size. Defaults to 1000
        arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

    Returns:
        res (list[dict]): List of results
    """

    cursor = db.aql.execute(
        query=query,
        bind_vars=bind_vars,
        batch_size=batch_size,
        **arango_kwargs,
    )
    cursor = cast(Cursor, cursor)

    return list(cursor)


# ....................... #


class ArangoBase(SyncDocumentABC):
    """ArangoDB base class"""

    config: ClassVar[ArangoConfig] = ArangoConfig()
    _static: ClassVar[Optional[ArangoClient]] = None
    __discriminator__ = ["database", "collection"]

    # ....................... #

    @classmethod
    def _client(cls):
        """
        Get syncronous ArangoDB client

        Returns:
            client (arango.ArangoClient): Syncronous ArangoDB client
        """

        if cls._static is None:
            cls._static = ArangoClient(hosts=cls.config.url())

        return cls._static

    # ....................... #

    @classmethod
    def _get_database(cls):
        """
        Get assigned ArangoDB database

        Returns:
            database (arango.StandardDatabase): Assigned ArangoDB database
        """

        client = cls._client()
        username = cls.config.credentials.username.get_secret_value()
        password = cls.config.credentials.password.get_secret_value()
        database = cls.config.database

        sys_db = client.db(
            "_system",
            username=username,
            password=password,
        )

        if not sys_db.has_database(database):
            sys_db.create_database(database)

        db = client.db(
            database,
            username=username,
            password=password,
        )

        return db

    # ....................... #

    @classmethod
    def _get_collection(cls):
        """
        Get assigned ArangoDB collection

        Returns:
            collection (arango.StandardCollection): Assigned ArangoDB collection
        """

        collection = cls.config.collection
        db = cls._get_database()

        if not db.has_collection(collection):
            db.create_collection(collection)

        return db.collection(collection)

    # ....................... #

    @staticmethod
    def _serialize(doc: dict) -> dict:
        """
        Serialize a document

        Args:
            doc (dict): Document to serialize

        Returns:
            doc (dict): Serialized document
        """

        doc["_key"] = doc["id"]

        return doc

    # ....................... #

    @staticmethod
    def _deserialize(doc: dict) -> dict:
        """
        Deserialize a document

        Args:
            doc (dict): Document to deserialize

        Returns:
            doc (dict): Deserialized document
        """

        return doc

    # ....................... #

    @classmethod
    def _raw_query(
        cls,
        query: str,
        bind_vars: dict[str, Any] = {},
        batch_size: int = 1000,
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Execute a raw query against ArangoDB

        Args:
            query (str): AQL query to execute
            bind_vars (dict[str, Any], optional): Bind variables
            batch_size (int, optional): Batch size. Defaults to 1000
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (list[dict]): List of results
        """

        return _execute_query(
            db=cls._get_database(),
            query=query,
            bind_vars=bind_vars,
            batch_size=batch_size,
            arango_kwargs=arango_kwargs,
        )

    # ....................... #

    @classmethod
    def create(cls, data: Self, arango_kwargs: dict[str, Any] = {}):
        """
        Create a new document in the collection

        Args:
            data (Self): Data model to be created
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (Self): Created data model

        Raises:
            Conflict: Document already exists
        """

        collection = cls._get_collection()
        document = cls._serialize(data.model_dump())

        if collection.has(document["_key"]):
            raise Conflict("Document already exists")

        collection.insert(document, **arango_kwargs)

        return data

    # ....................... #

    def save(self: Self, arango_kwargs: dict[str, Any] = {}):
        """
        Save a document in the collection.
        Document will be updated if exists

        Args:
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            self (Self): Saved data model
        """

        collection = self._get_collection()
        document = self._serialize(self.model_dump())

        if collection.has(document["_key"]):
            collection.replace(
                document,
                silent=True,
                **arango_kwargs,
            )

        else:
            collection.insert(document, **arango_kwargs)

        return self

    # ....................... #

    @classmethod
    def create_many(cls, data: list[Self], arango_kwargs: dict[str, Any] = {}):
        """
        Create multiple documents in the collection

        Args:
            data (list[Self]): List of data models to be created
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (list[Self]): List of created data models
        """

        collection = cls._get_collection()
        _data = [cls._serialize(item.model_dump()) for item in data]

        res = collection.insert_many(
            _data,
            return_new=True,
            **arango_kwargs,
        )

        successful_docs = [x for x in res if isinstance(x, dict)]  # type: ignore
        successful_keys = [x["_key"] for x in successful_docs]

        return [d for d in data if d.id in successful_keys]

    # ....................... #

    @classmethod
    def update_many(
        cls,
        objects: list[Self],
        updates: list[AbstractData],
        soft_frozen: bool = True,
        trusted: bool = False,
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Update multiple documents with the given data. Replaces documents on update.

        Args:
            objects (list[Self]): List of documents to update
            updates (list[AbstractData]): List of data to update the documents with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the documents)
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            list[Self]: List of updated documents
            list[dict[str, Any]]: List of differences between the old and new documents
        """

        collection = cls._get_collection()
        diffs: list[dict[str, Any]] = []
        _docs: list[Self | None] = []

        for o, u in zip(objects, updates):
            upd = o._determine_update_dict(u, soft_frozen=soft_frozen)
            diffs.append(upd)

            if upd:
                new = o._perform_model_update(upd, trusted=trusted)
                _docs.append(new)

            else:
                _docs.append(None)

        docs = [cls._serialize(d.model_dump()) for d in _docs if d is not None]

        if docs:
            _res = collection.replace_many(
                docs,
                return_new=True,
                **arango_kwargs,
            )

        output = [o if _d is None else _d for o, _d in zip(objects, _docs)]

        return output, diffs

    # ....................... #

    def atomic_update(
        self: Self,
        updates: AbstractData,
        soft_frozen: bool = True,
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Atomic update of the document. This method doesn't return the updated instance and doesn't validate the update data, so you should trust it.

        Args:
            updates (AbstractData): Data to update the document with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            diff (dict[str, Any]): Differences between the old and new document
        """

        collection = self._get_collection()
        upd = self._determine_update_dict(updates, soft_frozen=soft_frozen)

        if upd:
            collection.update({"_key": self.id, **upd}, silent=True, **arango_kwargs)

        return upd

    # ....................... #

    @classmethod
    def atomic_update_many(
        cls,
        objects: list[Self],
        updates: list[AbstractData],
        soft_frozen: bool = True,
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Atomic update of multiple documents. This method doesn't return the updated instances and doesn't validate the update data, so you should trust it.

        Args:
            objects (list[Self]): List of documents to update
            updates (list[AbstractData]): List of data to update the documents with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            list[dict[str, Any]]: List of differences between the old and new documents
        """

        collection = cls._get_collection()
        _docs: list[dict[str, Any]] = []
        diffs: list[dict[str, Any]] = []

        for o, u in zip(objects, updates):
            upd = o._determine_update_dict(u, soft_frozen=soft_frozen)
            diffs.append(upd)

            if upd:
                _docs.append({"_key": o.id, **upd})

        if _docs:
            collection.update_many(_docs, silent=True, **arango_kwargs)

        return diffs

    # ....................... #

    @classmethod
    def find(cls, id_: str):
        """
        Find a document in the collection

        Args:
            id_ (str): Document ID

        Returns:
            res (Self): Found data model

        Raises:
            BadRequest: Request or value is required
            NotFound: Document not found
        """

        collection = cls._get_collection()

        request = {"_key": id_}

        document = collection.get(request)
        document = cast(dict | None, document)

        if not document:
            raise NotFound(f"Document with ID {id_} not found")

        return cls(**cls._deserialize(document))

    # ....................... #

    @classmethod
    def find_one(
        cls,
        filters: Optional[CONDITIONAL] = None,
        doc_clause: str = "doc",
        bind_vars: dict[str, Any] = {},
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Find one document in the collection matching the query

        Args:
            filters (list[str | list[str]], optional): Filters to apply to the query.
            doc_clause (str, optional): Document clause substitution.
            bind_vars (dict[str, Any], optional): Bind variables for the query.
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (Self): Found data model
        """

        iterator = CollectionIteratorParameters(doc_clause=doc_clause)
        parameters = CollectionQueryParameters(filters=filters, limit=1)

        q = ArangoQueryBuilder.build_collection_query(
            collection=cls.config.collection,
            iterator=iterator,
            parameters=parameters,
        )

        res: list[dict] = cls._raw_query(
            query=q,
            bind_vars=bind_vars,
            arango_kwargs=arango_kwargs,
        )

        if not res:
            raise NotFound("No documents found matching the query")

        return cls(**cls._deserialize(res[0]))

    # ....................... #

    @classmethod
    def count(
        cls,
        filters: Optional[CONDITIONAL] = None,
        doc_clause: str = "doc",
        bind_vars: dict[str, Any] = {},
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Count documents in the collection

        Args:
            filters (list[str | list[str]], optional): Filters to apply to the query.
            doc_clause (str, optional): Document clause substitution.
            bind_vars (dict[str, Any], optional): Bind variables for the query.
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (int): Number of documents
        """

        iterator = CollectionIteratorParameters(doc_clause=doc_clause)
        parameters = CollectionQueryParameters(filters=filters, return_clause="1")

        q = ArangoQueryBuilder.build_collection_query(
            collection=cls.config.collection,
            iterator=iterator,
            parameters=parameters,
        )
        q = f"RETURN LENGTH({q})"

        res: list[int] = cls._raw_query(
            query=q,
            bind_vars=bind_vars,
            arango_kwargs=arango_kwargs,
        )

        return res[0]

    # ....................... #

    @classmethod
    def find_many(
        cls,
        filters: Optional[CONDITIONAL] = None,
        limit: int = 100,
        offset: int = 0,
        sort: Optional[list[str]] = None,
        doc_clause: str = "doc",
        bind_vars: dict[str, Any] = {},
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Find multiple documents in the collection matching the query

        Args:
            filters (list[str | list[str]], optional): Filters to apply to the query.
            limit (int, optional): Limit the number of documents.
            offset (int, optional): Offset the number of documents.
            sort (list[str], optional): Sort the documents.
            doc_clause (str, optional): Document clause substitution.
            bind_vars (dict[str, Any], optional): Bind variables for the query.
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (list[Self]): List of found data models
        """

        iterator = CollectionIteratorParameters(doc_clause=doc_clause)
        parameters = CollectionQueryParameters(
            filters=filters,
            limit=limit,
            offset=offset,
            sort=sort,
        )
        q = ArangoQueryBuilder.build_collection_query(
            collection=cls.config.collection,
            iterator=iterator,
            parameters=parameters,
        )

        res: list[dict] = cls._raw_query(
            query=q,
            bind_vars=bind_vars,
            arango_kwargs=arango_kwargs,
        )

        return [cls(**cls._deserialize(doc)) for doc in res]

    # ....................... #

    @classmethod
    def find_all(
        cls,
        filters: Optional[CONDITIONAL] = None,
        sort: Optional[list[str]] = None,
        doc_clause: str = "doc",
        bind_vars: dict[str, Any] = {},
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Find all documents in the collection matching the query

        Args:
            filters (list[str | list[str]], optional): Filters to apply to the query.
            sort (list[str], optional): Sort the documents.
            doc_clause (str, optional): Document clause substitution.
            bind_vars (dict[str, Any], optional): Bind variables for the query.
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client
        Returns:
            res (list[Self]): List of found data models
        """

        iterator = CollectionIteratorParameters(doc_clause=doc_clause)
        parameters = CollectionQueryParameters(filters=filters, sort=sort)

        q = ArangoQueryBuilder.build_collection_query(
            collection=cls.config.collection,
            iterator=iterator,
            parameters=parameters,
        )

        res: list[dict] = cls._raw_query(
            query=q,
            bind_vars=bind_vars,
            arango_kwargs=arango_kwargs,
        )

        return [cls(**cls._deserialize(doc)) for doc in res]

    # ....................... #

    @classmethod
    def find_all_projection(
        cls,
        fields: list[str],
        filters: Optional[CONDITIONAL] = None,
        sort: Optional[list[str]] = None,
        doc_clause: str = "doc",
        bind_vars: dict[str, Any] = {},
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Find all document projections in the collection matching the query and fields

        Args:
            fields (list[str]): Fields to include.
            filters (list[str | list[str]], optional): Filters to apply to the query.
            sort (list[str], optional): Sort the documents.
            doc_clause (str, optional): Document clause substitution.
            bind_vars (dict[str, Any], optional): Bind variables for the query.
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (list[dict]): List of found document projections
        """

        return_clause = ArangoQueryBuilder.build_projection_expression(
            fields=fields,
            doc_clause=doc_clause,
        )
        iterator = CollectionIteratorParameters(doc_clause=doc_clause)
        parameters = CollectionQueryParameters(
            filters=filters,
            sort=sort,
            return_clause=return_clause,
        )

        q = ArangoQueryBuilder.build_collection_query(
            collection=cls.config.collection,
            iterator=iterator,
            parameters=parameters,
        )

        res: list[dict] = cls._raw_query(
            query=q,
            bind_vars=bind_vars,
            arango_kwargs=arango_kwargs,
        )

        return res

    # ....................... #

    def kill(self: Self, arango_kwargs: dict[str, Any] = {}):
        """
        Hard delete a document from the collection

        Args:
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client
        """

        collection = self._get_collection()
        collection.delete(document={"_key": self.id}, **arango_kwargs)

    # ....................... #

    @classmethod
    def kill_many(cls, ids: list[str], arango_kwargs: dict[str, Any] = {}):
        """
        Hard delete multiple documents from the collection

        Args:
            ids (list[str]): List of document IDs
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client
        """

        collection = cls._get_collection()
        collection.delete_many(
            documents=[{"_key": id_} for id_ in ids],
            **arango_kwargs,
        )

    # ....................... #

    @classmethod
    def patch(
        cls,
        data: TabularData,
        include: Optional[Sequence[str]] = None,
        on: Optional[str] = None,
        left_on: Optional[str] = None,
        right_on: Optional[str] = None,
        prefix: Optional[str] = None,
        kind: Literal["inner", "left"] = "inner",
        fill_none: Any = None,
    ):
        """
        Extend data with documents from the collection

        Args:
            data (TabularData): Data to be extended
            include (Sequence[str], optional): Fields to include
            on (str, optional): Field to join on. If provided, `left_on` and `right_on` will be ignored
            left_on (str, optional): Field to join on the left
            right_on (str, optional): Field to join on the right
            prefix (str, optional): Prefix for the fields
            kind (Literal["inner", "left"], optional): Kind of join
            fill_none (Any, optional): Value to fill None

        Returns:
            res (TabularData): Extended data

        Raises:
            BadRequest: if `data` is empty, `on` or `left_on` and `right_on` are not provided
        """

        if not data:
            raise BadRequest("`data` is required")

        if on is not None:
            left_on = on
            right_on = on

        if left_on is None or right_on is None:
            raise BadRequest("Fields `left_on` and `right_on` are required")

        if kind == "left" and not include:  # type safe
            raise BadRequest("Fields to include are required for left join")

        if include is not None:
            include = list(include)
            include.append(right_on)
            include = list(set(include))

        if not include:
            docs = cls.find_all(
                filters=[f"doc.{right_on} IN @left_on_unique"],
                bind_vars={
                    "left_on_unique": list(data.unique(left_on)),
                },
            )

        else:
            docs = cls.find_all_projection(
                filters=[f"doc.{right_on} IN @left_on_unique"],
                bind_vars={
                    "left_on_unique": list(data.unique(left_on)),
                },
                fields=list(include),
            )

        tab_docs = TabularData(docs)

        if not len(tab_docs) and kind == "left":
            tab_docs = TabularData([{k: fill_none for k in include}])  # type: ignore

        return data.join(
            other=tab_docs.slice(include=include),
            on=on,
            left_on=left_on,
            right_on=right_on,
            prefix=prefix,
            kind=kind,
            fill_none=fill_none,
        )

    # ....................... #

    @classmethod
    def build_global_id(cls, id_: str) -> str:
        """
        Build global ID

        Args:
            id_ (str): ID

        Returns:
            global_id (str): Global ID
        """

        return f"{cls.config.collection}/{id_}"

    # ....................... #

    @property
    def global_id(self: Self) -> str:
        """
        Get global ID

        Returns:
            global_id (str): Global ID
        """

        return self.build_global_id(self.id)

    # ....................... #

    @staticmethod
    def safe_init(*entries: "ArangoBase | ArangoBaseEdge"):
        """
        Safe create collections

        Args:
            entries (tuple[ArangoBase | ArangoBaseEdge]): The entries to initialize
        """

        if not entries:
            entries: list[ArangoBase | ArangoBaseEdge] = Registry.get_by_config(  # type: ignore[no-redef]
                ArangoConfig
            )

        for x in entries:
            x._get_collection()


# ....................... #


class ArangoBaseEdge(ArangoBase):
    """ArangoDB base edge class"""

    from_: str = Field(frozen=True)
    to_: str = Field(frozen=True)

    __discriminator__ = ["database", "collection"]

    # ....................... #

    @classmethod
    def _get_collection(cls):
        """
        Get assigned ArangoDB collection

        Returns:
            collection (arango.StandardCollection): Assigned ArangoDB collection
        """

        collection = cls.config.collection
        db = cls._get_database()

        if not db.has_collection(collection):
            db.create_collection(collection, edge=True)

        return db.collection(collection)

    # ....................... #

    @staticmethod
    def _serialize(doc: dict) -> dict:
        """
        Serialize an edge document

        Args:
            doc (dict): Edge document to serialize

        Returns:
            doc (dict): Serialized edge document
        """

        doc = ArangoBase._serialize(doc)

        doc["_from"] = doc.pop("from_")
        doc["_to"] = doc.pop("to_")

        return doc

    # ....................... #

    @staticmethod
    def _deserialize(doc: dict) -> dict:
        """
        Deserialize an edge document

        Args:
            doc (dict): Edge document to deserialize

        Returns:
            doc (dict): Deserialized edge document
        """

        doc = ArangoBase._deserialize(doc)

        doc["from_"] = doc.pop("_from")
        doc["to_"] = doc.pop("_to")

        return doc

    # ....................... #

    @classmethod
    def find(cls, id_: str):
        raise NotImplementedError

    # ....................... #

    @classmethod
    def find_by_vertices(cls, from_: str, to_: str):
        """
        Find an edge document in the collection

        Args:
            from_ (str): From node ID
            to_ (str): To node ID

        Returns:
            res (Self): Found data model

        Raises:
            NotFound: Edge not found
        """

        collection = cls._get_collection()

        request = {"_from": from_, "_to": to_}

        document = collection.get(request)
        document = cast(dict | None, document)

        if not document:
            raise NotFound(f"Edge {from_} -> {to_} not found")

        return cls(**cls._deserialize(document))

    # ....................... #

    @classmethod
    def patch(cls):
        raise NotImplementedError


# ....................... #


class ArangoEdgeDefinition(BaseModel):
    """ArangoDB edge definition"""

    edge_collection: type[ArangoBaseEdge]
    from_nodes: list[type[ArangoBase]]
    to_nodes: list[type[ArangoBase]]


# ....................... #


class ArangoBaseGraph(AbstractABC):
    """ArangoDB graph class"""

    edge_definitions: ClassVar[list[ArangoEdgeDefinition]] = []

    # ....................... #

    config: ClassVar[ArangoGraphConfig] = ArangoGraphConfig()
    _static: ClassVar[Optional[ArangoClient]] = None
    __discriminator__ = ["database", "name"]

    # ....................... #

    @classmethod
    def _client(cls):
        """
        Get syncronous ArangoDB client

        Returns:
            client (arango.ArangoClient): Syncronous ArangoDB client
        """

        if cls._static is None:
            cls._static = ArangoClient(hosts=cls.config.url())

        return cls._static

    # ....................... #

    @classmethod
    def _get_database(cls):
        """
        Get assigned ArangoDB database

        Returns:
            database (arango.StandardDatabase): Assigned ArangoDB database
        """

        client = cls._client()
        username = cls.config.credentials.username.get_secret_value()
        password = cls.config.credentials.password.get_secret_value()
        database = cls.config.database

        sys_db = client.db(
            "_system",
            username=username,
            password=password,
        )

        if not sys_db.has_database(database):
            sys_db.create_database(database)

        db = client.db(
            database,
            username=username,
            password=password,
        )

        return db

    # ....................... #

    @classmethod
    def _get_graph(cls):
        """
        Get assigned ArangoDB graph

        Returns:
            graph (arango.StandardGraph): Assigned ArangoDB graph
        """

        name = cls.config.name
        db = cls._get_database()

        if not db.has_graph(name):
            edge_definitions = [
                {
                    "edge_collection": e.edge_collection.config.collection,
                    "from_vertex_collections": [
                        node.config.collection for node in e.from_nodes
                    ],
                    "to_vertex_collections": [
                        node.config.collection for node in e.to_nodes
                    ],
                }
                for e in cls.edge_definitions
            ]
            db.create_graph(name, edge_definitions=edge_definitions)

        return db.graph(name)

    # ....................... #

    @classmethod
    def raw_query(
        cls,
        query: str,
        bind_vars: dict[str, Any] = {},
        batch_size: int = 1000,
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Execute a raw query against ArangoDB

        Args:
            query (str): AQL query to execute
            bind_vars (dict[str, Any], optional): Bind variables
            batch_size (int, optional): Batch size. Defaults to 1000
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (list[dict]): List of results
        """

        return _execute_query(
            db=cls._get_database(),
            query=query,
            bind_vars=bind_vars,
            batch_size=batch_size,
            arango_kwargs=arango_kwargs,
        )

    # ....................... #

    @classmethod
    def traverse(
        cls,
        iterator: GraphIteratorParameters,
        parameters: GraphQueryParameters = GraphQueryParameters(),
        bind_vars: dict[str, Any] = {},
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Perform a graph traversal

        Args:
            iterator (GraphIteratorParameters): Graph iterator specification
            parameters (GraphQueryParameters, optional): Graph query parameters
            bind_vars (dict[str, Any], optional): Bind variables
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            res (list[dict]): List of results
        """

        q = ArangoQueryBuilder.build_graph_query(
            graph=cls.config.name,
            iterator=iterator,
            parameters=parameters,
        )

        res: list[dict] = cls.raw_query(
            query=q,
            bind_vars=bind_vars,
            arango_kwargs=arango_kwargs,
        )

        return res

    # ....................... #

    @classmethod
    def count(
        cls,
        iterator: GraphIteratorParameters,
        parameters: GraphQueryParameters = GraphQueryParameters(),
        bind_vars: dict[str, Any] = {},
        arango_kwargs: dict[str, Any] = {},
    ):
        """
        Count graph traversal results

        Args:
            iterator (GraphIteratorParameters): Graph iterator specification
            parameters (GraphQueryParameters, optional): Graph query parameters
            bind_vars (dict[str, Any], optional): Bind variables
            arango_kwargs (dict[str, Any], optional): Additional arguments to pass to the ArangoDB client

        Returns:
            cnt (int): Number of graph traversal results
        """

        parameters.pop("limit", None)
        parameters.pop("offset", None)
        parameters["return_clause"] = "1"

        q = ArangoQueryBuilder.build_graph_query(
            graph=cls.config.name,
            iterator=iterator,
            parameters=parameters,
        )

        q = f"RETURN LENGTH({q})"

        res: list[int] = cls.raw_query(
            query=q,
            bind_vars=bind_vars,
            arango_kwargs=arango_kwargs,
        )

        return res[0]

    # ....................... #

    @staticmethod
    def safe_init(*entries: "ArangoBaseGraph"):
        """
        Safe create graphs

        Args:
            entries (tuple[ArangoBaseGraph]): The entries to initialize
        """

        if not entries:
            entries: list[ArangoBaseGraph] = Registry.get_by_config(ArangoGraphConfig)  # type: ignore[no-redef]

        for x in entries:
            x._get_graph()
