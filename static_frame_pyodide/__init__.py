import sys
import asyncio

_SF = '1.4.5'
__version__ = '0.1.3'

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


try:
    loop = asyncio.get_running_loop()
except RuntimeError:  # 'RuntimeError: There is no current event loop...'
    loop = None

if loop and loop.is_running():
    print('Async event loop already running. Adding coroutine to the event loop.')
    task = loop.create_task(_load())
else:
    print('Starting new event loop')
    asyncio.run(_load())

# asyncio.run(_load())
# delegate interface
from static_frame import *

