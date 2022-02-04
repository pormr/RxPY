from typing import Callable, Optional, TypeVar

from rx.core import Observable, abc
from rx.internal import ArgumentOutOfRangeException

_T = TypeVar("_T")


def _skip(count: int) -> Callable[[Observable[_T]], Observable[_T]]:
    if count < 0:
        raise ArgumentOutOfRangeException()

    def skip(source: Observable[_T]) -> Observable[_T]:
        """The skip operator.

        Bypasses a specified number of elements in an observable sequence
        and then returns the remaining elements.

        Args:
            source: The source observable.

        Returns:
            An observable sequence that contains the elements that occur
            after the specified index in the input sequence.
        """

        def subscribe(
            observer: abc.ObserverBase[_T],
            scheduler: Optional[abc.SchedulerBase] = None,
        ):
            remaining = count

            def on_next(value: _T) -> None:
                nonlocal remaining

                if remaining <= 0:
                    observer.on_next(value)
                else:
                    remaining -= 1

            return source.subscribe_(
                on_next, observer.on_error, observer.on_completed, scheduler
            )

        return Observable(subscribe)

    return skip


__all__ = ["_skip"]
