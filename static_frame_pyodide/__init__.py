import sys
import asyncio

__version__ = '0.1.7'

_SF = '1.4.5'
_AK = '0.4.8'
_AM = '0.1.9'

_EMS = '3_1_32' # emscripten version
_URL = 'https://flexatone.s3.us-west-1.amazonaws.com/packages/'

_MODULE = sys.modules[__name__]

async def _micropip_and_import() -> bool:

    micropip = __import__('micropip')

    await micropip.install([
        'sqlite3',
        f'{_URL}arraymap-{_AM}-cp311-cp311-emscripten_{_EMS}_wasm32.whl',
        f'{_URL}arraykit-{_AK}-cp311-cp311-emscripten_{_EMS}_wasm32.whl',
        f'static-frame=={_SF}',
        ])

    try:
        sf = __import__('static_frame')
    except ModuleNotFoundError:
        print("Cannot import statc-frame into this namespace, try `import static_frame as sf`")
        sf = None

    if sf:
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
    loop.create_task(asyncio.wait_for(_micropip_and_import(), None))
else:
    asyncio.run(_micropip_and_import())



# new_loop = asyncio.new_event_loop()
# new_loop.run_until_complete(_micropip_and_import())

# loop.create_task(_schedule_and_await(loop))

# for coro in asyncio.as_completed((_micropip_and_import(),)):
#     # loop.create_task(coro)
#     print(coro)

# def finished(_):
#     print('finished')
# future = asyncio.run_coroutine_threadsafe(_micropip_and_import(), loop)
# future.add_done_callback(finished)
# assert future.result(20) == True

# loop.call_soon(_micropip_and_import())

# import threading
# def target():
#     return asyncio.run(_micropip_and_import())
# t = threading.Thread(target=target)
# t.start()
# t.join()
