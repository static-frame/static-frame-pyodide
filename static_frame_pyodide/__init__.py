import sys
import asyncio

__version__ = '0.1.3'
_SF = '1.4.5'
_AK = '0.4.8'
_AM = '0.1.9'
_EMS = '3_1_32' # emscripten version

if sys.platform != 'emscripten':
    raise RuntimeError('This package is only for use in emscripten environments')

_URL = 'https://flexatone.s3.us-west-1.amazonaws.com/packages/'

async def _load():
    print('micropiping modules')
    import micropip

    await micropip.install([
        'sqlite3',
        f'{_URL}arraymap-{_AM}-cp311-cp311-emscripten_{_EMS}_wasm32.whl',
        f'{_URL}arraykit-{_AK}-cp311-cp311-emscripten_{_EMS}_wasm32.whl',
        ])

    await micropip.install(f'static-frame=={_SF}')

async def _add_task(loop):
    task = loop.create_task(_load())
    await task


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = None

if loop and loop.is_running():
    print('loop already running')
    asyncio.run_coroutine_threadsafe(_add_task(loop), loop)
    # loop.run_until_complete(_add_task(loop))
    # asyncio.run_coroutine(_add_task(loop), loop)

else:
    print('starting new event loop')
    asyncio.run(_load())

# delegate interface
from static_frame import *

