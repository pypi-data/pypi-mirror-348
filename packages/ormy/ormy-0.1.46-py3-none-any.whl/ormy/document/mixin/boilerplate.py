from contextlib import asynccontextmanager, contextmanager
from typing import Any, ClassVar, Optional, Self

from ormy.document._abc import BaseDocumentABC

# ----------------------- #

try:
    from .meilisearch import MeilisearchConfig, MeilisearchMixin

    class _Meilisearch(BaseDocumentABC, MeilisearchMixin):
        mixin_configs: ClassVar[list[Any]] = [MeilisearchConfig()]

        # ....................... #

        def __init_subclass__(cls, **kwargs):
            """Initialize subclass"""

            super().__init_subclass__(**kwargs)

            cls.defer_config_patch(
                config_type=MeilisearchConfig,
                dynamic_field="index",
                compute_fn=lambda cls: f"{cls.config.database}-{cls.config.collection}",
            )

except ImportError:
    pass

# ....................... #

try:
    from .s3 import S3Config, S3Mixin

    class _S3(BaseDocumentABC, S3Mixin):
        mixin_configs: ClassVar[list[Any]] = [S3Config()]

        # ....................... #

        def __init_subclass__(cls, **kwargs):
            """Initialize subclass"""

            super().__init_subclass__(**kwargs)

            cls.defer_config_patch(
                config_type=S3Config,
                dynamic_field="bucket",
                compute_fn=lambda cls: f"{cls.config.database}-{cls.config.collection}",
            )

        # ....................... #

        def add_file(
            self: Self,
            file: bytes,
            name: str,
            avoid_duplicates: bool = True,
            tags: dict[str, str] = {},
        ):
            """
            Add an attachment to the entity

            Args:
                file (bytes): The file to add
                name (str): The name of the file
                avoid_duplicates (bool): Whether to avoid duplicates
                tags (dict[str, str]): The tags to add to the file

            Returns:
                result (str): The key of the attachment
            """

            key = f"{self.id}/{name}"

            f = self.s3_upload_file(
                key=key,
                file=file,
                avoid_duplicates=avoid_duplicates,
            )

            if tags:
                self.s3_add_file_tags(key=key, tags=tags)

            return f

        # ....................... #

        def download_file(self: Self, name: str):
            """
            Download an attachment from the entity

            Args:
                name (str): The name of the attachment to download

            Returns:
                result (bytes): The attachment
            """

            key = f"{self.id}/{name}"
            data = self.s3_download_file(key=key)

            return data["Body"]

        # ....................... #

        def remove_file(self: Self, name: str):
            """
            Remove a file from the entity

            Args:
                name (str): The name of the attachment to remove
            """

            key = f"{self.id}/{name}"

            return self.s3_delete_file(key=key)

        # ....................... #

        def list_files(self: Self, page: int = 1, size: int = 20):
            """
            list files from the entity

            Args:
                page (int): The page number
                size (int): The page size

            Returns:
                result (ormy.base.pydantic.TableResponse): The attachments
            """

            return self.s3_list_files(blob=str(self.id), page=page, size=size)

        # ....................... #

        def file_exists(self: Self, name: Optional[str] = None) -> bool:
            """
            Check if a file exists

            Args:
                name (str): The name of the file to check

            Returns:
                result (bool): Whether the file exists
            """

            if not name:
                return False

            key: str = f"{self.id}/{name}"

            return self.s3_file_exists(key=key)

except ImportError:
    pass

# ....................... #

try:
    from .redlock import RedlockConfig, RedlockMixin

    class _Redlock(BaseDocumentABC, RedlockMixin):
        mixin_configs: ClassVar[list[Any]] = [RedlockConfig()]

        # ....................... #

        def __init_subclass__(cls, **kwargs):
            """Initialize subclass"""

            super().__init_subclass__(**kwargs)

            cls.defer_config_patch(
                config_type=RedlockConfig,
                dynamic_field="collection",
                compute_fn=lambda cls: f"{cls.config.database}-{cls.config.collection}",
            )

        # ....................... #

        @contextmanager
        def lock(
            self,
            timeout: int = 10,
            extend_interval: int = 5,
            auto_extend: bool = True,
        ):
            """
            Lock entity instance with automatic extension

            Args:
                timeout (int, optional): The timeout for the lock in seconds. Defaults to 10.
                extend_interval (int, optional): The interval to extend the lock in seconds. Defaults to 5.
                auto_extend (bool, optional): Whether to automatically extend the lock. Defaults to True.

            Yields:
                result (bool): True if the lock was acquired, False otherwise.

            Raises:
                Conflict: If the lock already exists.
                InternalError: If the timeout or extend_interval is not greater than 0 or extend_interval is not less than timeout or the lock aquisition or extension fails.
            """

            with self.redlock_cls(
                id_=str(self.id),
                timeout=timeout,
                extend_interval=extend_interval,
                auto_extend=auto_extend,
            ) as res:
                yield res

        # ....................... #

        @asynccontextmanager
        async def alock(
            self,
            timeout: int = 10,
            extend_interval: int = 5,
            auto_extend: bool = True,
        ):
            """
            Lock entity instance with automatic extension

            Args:
                timeout (int, optional): The timeout for the lock in seconds. Defaults to 10.
                extend_interval (int, optional): The interval to extend the lock in seconds. Defaults to 5.
                auto_extend (bool, optional): Whether to automatically extend the lock. Defaults to True.

            Yields:
                result (bool): True if the lock was acquired, False otherwise.

            Raises:
                Conflict: If the lock already exists.
                InternalError: If the timeout or extend_interval is not greater than 0 or extend_interval is not less than timeout or the lock aquisition or extension fails.
            """

            async with self.aredlock_cls(
                id_=str(self.id),
                timeout=timeout,
                extend_interval=extend_interval,
                auto_extend=auto_extend,
            ) as res:
                yield res

except ImportError:
    pass

# ....................... #

try:
    from .rabbitmq import RabbitMQConfig, RabbitMQMixin

    class _RabbitMQ(BaseDocumentABC, RabbitMQMixin):
        mixin_configs: ClassVar[list[Any]] = [RabbitMQConfig()]

        # ....................... #

        def __init_subclass__(cls, **kwargs):
            """Initialize subclass"""

            super().__init_subclass__(**kwargs)

            cls.defer_config_patch(
                config_type=RabbitMQConfig,
                dynamic_field="queue",
                compute_fn=lambda cls: f"{cls.config.database}-{cls.config.collection}",
            )

except ImportError:
    pass
