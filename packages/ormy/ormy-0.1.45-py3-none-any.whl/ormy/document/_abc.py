from abc import abstractmethod
from typing import Any, ClassVar, Mapping, Self, TypeVar, cast

from pydantic import Field

from ormy._abc import (
    AbstractABC,
    AbstractMixinABC,
    ConfigABC,
    SemiFrozenField,
)
from ormy.base.func import dict_hash_difference, hex_uuid4
from ormy.base.pydantic import IGNORE
from ormy.base.typing import AbstractData
from ormy.exceptions import Conflict

# ----------------------- #

C = TypeVar("C", bound=ConfigABC)

# TODO: DocumentConfigABC ???

# ....................... #


class BaseDocumentABC(AbstractABC):
    """Abstract Base Class for Document-Oriented ORM"""

    id: str = Field(default_factory=hex_uuid4)

    semi_frozen_fields: ClassVar[Mapping[str, SemiFrozenField | dict[str, Any]]] = {}
    __discriminator__: ClassVar[list[str]] = []

    # ....................... #

    def __init_subclass__(cls, **kwargs):
        """Initialize subclass"""

        super().__init_subclass__(**kwargs)
        cls.__parse_semi_frozen_fields()

    # ....................... #

    @classmethod
    def __parse_semi_frozen_fields(cls):
        """Parse semi-frozen fields"""

        new = {}

        for field, value in cls.semi_frozen_fields.items():
            if isinstance(value, dict):
                new[field] = SemiFrozenField(**value)

            else:
                new[field] = value

        cls.semi_frozen_fields = new

    # ....................... #

    def _determine_update_dict(
        self: Self,
        data: AbstractData,
        soft_frozen: bool = True,
    ):
        if not isinstance(data, dict):
            data = data.model_dump()

        diff = dict_hash_difference(self.model_dump(), data)
        res = {}

        for k in diff.keys():
            val = data.get(k, IGNORE)

            if val != IGNORE and k in self.model_fields:
                if k in self.semi_frozen_fields.keys():
                    _semi = self.semi_frozen_fields[k]
                    semi = cast(SemiFrozenField, _semi)

                    if semi.evaluate(self):
                        if not soft_frozen:
                            raise Conflict(
                                f"Field {k} is semi-frozen within context {semi.context}"
                            )

                        else:
                            continue

                elif self.model_fields[k].frozen:
                    if not soft_frozen:
                        raise Conflict(f"Field {k} is frozen")

                    else:
                        continue

                res[k] = val

        return res

    # ....................... #

    def _perform_model_update(
        self: Self,
        update: dict[str, Any],
        trusted: bool = False,
    ):
        """
        Perform model update

        Args:
            update (dict[str, Any]): Update to perform
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the document)

        Returns:
            Self: Updated document
        """

        if trusted:
            for k, v in update.items():
                setattr(self, k, v)

            return self

        else:
            return self.model_copy(update=update, deep=True)


# ....................... #


