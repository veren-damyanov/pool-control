"""Asyncio related utilities."""

import asyncio


class LoopCloseTimeout(Exception):
    pass


async def all_tasks_to_close(interval=0.1, timeout=2.0):
    elapsed = 0.0
    while len(asyncio.all_tasks()) > 1:  # the last task remaining is me ;)
        await asyncio.sleep(interval)
        elapsed += interval
        if elapsed > timeout:
            raise LoopCloseTimeout(f'elapsed time {elapsed} sec.')
