import sys
import asyncio

__version__ = '0.1.5'
_SF = '1.4.5'
_AK = '0.4.8'
_AM = '0.1.9'
_EMS = '3_1_32' # emscripten version
_URL = 'https://flexatone.s3.us-west-1.amazonaws.com/packages/'


_MODULE = sys.modules[__name__]

# relevant:
# https://ipython.readthedocs.io/en/stable/interactive/autoawait.html

async def _micropip_and_import() -> bool:
    print('micropiping modules')
    import micropip

    await micropip.install([
        'sqlite3',
        f'{_URL}arraymap-{_AM}-cp311-cp311-emscripten_{_EMS}_wasm32.whl',
        f'{_URL}arraykit-{_AK}-cp311-cp311-emscripten_{_EMS}_wasm32.whl',
        ])

    await micropip.install(f'static-frame=={_SF}')
    sf = __import__('static_frame')
    for name in dir(sf):
        if not name.startswith('_'):
            setattr(_MODULE, name, getattr(sf, name))
            print('set', name)
    await asyncio.sleep(0)

async def _schedule_and_await(loop):
    task = loop.create_task(_micropip_and_import())
    await task

# async def _schedule_and_await(loop):
#     await asyncio.wait_for(_micropip_and_import(), None)
#     print('post wait-for')

# async def _schedule_and_await(loop):
#     await loop.run_in_executor(None, _micropip_and_import())

#-------------------------------------------------------------------------------
if sys.platform != 'emscripten':
    raise RuntimeError('This package is only for use in emscripten environments')

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = None

if loop and loop.is_running():
    print('loop already running')

    # new_loop = asyncio.new_event_loop()
    # new_loop.run_until_complete(_micropip_and_import())

    # loop.create_task(_schedule_and_await(loop))

    # task = loop.create_task(_micropip_and_import())
    # assert task.result() == True

    # for coro in asyncio.as_completed((_micropip_and_import(),)):
    #     # loop.create_task(coro)
    #     print(coro)

    # this always times out and does not run
    # future = asyncio.run_coroutine_threadsafe(_micropip_and_import(), loop)
    # assert future.result(20) == True
    # loop.call_soon(_micropip_and_import())

else:
    print('starting new event loop')
    asyncio.run(_micropip_and_import())



