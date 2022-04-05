#!/usr/bin/env python

from __future__ import annotations

from math import inf

from trio import MemoryReceiveChannel
from trio import MemorySendChannel
from trio import open_memory_channel
from trio import open_nursery
from trio import run
from trio import sleep

from rubinetto import rubinetto


async def producer(s: MemorySendChannel[int]) -> None:
    'write 100 messages at ~10 msg/sec'

    async with s:
        for i in range(100):
            await sleep(.1)
            await s.send(i)


async def consumer(r: MemoryReceiveChannel[int]) -> None:
    'dumb consumer'

    async with r:
        async for i in r:
            print(i)


async def main() -> None:
    s, r = open_memory_channel[int](inf)
    async with open_nursery() as nursery, rubinetto(r) as faucet:
        nursery.start_soon(producer, s)
        nursery.start_soon(consumer, faucet)

if __name__ == '__main__':
    run(main)
