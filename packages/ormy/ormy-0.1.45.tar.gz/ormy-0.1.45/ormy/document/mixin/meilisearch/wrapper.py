import asyncio
from contextlib import asynccontextmanager, contextmanager
from typing import Any, Callable, ClassVar, Optional, Self, TypeVar, cast

from ormy._abc.registry import Registry
from ormy.base.typing import AsyncCallable
from ormy.document._abc import DocumentMixinABC
from ormy.exceptions import ModuleNotFound

try:
    from meilisearch_python_sdk import AsyncClient, Client
    from meilisearch_python_sdk.errors import MeilisearchApiError
    from meilisearch_python_sdk.models.search import (
        Federation,
        SearchParams,
        SearchResultsFederated,
    )
    from meilisearch_python_sdk.models.settings import MeilisearchSettings
    from meilisearch_python_sdk.types import JsonDict
except ImportError as e:
    raise ModuleNotFound(
        extra="meilisearch", packages=["meilisearch-python-sdk"]
    ) from e

from .config import MeilisearchConfig
from .schema import (
    AnyFilter,
    ArrayFilter,
    BooleanFilter,
    DatetimeFilter,
    MeilisearchReference,
    NumberFilter,
    SearchRequest,
    SearchRequestDict,
    SearchResponse,
    SortField,
)

# ----------------------- #

T = TypeVar("T")

# ----------------------- #


