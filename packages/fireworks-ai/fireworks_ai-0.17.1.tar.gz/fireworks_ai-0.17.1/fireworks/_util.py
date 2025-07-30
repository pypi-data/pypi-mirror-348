import asyncio
from typing import Coroutine, Any, TypeVar

T = TypeVar("T")


def run_coroutine_in_appropriate_loop(coro: Coroutine[Any, Any, T]) -> T:
    """
    Runs a coroutine in the appropriate event loop context and returns its result.

    This handles three cases:
    1. Inside a running event loop - creates a future and waits for it
    2. Event loop exists but not running - runs until complete
    3. No event loop available - creates a new one with asyncio.run

    Returns:
        The result of the coroutine
    """
    # Try to run the coroutine in the current event loop if possible
    loop = asyncio.get_event_loop()
    if loop.is_running():
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        return future.result()
    else:
        # If we're not in an async context, we can run until complete
        return loop.run_until_complete(coro)
