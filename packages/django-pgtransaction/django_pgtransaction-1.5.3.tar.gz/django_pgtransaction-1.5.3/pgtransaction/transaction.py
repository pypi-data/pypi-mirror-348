from __future__ import annotations

from functools import cached_property, wraps
from typing import Any, Callable, Final, Literal, TypeVar, overload

import django
from django.db import DEFAULT_DB_ALIAS, Error, transaction
from django.db.utils import NotSupportedError

from pgtransaction import config

_C = TypeVar("_C", bound=Callable[..., Any])

READ_COMMITTED: Final = "READ COMMITTED"
REPEATABLE_READ: Final = "REPEATABLE READ"
SERIALIZABLE: Final = "SERIALIZABLE"


class Atomic(transaction.Atomic):
    def __init__(
        self,
        using: str | None,
        savepoint: bool,
        durable: bool,
        isolation_level: Literal["READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"] | None,
        retry: int | None,
    ):
        if django.VERSION >= (3, 2):
            super().__init__(using, savepoint, durable)
        else:  # pragma: no cover
            super().__init__(using, savepoint)

        self.isolation_level = isolation_level
        self._retry = retry
        self._used_as_context_manager = True

        if self.isolation_level:  # pragma: no cover
            if self.connection.vendor != "postgresql":
                raise NotSupportedError(
                    f"pgtransaction.atomic cannot be used with {self.connection.vendor}"
                )

            if self.isolation_level.upper() not in (
                READ_COMMITTED,
                REPEATABLE_READ,
                SERIALIZABLE,
            ):
                raise ValueError(f'Invalid isolation level "{self.isolation_level}"')

    @cached_property
    def retry(self) -> int:
        """
        Lazily load the configured retry value

        We do this so that atomic decorators can be instantiated without an
        implicit dependency on Django settings being configured.

        Note that this is not fully thread safe as the cached_property decorator
        can be redundantly called by multiple threads, but there should be no
        adverse effect in this case.
        """
        return self._retry if self._retry is not None else config.retry()

    @property
    def connection(self) -> Any:
        # Don't set this property on the class, otherwise it won't be thread safe
        return transaction.get_connection(self.using)

    def __call__(self, func: _C) -> _C:
        self._used_as_context_manager = False

        @wraps(func)
        def inner(*args: Any, **kwds: Any) -> Any:
            num_retries = 0

            while True:  # pragma: no branch
                try:
                    with self._recreate_cm():
                        return func(*args, **kwds)
                except Error as error:
                    if (
                        error.__cause__.__class__ not in config.retry_exceptions()
                        or num_retries >= self.retry
                    ):
                        raise

                num_retries += 1

        return inner  # type: ignore - we only care about accuracy for the outer method

    def execute_set_isolation_level(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {self.isolation_level.upper()}")

    def __enter__(self) -> None:
        in_nested_atomic_block = self.connection.in_atomic_block

        if in_nested_atomic_block and self.retry:
            raise RuntimeError("Retries are not permitted within a nested atomic transaction")

        if self.retry and self._used_as_context_manager:
            raise RuntimeError(
                "Cannot use pgtransaction.atomic as a context manager "
                "when retry is non-zero. Use as a decorator instead."
            )

        # If we're already in a nested atomic block, try setting the isolation
        # level before any check points are made when entering the atomic decorator.
        # This helps avoid errors and allow people to still nest isolation levels
        # when applicable
        if in_nested_atomic_block and self.isolation_level:
            self.execute_set_isolation_level()

        super().__enter__()

        # If we weren't in a nested atomic block, set the isolation level for the first
        # time after the transaction has been started
        if not in_nested_atomic_block and self.isolation_level:
            self.execute_set_isolation_level()


@overload
def atomic(using: _C) -> _C: ...


@overload
def atomic(
    using: str | None = None,
    savepoint: bool = True,
    durable: bool = False,
    isolation_level: Literal["READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"] | None = None,
    retry: int | None = None,
) -> Atomic: ...


def atomic(
    using: str | None | _C = None,
    savepoint: bool = True,
    durable: bool = False,
    isolation_level: Literal["READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"] | None = None,
    retry: int | None = None,
) -> Atomic | _C:
    """
    Extends `django.db.transaction.atomic` with PostgreSQL functionality.

    Allows one to dynamically set the isolation level when opening a transaction,
    as well as specifying a retry policy for when an operation in that transaction results
    in a Postgres locking exception.

    Args:
        using: The database to use.
        savepoint: If `True`, create a savepoint to roll back.
        durable: If `True`, raise a `RuntimeError` if nested within another atomic block.
        isolation_level: The isolation level we wish to be
            used for the duration of the transaction. If passed in
            as None, the current isolation level is used. Otherwise,
            we must choose from `pgtransaction.READ_COMMITTED`,
            `pgtransaction.REPEATABLE_READ` or `pgtransaction.SERIALIZABLE`.
            Note that the default isolation for a Django project is
            "READ COMMITTED". It is not permitted to pass this value
            as anything but None when using [pgtransaction.atomic][]
            is used as a nested atomic block - in that scenario,
            the isolation level is inherited from the parent transaction.
        retry: An integer specifying the number of attempts
            we want to retry the entire transaction upon encountering
            the settings-specified psycogp2 exceptions. If passed in as
            None, we default to using the settings-specified retry
            policy defined by `settings.PGTRANSACTION_RETRY_EXCEPTIONS` and
            `settings.PGTRANSACTION_RETRY`. Note that it is not possible
            to specify a non-zero value of retry when [pgtransaction.atomic][]
            is used in a nested atomic block or when used as a context manager.

    Example:
        Since [pgtransaction.atomic][] inherits from `django.db.transaction.atomic`, it
        can be used in exactly the same manner. Additionally, when used as a
        context manager or a decorator, one can use it to specify the
        isolation level of the new transaction. For example:

            import pgtransaction

            with pgtransaction.atomic(isolation_level=pgtransaction.REPEATABLE_READ):
                # Isolation level is now "REPEATABLE READ" for the duration of the "with" block.
                ...

        Note that setting `isolation_level` in a nested atomic block is permitted as long
        as no queries have been made.

    Example:
        When used as a decorator, one can also specify a `retry` argument. This
        defines the number of times the transaction will be retried upon encountering
        the exceptions referenced by `settings.PGTRANSACTION_RETRY_EXCEPTIONS`,
        which defaults to
        `(psycopg.errors.SerializationFailure, psycopg.errors.DeadlockDetected)`.
        For example:

            @pgtransaction.atomic(retry=3)
            def update():
                # will retry update function up to 3 times
                # whenever any exception in settings.PGTRANSACTION_RETRY_EXCEPTIONS
                # is encountered. Each retry will open a new transaction (after
                # rollback the previous one).

        Attempting to set a non-zero value for `retry` when using [pgtransaction.atomic][]
        as a context manager will result in a `RuntimeError`.
    """
    # Copies structure of django.db.transaction.atomic
    if callable(using):
        return Atomic(
            DEFAULT_DB_ALIAS,
            savepoint,
            durable,
            isolation_level,
            retry,
        )(using)
    else:
        return Atomic(
            using,
            savepoint,
            durable,
            isolation_level,
            retry,
        )