class MeilisearchMixin(DocumentMixinABC):
    """Meilisearch mixin"""

    mixin_configs: ClassVar[list[Any]] = [MeilisearchConfig()]

    __meili_static: ClassVar[Optional[Client]] = None
    __ameili_static: ClassVar[Optional[AsyncClient]] = None

    # ....................... #

    def __init_subclass__(cls, **kwargs):
        """Initialize subclass"""

        super().__init_subclass__(**kwargs)

        cls.defer_mixin_registration(
            config=MeilisearchConfig,
            discriminator="index",
        )

    # ....................... #

    @classmethod  # TODO: remove ? or simplify somehow
    def meili_model_reference(cls):
        """
        **[DEPRECATED]**

        Generate a Meilisearch reference for the model schema with filters and sort fields

        Returns:
            schema (MeilisearchReference): The Meilisearch reference for the model schema
        """

        full_schema = cls.model_flat_schema()
        cfg = cls.get_mixin_config(type_=MeilisearchConfig)

        sort = []
        filters = []

        if filterable := cfg.settings.filterable_attributes:
            for f in filterable:
                if field := next((x for x in full_schema if x["key"] == f), None):
                    filter_model: Optional[type[AnyFilter]] = None

                    match field["type"]:
                        case "boolean":
                            filter_model = BooleanFilter

                        case "number":
                            filter_model = NumberFilter

                        case "integer":
                            filter_model = NumberFilter

                        case "datetime":
                            filter_model = DatetimeFilter

                        case "array":
                            filter_model = ArrayFilter

                        case _:
                            field["type"] = "array"
                            filter_model = ArrayFilter

                    if filter_model:
                        filters.append(filter_model.model_validate(field))

        if sortable := cfg.settings.sortable_attributes:
            default_sort = cfg.settings.default_sort

            for s in sortable:
                if field := next((x for x in full_schema if x["key"] == s), None):
                    sort_key = SortField(**field, default=s == default_sort)
                    sort.append(sort_key)

        return MeilisearchReference(filters=filters, sort=sort)  # type: ignore[arg-type]

    # ....................... #

    @classmethod
    def __is_static_meili(cls):
        """
        Check if static Meilisearch client is used

        Returns:
            use_static (bool): Whether to use static Meilisearch client
        """

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)
        use_static = not cfg.context_client

        return use_static

    # ....................... #

    @classmethod
    def __get_exclude_mask(cls):
        """Get exclude mask"""

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)
        return cfg.settings.exclude_mask

    # ....................... #

    @classmethod
    def __meili_abstract_client(cls):
        """
        Abstract client

        Returns:
            client (meilisearch_python_sdk.Client): Abstract client
        """

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)
        url = cfg.url()
        key = cfg.credentials.master_key

        if key:
            api_key = key.get_secret_value()

        else:
            api_key = None

        return Client(
            url=url,
            api_key=api_key,
            custom_headers={"Content-Type": "application/json"},
        )

    # ....................... #

    @classmethod
    def __ameili_abstract_client(cls):
        """
        Abstract async client

        Returns:
            client (meilisearch_python_sdk.AsyncClient): Abstract async client
        """

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)
        url = cfg.url()
        key = cfg.credentials.master_key

        if key:
            api_key = key.get_secret_value()

        else:
            api_key = None

        return AsyncClient(
            url=url,
            api_key=api_key,
            custom_headers={"Content-Type": "application/json"},
        )

    # ....................... #

    @classmethod
    def _meili_static_client(cls):
        """
        Get static Meilisearch client

        Returns:
            client (meilisearch_python_sdk.Client): Static Meilisearch client
        """

        if cls.__meili_static is None:
            cls.__meili_static = cls.__meili_abstract_client()

        return cls.__meili_static

    # ....................... #

    @classmethod
    def _ameili_static_client(cls):
        """
        Get static async Meilisearch client

        Returns:
            client (meilisearch_python_sdk.AsyncClient): Static async Meilisearch client
        """

        if cls.__ameili_static is None:
            cls.__ameili_static = cls.__ameili_abstract_client()

        return cls.__ameili_static

    # ....................... #

    @classmethod
    def __meili_execute_task(cls, task: Callable[[Any], T], *args, **kwargs) -> T:
        """Execute task"""

        if cls.__is_static_meili():
            c = cls._meili_static_client()
            return task(c, *args, **kwargs)

        else:
            with cls._meili_client() as c:
                return task(c, *args, **kwargs)

    # ....................... #

    @classmethod
    async def __ameili_execute_task(
        cls, task: AsyncCallable[[Any], T], *args, **kwargs
    ) -> T:
        """Execute async task"""

        if cls.__is_static_meili():
            c = cls._ameili_static_client()
            return await task(c, *args, **kwargs)

        else:
            async with cls._ameili_client() as c:
                return await task(c, *args, **kwargs)

    # ....................... #

    @classmethod
    def meili_safe_create_or_update(cls):
        """
        Safely create or update the Meilisearch index.
        If the index does not exist, it will be created.
        If the index exists and settings were updated, index will be updated.
        """

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)

        def _task(c: Client):
            try:
                ix = c.get_index(cfg.index)
                cls._logger().debug(f"Index `{cfg.index}` already exists")
                settings = MeilisearchSettings.model_validate(cfg.settings.model_dump())

                if ix.get_settings() != settings:
                    ix.update_settings(settings)
                    cls._logger().debug(f"Update of index `{cfg.index}` is started")

            except MeilisearchApiError:
                settings = MeilisearchSettings.model_validate(cfg.settings.model_dump())
                c.create_index(
                    cfg.index,
                    primary_key=cfg.primary_key,
                    settings=settings,
                )
                cls._logger().debug(f"Index `{cfg.index}` is created")

        if not cfg.is_default():
            cls.__meili_execute_task(_task)

    # ....................... #

    @classmethod
    async def ameili_safe_create_or_update(cls):
        """
        Safely create or update the Meilisearch index.
        If the index does not exist, it will be created.
        If the index exists and settings were updated, index will be updated.
        """

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)

        async def _task(c: AsyncClient):
            try:
                ix = await c.get_index(cfg.index)
                cls._logger().debug(f"Index `{cfg.index}` already exists")
                settings = MeilisearchSettings.model_validate(cfg.settings.model_dump())

                if (await ix.get_settings()) != settings:
                    await ix.update_settings(settings)
                    cls._logger().debug(f"Update of index `{cfg.index}` is started")

            except MeilisearchApiError:
                settings = MeilisearchSettings.model_validate(cfg.settings.model_dump())
                await c.create_index(
                    cfg.index,
                    primary_key=cfg.primary_key,
                    settings=settings,
                )
                cls._logger().debug(f"Index `{cfg.index}` is created")

        if not cfg.is_default():
            await cls.__ameili_execute_task(_task)

    # ....................... #

    @classmethod  # TODO: move above
    @contextmanager
    def _meili_client(cls):
        """
        Get syncronous Meilisearch client

        Yields:
            client (meilisearch_python_sdk.Client): Meilisearch client
        """

        try:
            yield cls.__meili_abstract_client()

        finally:
            pass

    # ....................... #

    @classmethod  # TODO: move above
    @asynccontextmanager
    async def _ameili_client(cls):
        """
        Get asyncronous Meilisearch client

        Yields:
            client (meilisearch_python_sdk.AsyncClient): Meilisearch client
        """

        try:
            yield cls.__ameili_abstract_client()

        finally:
            pass

    # ....................... #

    @classmethod
    def _meili_health(cls) -> bool:
        """
        Check Meilisearch health

        Returns:
            status (bool): Whether Meilisearch is healthy
        """

        def _task(c: Client):
            try:
                h = c.health()
                status = h.status == "available"

            except Exception:
                status = False

            return status

        return cls.__meili_execute_task(_task)

    # ....................... #

    @classmethod
    async def _ameili_health(cls) -> bool:
        """
        Check Meilisearch health

        Returns:
            status (bool): Whether Meilisearch is healthy
        """

        async def _task(c: AsyncClient):
            try:
                h = await c.health()
                status = h.status == "available"

            except Exception:
                status = False

            return status

        return await cls.__ameili_execute_task(_task)

    # ....................... #

    @classmethod
    def _meili_index(cls):
        """
        Get associated Meilisearch index

        Returns:
            index (meilisearch_python_sdk.Index): Meilisearch index
        """

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)

        def _task(c: Client):
            return c.get_index(cfg.index)

        return cls.__meili_execute_task(_task)

    # ....................... #

    @classmethod
    async def _ameili_index(cls):
        """
        Get associated Meilisearch index in asyncronous mode

        Returns:
            index (meilisearch_python_sdk.Index): Meilisearch index
        """

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)

        async def _task(c: AsyncClient):
            return await c.get_index(cfg.index)

        return await cls.__ameili_execute_task(_task)

    # ....................... #

    @classmethod
    def _meili_multi_search(
        cls,
        queries: list[SearchParams],
        federation: Optional[Federation] = None,
    ):
        """
        Multi search documents in Meilisearch

        Args:
            queries (list[SearchParams]): The queries to search
            federation (Federation, optional): The federation to use

        Returns:
            response (SearchResultsFederated): The search response
        """

        def _task(c: Client):
            res = c.multi_search(
                queries=queries,
                federation=federation,
            )
            res = cast(SearchResultsFederated, res)
            return res

        return cls.__meili_execute_task(_task)

    # ....................... #

    @classmethod
    async def _ameili_multi_search(
        cls,
        queries: list[SearchParams],
        federation: Optional[Federation] = None,
    ):
        """
        Multi search documents in Meilisearch in asyncronous mode

        Args:
            queries (list[SearchParams]): The queries to search
            federation (Federation, optional): The federation to use

        Returns:
            response (SearchResultsFederated): The search response
        """

        async def _task(c: AsyncClient):
            res = await c.multi_search(
                queries=queries,
                federation=federation,
            )
            res = cast(SearchResultsFederated, res)
            return res

        return await cls.__ameili_execute_task(_task)

    # ....................... #

    @classmethod
    def _meili_prepare_request(
        cls,
        request: SearchRequest | SearchRequestDict,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ):
        """
        Prepare search request

        Args:
            request (SearchRequest | SearchRequestDict): The search request
            page (int, optional): The page number. Defaults to 1.
            size (int, optional): The number of hits per page. Defaults to 20.

        Returns:
            request (dict): The prepared search request
        """

        def _check_raw(
            x: str, filterable: list[str], all_attributes: list[str]
        ) -> bool:
            k, *_ = x.split(" ")
            return k in filterable or (filterable == ["*"] and k in all_attributes)

        cfg = cls.get_mixin_config(type_=MeilisearchConfig)
        sortable = cfg.settings.sortable_attributes
        filterable = cfg.settings.filterable_attributes
        all_attributes = list(cls.model_fields.keys()) + list(
            cls.model_computed_fields.keys()
        )

        if sortable is None:
            sortable = []

        if isinstance(request, dict):
            request = SearchRequest.model_validate(request)

        if request.sort and request.sort in sortable:
            sort = [f"{request.sort}:{request.order.value}"]

        else:
            sort = None

        if request.filters and filterable:
            raw_filters = [f.build() for f in request.filters if f.type == "raw"]
            exclude_raw = []

            for i, x in enumerate(raw_filters):
                if isinstance(x, str):
                    if not _check_raw(x, filterable, all_attributes):
                        exclude_raw.append(i)

                else:
                    for y in x:
                        if not _check_raw(y, filterable, all_attributes):
                            exclude_raw.append(i)
                            break

            raw_filters = [x for i, x in enumerate(raw_filters) if i not in exclude_raw]

            filters = [
                f.build()
                for f in request.filters
                if (
                    f.key in filterable
                    or (filterable == ["*"] and f.key in all_attributes)
                )
                and f.type != "raw"
            ]
            filters = list(filter(None, filters))
            filters.extend(raw_filters)

        else:
            filters = []

        req = {
            "query": request.query,
            "sort": sort,
            "filter": filters,
        }

        if page is not None and size is not None:
            req["hits_per_page"] = size  # type: ignore[assignment]
            req["page"] = page  # type: ignore[assignment]

        return req

    # ....................... #

    @staticmethod
    def _meili_prepare_response(res: Any, federated: bool = False):
        """
        Prepare search response

        Args:
            res (meilisearch_python_sdk.models.search.SearchResults): The search results

        Returns:
            response (SearchResponse): The prepared search response
        """

        return SearchResponse.from_search_results(res, federated)

    # ....................... #

    @classmethod
    def _prepare_fields(
        cls,
        include: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
    ):
        """
        Prepare fields for search

        Args:
            include (list[str], optional): The fields to include in the search
            exclude (list[str], optional): The fields to exclude from the search

        Returns:
            include (list[str]): The prepared fields
        """

        #! Not necessary ??

        fields = list(cls.model_fields.keys()) + list(cls.model_computed_fields.keys())

        if exclude is not None and include is None:
            include = [x for x in fields if x not in exclude]

        elif include is not None:
            include = [x for x in include if x in fields]

        return include

    # ....................... #

    @classmethod
    def meili_search(
        cls,
        request: SearchRequest | SearchRequestDict,
        page: int = 1,
        size: int = 20,
        include: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
    ):
        """
        Search documents in Meilisearch

        Args:
            request (SearchRequest | SearchRequestDict): The search request
            page (int, optional): The page number. Defaults to 1.
            size (int, optional): The number of hits per page. Defaults to 20.
            include (list[str], optional): The fields to include in the search
            exclude (list[str], optional): The fields to exclude from the search

        Returns:
            response (SearchResponse): The search response
        """

        attrs = cls._prepare_fields(include, exclude)
        ix = cls._meili_index()
        req = cls._meili_prepare_request(request, page, size)
        res = ix.search(attributes_to_retrieve=attrs, **req)

        return cls._meili_prepare_response(res)

    # ....................... #

    @classmethod
    async def ameili_search(
        cls,
        request: SearchRequest | SearchRequestDict,
        page: int = 1,
        size: int = 20,
        include: Optional[list[str]] = None,
        exclude: Optional[list[str]] = None,
    ):
        """
        Search documents in Meilisearch in asyncronous mode

        Args:
            request (SearchRequest | SearchRequestDict): The search request
            page (int, optional): The page number. Defaults to 1.
            size (int, optional): The number of hits per page. Defaults to 20.
            include (list[str], optional): The fields to include in the search
            exclude (list[str], optional): The fields to exclude from the search

        Returns:
            response (SearchResponse): The search response
        """

        attrs = cls._prepare_fields(include, exclude)
        ix = await cls._ameili_index()
        req = cls._meili_prepare_request(request, page, size)
        res = await ix.search(attributes_to_retrieve=attrs, **req)

        return cls._meili_prepare_response(res)

    # ....................... #

    @classmethod
    def meili_multi_search(
        cls,
        indexes: list[type[Self]],
        request: SearchRequest | SearchRequestDict,
        page: int = 1,
        size: int = 20,
    ):
        """
        Multi search documents in Meilisearch

        Args:
            indexes (list[type[Self]]): The indexes to search
            request (SearchRequest | SearchRequestDict): The search request
            page (int, optional): The page number. Defaults to 1.
            size (int, optional): The number of hits per page. Defaults to 20.
        """

        idxs_str = [x.get_mixin_config(type_=MeilisearchConfig).index for x in indexes]
        reqs = [x._meili_prepare_request(request) for x in indexes]
        fed = Federation(limit=size, offset=size * (page - 1))
        queries = [SearchParams(index_uid=i, **r) for i, r in zip(idxs_str, reqs)]
        res = cls._meili_multi_search(queries, fed)

        return cls._meili_prepare_response(res, True)

    # ....................... #

    @classmethod
    async def ameili_multi_search(
        cls,
        indexes: list[type[Self]],
        request: SearchRequest | SearchRequestDict,
        page: int = 1,
        size: int = 20,
    ):
        """
        Multi search documents in Meilisearch in asyncronous mode

        Args:
            indexes (list[type[Self]]): The indexes to search
            request (SearchRequest | SearchRequestDict): The search request
            page (int, optional): The page number. Defaults to 1.
            size (int, optional): The number of hits per page. Defaults to 20.
        """

        idxs_str = [x.get_mixin_config(type_=MeilisearchConfig).index for x in indexes]
        reqs = [x._meili_prepare_request(request) for x in indexes]
        fed = Federation(limit=size, offset=size * (page - 1))
        queries = [SearchParams(index_uid=i, **r) for i, r in zip(idxs_str, reqs)]
        res = await cls._ameili_multi_search(queries, fed)

        return cls._meili_prepare_response(res, True)

    # ....................... #

    @classmethod
    def meili_delete_documents(cls, ids: str | list[str]):
        """
        Delete documents from Meilisearch

        Args:
            ids (str | list[str]): The document IDs
        """

        ix = cls._meili_index()

        if isinstance(ids, str):
            ids = [ids]

        ix.delete_documents(ids)

    # ....................... #

    @classmethod
    async def ameili_delete_documents(cls, ids: str | list[str]):
        """
        Delete documents from Meilisearch in asyncronous mode

        Args:
            ids (str | list[str]): The document IDs
        """

        ix = await cls._ameili_index()

        if isinstance(ids, str):
            ids = [ids]

        await ix.delete_documents(ids)

    # ....................... #

    @classmethod
    def _meili_all_documents(cls):
        """
        Get all documents from Meilisearch

        Returns:
            documents (list[JsonDict]): The list of documents
        """

        ix = cls._meili_index()
        res: list[JsonDict] = []
        offset = 0

        while docs := ix.get_documents(offset=offset, limit=1000).results:
            res.extend(docs)
            offset += 1000

        return res

    # ....................... #

    @classmethod
    async def _ameili_all_documents(cls):
        """
        Get all documents from Meilisearch in asyncronous mode

        Returns:
            documents (list[JsonDict]): The list of documents
        """

        ix = await cls._ameili_index()
        res: list[JsonDict] = []
        offset = 0

        while docs := (await ix.get_documents(offset=offset, limit=1000)).results:
            res.extend(docs)
            offset += 1000

        return res

    # ....................... #

    @classmethod
    def meili_update_documents(cls, docs: Self | list[Self]):
        """
        Update documents in Meilisearch

        Args:
            docs (Self | list[Self]): The documents to update
        """

        ix = cls._meili_index()
        exclude_mask = cls.__get_exclude_mask()

        if not isinstance(docs, list):
            docs = [docs]

        masked = []

        if exclude_mask:
            for d in docs:
                for k, v in exclude_mask.items():
                    if hasattr(d, k):
                        doc_value = getattr(d, k)

                        if not isinstance(v, list):
                            v = [v]

                        if not isinstance(doc_value, list):
                            doc_value = [doc_value]

                        # Handle unhashable exceptions
                        try:
                            if set(doc_value).intersection(v):
                                masked.append(d)

                        except Exception:
                            pass

        doc_dicts = [d.model_dump() for d in docs if d not in masked]
        ix.update_documents(doc_dicts)

    # ....................... #

    @classmethod
    async def ameili_update_documents(cls, docs: Self | list[Self]):
        """
        Update documents in Meilisearch in asyncronous mode

        Args:
            docs (Self | list[Self]): The documents to update
        """

        ix = await cls._ameili_index()
        exclude_mask = cls.__get_exclude_mask()

        if not isinstance(docs, list):
            docs = [docs]

        masked = []

        if exclude_mask:
            for d in docs:
                for k, v in exclude_mask.items():
                    if hasattr(d, k):
                        doc_value = getattr(d, k)

                        if not isinstance(v, list):
                            v = [v]

                        if not isinstance(doc_value, list):
                            doc_value = [doc_value]

                        # Handle unhashable exceptions
                        try:
                            if set(doc_value).intersection(v):
                                masked.append(d)

                        except Exception:
                            pass

        doc_dicts = [d.model_dump() for d in docs if d not in masked]
        await ix.update_documents(doc_dicts)

    # ....................... #

    @classmethod
    def meili_last_update(cls):
        """
        Get the last update timestamp of the Meilisearch index

        Returns:
            timestamp (int | None): The last update timestamp
        """

        ix = cls._meili_index()
        dt = ix.updated_at

        if dt:
            return int(dt.timestamp())

        return None

    # ....................... #

    @classmethod
    async def ameili_last_update(cls):
        """
        Get the last update timestamp of the Meilisearch index in asyncronous mode

        Returns:
            timestamp (int | None): The last update timestamp
        """

        ix = await cls._ameili_index()
        dt = ix.updated_at

        if dt:
            return int(dt.timestamp())

        return None

    # ....................... #

    @staticmethod
    def meili_safe_init(*entries: "MeilisearchMixin"):
        """
        Safe create or update indexes

        Args:
            entries (tuple[MeilisearchMixin]): The entries to initialize
        """

        if not entries:
            entries: list[MeilisearchMixin] = Registry.get_by_config(MeilisearchConfig)  # type: ignore[no-redef]

        for x in entries:
            x.meili_safe_create_or_update()

    # ....................... #

    @staticmethod
    async def ameili_safe_init(*entries: "MeilisearchMixin"):
        """
        Safe create or update indexes in asyncronous mode

        Args:
            entries (tuple[MeilisearchMixin]): The entries to initialize
        """

        if not entries:
            entries: list[MeilisearchMixin] = Registry.get_by_config(MeilisearchConfig)  # type: ignore[no-redef]

        tasks = [x.ameili_safe_create_or_update() for x in entries]

        if tasks:
            await asyncio.gather(*tasks)
