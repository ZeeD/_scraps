from json import dumps
from json import loads
from os.path import join

from quart import websocket
from quart_trio import QuartTrio
from vosk import KaldiRecognizer
from vosk import Model

letters = 'a', 'bi', 'ci', 'di', 'e', 'effe', 'gi', 'acca'
numbers = 'uno', 'due', 'tre', 'quattro', 'cinque', 'sei', 'sette', 'otto'


class Qrt(QuartTrio):
    def __init__(self) -> None:
        super().__init__(__name__, static_url_path='')

        @self.websocket('/ws/<samplerate>')
        async def ws(samplerate: str='44100') -> None:
            await websocket.accept()

            rec = KaldiRecognizer(Model(join(__file__, '..', 'model')),
                                  int(samplerate),
                                  dumps([f'{letter} {number}'
                                         for letter in letters
                                         for number in numbers]))

            while True:
                data = await websocket.receive()

                if rec.AcceptWaveform(data):
                    await websocket.send_json(loads(rec.Result()))
