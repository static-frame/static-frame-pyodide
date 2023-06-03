import sys
import asyncio

_SF = '1.4.5'
__version__ = '0.1.2'

if sys.platform != 'emscripten':
    raise RuntimeError('This package is only for use in emscripten environments')

_URL = 'https://flexatone.s3.us-west-1.amazonaws.com/packages/'

async def _load():
    print('micropiping modules')
    import micropip
    await micropip.install('sqlite3',
    f'{_URL}arraymap-0.1.9-cp311-cp311-emscripten_3_1_32_wasm32.whl',
    f'{_URL}arraykit-0.4.8-cp311-cp311-emscripten_3_1_32_wasm32.whl')
    await micropip.install('static-frame==1.4.5')

asyncio.run(_load())
# delegate interface
from static_frame import *