class SyncDocumentABC(BaseDocumentABC):
    """Abstract Base Class for Document-Oriented ORM (Sync)"""

    @classmethod
    @abstractmethod
    def create(cls, data: Self) -> Self: ...

    # ....................... #

    @abstractmethod
    def save(self: Self) -> Self: ...

    # ....................... #

    @classmethod
    @abstractmethod
    def find(cls, id_: str) -> Self: ...

    # ....................... #

    @abstractmethod
    def kill(self: Self) -> None: ...

    # ....................... #

    @classmethod
    @abstractmethod
    def kill_many(cls, *args: Any, **kwargs: Any) -> None: ...

    # ....................... #

    def update(
        self: Self,
        updates: AbstractData,
        soft_frozen: bool = True,
        trusted: bool = False,
    ):
        """
        Update the document with the given data

        Args:
            updates (AbstractData): Data to update the document with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the document)

        Returns:
            res (Self): Updated document
            diff (dict[str, Any]): Differences between the old and new document
        """

        upd = self._determine_update_dict(updates, soft_frozen=soft_frozen)

        # Perform update only if there are any differences
        if upd:
            res = self._perform_model_update(upd, trusted=trusted)

            return res.save(), upd

        else:
            return self, {}

    # ....................... #

    @classmethod
    def update_many(
        cls,
        objects: list[Self],
        updates: list[AbstractData],
        soft_frozen: bool = True,
        trusted: bool = False,
    ) -> tuple[list[Self], list[dict[str, Any]]]:
        """
        Update multiple documents with the given data

        Args:
            objects (list[Self]): List of documents to update
            updates (list[AbstractData]): List of data to update the documents with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the documents)

        Returns:
            list[Self]: List of updated documents
            list[dict[str, Any]]: List of differences between the old and new documents
        """

        raise NotImplementedError

    # ....................... #

    def atomic_update(
        self: Self,
        updates: AbstractData,
        soft_frozen: bool = True,
    ) -> dict[str, Any]:
        """
        Atomic update of the document. This method doesn't return the updated instance and doesn't validate the update data, so you should trust it.

        Args:
            updates (AbstractData): Data to update the document with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the document)

        Returns:
            diff (dict[str, Any]): Differences between the old and new document
        """

        raise NotImplementedError

    # ....................... #

    @classmethod
    def atomic_update_many(
        cls,
        objects: list[Self],
        updates: list[AbstractData],
        soft_frozen: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Atomic update of multiple documents. This method doesn't return the updated instance and doesn't validate the update data, so you should trust it.

        Args:
            objects (list[Self]): List of documents to update
            updates (list[AbstractData]): List of data to update the documents with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the documents)

        Returns:
            list[dict[str, Any]]: List of differences between the old and new documents
        """

        raise NotImplementedError


# ....................... #


class AsyncDocumentABC(BaseDocumentABC):
    """Abstract Base Class for Document-Oriented ORM (Async)"""

    @classmethod
    @abstractmethod
    async def acreate(cls, data: Self) -> Self: ...

    # ....................... #

    @abstractmethod
    async def asave(self: Self) -> Self: ...

    # ....................... #

    @classmethod
    @abstractmethod
    async def afind(cls, id_: str) -> Self: ...

    # ....................... #

    @abstractmethod
    async def akill(self: Self) -> None: ...

    # ....................... #

    @classmethod
    @abstractmethod
    async def akill_many(cls, *args: Any, **kwargs: Any) -> None: ...

    # ....................... #

    async def aupdate(
        self: Self,
        updates: AbstractData,
        soft_frozen: bool = True,
        trusted: bool = False,
    ):
        """
        Update the document with the given data

        Args:
            updates (AbstractData): Data to update the document with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the document)

        Returns:
            res (Self): Updated document
            diff (dict[str, Any]): Differences between the old and new document
        """

        upd = self._determine_update_dict(updates, soft_frozen=soft_frozen)

        # Perform update only if there are any differences
        if upd:
            res = self._perform_model_update(upd, trusted=trusted)

            return await res.asave(), upd

        else:
            return self, {}

    # ....................... #

    @classmethod
    async def aupdate_many(
        cls,
        objects: list[Self],
        updates: list[AbstractData],
        soft_frozen: bool = True,
        trusted: bool = False,
    ) -> tuple[list[Self], list[dict[str, Any]]]:
        """
        Update multiple documents with the given data

        Args:
            objects (list[Self]): List of documents to update
            updates (list[AbstractData]): List of data to update the documents with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the documents)

        Returns:
            list[Self]: List of updated documents
            list[dict[str, Any]]: List of differences between the old and new documents
        """

        raise NotImplementedError

    # ....................... #

    async def aatomic_update(
        self: Self,
        updates: AbstractData,
        soft_frozen: bool = True,
    ) -> dict[str, Any]:
        """
        Atomic update of the document. This method doesn't return the updated instance and doesn't validate the update data, so you should trust it.

        Args:
            updates (AbstractData): Data to update the document with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the document)

        Returns:
            diff (dict[str, Any]): Differences between the old and new document
        """

        raise NotImplementedError

    # ....................... #

    @classmethod
    async def aatomic_update_many(
        cls,
        objects: list[Self],
        updates: list[AbstractData],
        soft_frozen: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Atomic update of multiple documents. This method doesn't return the updated instance and doesn't validate the update data, so you should trust it.

        Args:
            objects (list[Self]): List of documents to update
            updates (list[AbstractData]): List of data to update the documents with
            soft_frozen (bool): Whether to allow soft frozen fields to be updated
            trusted (bool): Whether to trust the update (if set to True, the update will be performed directly on the documents)

        Returns:
            list[dict[str, Any]]: List of differences between the old and new documents
        """

        raise NotImplementedError


# ....................... #


class DocumentABC(SyncDocumentABC, AsyncDocumentABC):
    """Document ABC Base Class with sync and async methods"""


# ....................... #


class DocumentMixinABC(AbstractMixinABC):
    """Document Mixin ABC Base Class"""
