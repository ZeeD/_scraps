from types import TracebackType
from typing import Callable
from typing import Literal
from typing import Optional
from typing import TypedDict
from typing import Union

from _cffi_backend import _CDataBase
from _cffi_backend import buffer

class CallbackFlags:
    ...


class RawInputStream:
    def __init__(self,
                 samplerate: Optional[int]=None,
                 blocksize: Optional[int]=None,
                 dtype: Optional[str]=None,
                 channels: Optional[int]=None,
                 callback: Optional[Callable[[buffer, int, _CDataBase, CallbackFlags], None]]=None):
        ...

    def __enter__(self) -> 'RawInputStream':
        return self

    def __exit__(self, t: Optional[type[BaseException]] = ...,
                 value: Optional[BaseException] = ...,
                 traceback: Optional[TracebackType] = ...) -> bool:
        ...


class _QueryDevices(TypedDict):
    name: str
    hostapi: str
    max_input_channels: int
    max_output_channels: int
    default_low_input_latency: int
    default_low_output_latency: int
    default_high_input_latency: int
    default_high_output_latency: int
    default_samplerate: int


def query_devices(device: Optional[Union[int, str]]=None,
                  kind: Optional[Literal['input', 'output']]=None) -> _QueryDevices:
    ...
