from __future__ import annotations

from contextlib import asynccontextmanager
from math import inf
from typing import AsyncIterator
from typing import Callable
from typing import TypeVar

from trio import MemoryReceiveChannel
from trio import open_memory_channel
from trio import sleep

T = TypeVar('T')

C = Callable[[float], float]


@asynccontextmanager
async def rubinetto(r: MemoryReceiveChannel[T],
                    buffer_threshold: int = 10,
                    initial_velocity: float = 1.,
                    accelerate: C = lambda v: min(100, v * 2),
                    brake: C = lambda v: max(1, v / 2)
                    ) -> AsyncIterator[MemoryReceiveChannel[T]]:
    '''simple "faucet" to regulate the "messages per seconds"

    relies on channel statistics to keep the speed of the data flow constrained

    @param r: the "source" channel
    @param buffer_threshold: the threshold upon wich accelerate or brake
    @param initial_velocity: the initial velocity
    @param accelerate: step function to increase the velocity of the flow
    @param brake: step function to decrease the velocity of the flow
    @return: a new channel, with speed costrained
    '''

    s_2, r_2 = open_memory_channel[T](inf)

    yield r_2

    async with r, s_2:
        first = True
        v = initial_velocity
        async for i in r:
            if first:
                first = False
            else:
                current_buffer_used = r.statistics().current_buffer_used

                if current_buffer_used < buffer_threshold:
                    v = brake(v)
                else:
                    v = accelerate(v)

                await sleep(1. / v)

            await s_2.send(i)
