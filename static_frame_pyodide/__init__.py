import sys
import asyncio

__version__ = '0.1.4'
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
    await asyncio.sleep(0)
    sf = __import__('static_frame')
    for name in dir(sf):
        if not name.startswith('_'):
            setattr(sys.modules[__name__], name, getattr(sf, name))

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = None

if loop and loop.is_running():
    print('loop already running')
    loop.create_task(_load())
else:
    print('starting new event loop')
    asyncio.run(_load())

# delegate interface
# attempt = 3
# while attempt > 0:
#     try:
#         from static_frame import *
#         break
#     except ModuleNotFoundError:
#         attempt -= 1

