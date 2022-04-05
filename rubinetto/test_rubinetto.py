from __future__ import annotations
from trio import MemoryReceiveChannel

from rubinetto import rubinetto
from unittest.mock import Mock

async def test_rubinetto_empty() -> None:
    'when there are no incoming messages nothing should come out'

    r: MemoryReceiveChannel[int] = Mock()

    async with rubinetto(r) as faucet:
        async for _ in faucet:
            assert False
