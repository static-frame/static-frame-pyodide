import sys
import asyncio

__version__ = '0.1.5'

_SF = '1.4.5'
_AK = '0.4.8'
_AM = '0.1.9'

_EMS = '3_1_32' # emscripten version
_URL = 'https://flexatone.s3.us-west-1.amazonaws.com/packages/'

_MODULE = sys.modules[__name__]

async def _micropip_and_import() -> bool:
    print('micropiping')

    micropip = __import__('micropip')

    await asyncio.wait_for(micropip.install([
        'sqlite3',
        f'{_URL}arraymap-{_AM}-cp311-cp311-emscripten_{_EMS}_wasm32.whl',
        f'{_URL}arraykit-{_AK}-cp311-cp311-emscripten_{_EMS}_wasm32.whl',
        ]),
        None)

    await asyncio.wait_for(
        micropip.install(f'static-frame=={_SF}'),
        None)

    sf = __import__('static_frame')

    for name in dir(sf):
        if not name.startswith('_'):
            setattr(_MODULE, name, getattr(sf, name))

#-------------------------------------------------------------------------------
if sys.platform != 'emscripten':
    raise RuntimeError('This package is only for use in emscripten environments')

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = None

if loop and loop.is_running():
    print('loop already running')

    def target():
        return asyncio.run(_micropip_and_import())

    import threading
    t = threading.Thread(target=target)
    t.start()
    t.join()

else:
    print('starting new event loop')
    asyncio.run(_micropip_and_import())



