from quart import websocket
from quart_trio import QuartTrio
from json import loads
from os.path import join
from vosk import KaldiRecognizer
from vosk import Model


class Qrt(QuartTrio):
    def __init__(self) -> None:
        super().__init__(__name__, static_url_path='')

        @self.websocket('/ws/<samplerate>')
        async def ws(samplerate: str='44100') -> None:
            await websocket.accept()

            rec = KaldiRecognizer(Model(join(__file__, '..', 'model')),
                                  int(samplerate))

            while True:
                data = await websocket.receive()

                if rec.AcceptWaveform(data):
                    await websocket.send_json(loads(rec.FinalResult()))
