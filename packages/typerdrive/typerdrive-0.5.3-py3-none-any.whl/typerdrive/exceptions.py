from traceback import format_tb
from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

import snick
import typer
from buzz import Buzz, DoExceptParams, get_traceback, reformat_exception
from loguru import logger
from rich import traceback

from typerdrive.constants import ExitCode
from typerdrive.format import terminal_message
from typerdrive.format import strip_rich_style

traceback.install()


class TyperdriveError(Buzz):
    subject: str | None = None
    footer: str | None = None
    exit_code: ExitCode = ExitCode.GENERAL_ERROR
    details: Any | None = None

    def __init__(
        self,
        *args: Any,
        subject: str | None = None,
        footer: str | None = None,
        details: Any | None = None,
        exit_code: ExitCode | None = None,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        if subject:
            self.subject = subject
        if footer:
            self.footer = footer
        if details:
            self.details = details
        if exit_code:
            self.exit_code = exit_code


class ContextError(TyperdriveError):
    exit_code: ExitCode = ExitCode.INTERNAL_ERROR


class BuildCommandError(TyperdriveError):
    exit_code: ExitCode = ExitCode.INTERNAL_ERROR


P = ParamSpec("P")
T = TypeVar("T")
WrappedFunction = Callable[P, T]


def handle_errors(
    base_message: str,
    *,
    handle_exc_class: type[Exception] | tuple[type[Exception], ...] = TyperdriveError,
    ignore_exc_class: type[Exception] | tuple[type[Exception], ...] | None = None,
    do_except: Callable[[DoExceptParams], None] | None = None,
    do_else: Callable[[], None] | None = None,
    do_finally: Callable[[], None] | None = None,
    unwrap_message: bool = True,
    debug: bool = False,
) -> Callable[[WrappedFunction[P, T]], WrappedFunction[P, T]]:
    class _DefaultIgnoreException(Exception):
        """
        Define a special exception class to use for the default ignore behavior.

        Basically, this exception type can't be extracted from this method (easily), and thus could never actually
        be raised in any other context. This is only created here to preserve the `try/except/except/else/finally`
        structure.
        """

    ignore_exc_class = _DefaultIgnoreException if ignore_exc_class is None else ignore_exc_class

    def _decorate(func: WrappedFunction[P, T]) -> WrappedFunction[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return_value: T | None = None
            try:
                return_value = func(*args, **kwargs)
            except ignore_exc_class:
                raise
            except handle_exc_class as err:
                try:
                    final_message = reformat_exception(base_message, err)
                except Exception as msg_err:
                    raise RuntimeError(f"Failed while formatting message: {repr(msg_err)}")

                trace = get_traceback()

                if do_except:
                    do_except(
                        DoExceptParams(
                            err=err,
                            base_message=base_message,
                            final_message=final_message,
                            trace=trace,
                        )
                    )

                subject: str | None = base_message
                footer: str | None = None
                message: str

                exit_code: int = ExitCode.GENERAL_ERROR
                if isinstance(err, TyperdriveError):
                    if err.subject:
                        subject = err.subject
                    if err.footer:
                        footer = err.footer
                    if debug:
                        message = err.message
                    else:
                        message = err.base_message or err.message
                    if unwrap_message:
                        message = snick.unwrap(message)
                    exit_code = err.exit_code
                else:
                    message = str(err)

                terminal_message(
                    message,
                    subject=f"[red]{subject}[/red]",
                    footer=footer,
                    error=True,
                )

                raise typer.Exit(code=exit_code)

            else:
                if do_else:
                    do_else()
                return return_value

            finally:
                if do_finally:
                    do_finally()

        return wrapper

    return _decorate


def log_error(params: DoExceptParams):
    logger.error(
        "\n".join(
            [
                strip_rich_style(params.final_message),
                "--------",
                "Traceback:",
                "".join(format_tb(params.trace)),
            ]
        )
    )
