from json import loads
from os.path import join
from queue import Queue
from sys import stderr

from _cffi_backend import _CDataBase
from _cffi_backend import buffer
from sounddevice import CallbackFlags
from sounddevice import RawInputStream
from sounddevice import query_devices
from vosk import KaldiRecognizer
from vosk import Model


class TestMicrophone:
    def __init__(self) -> None:
        self.q = Queue[bytes]()

    def speech_to_text(self) -> None:
        samplerate = int(query_devices(kind='input')['default_samplerate'])

        with RawInputStream(samplerate=samplerate,
                            blocksize=8000,
                            dtype='int16',
                            channels=1,
                            callback=self.callback):
            rec = KaldiRecognizer(Model(join(__file__, '..', 'model')),
                                  samplerate)

            while True:
                if rec.AcceptWaveform(self.q.get()):
                    print(loads(rec.Result()))

    def callback(self,
                 indata: buffer,
                 frames: int,
                 time: _CDataBase,
                 status: CallbackFlags) -> None:
        if status:
            print(status, file=stderr)
        self.q.put(bytes(indata))
