import sys
import asyncio
from contextlib import contextmanager
from unittest.mock import patch

# import micropip; await micropip.install('static-frame-pyodide==0.1.5'); import static_frame_pyodide as sf; print(dir(sf))
class MockStaticFrame:
    Frame = 0
    Series = 1

class MockMicropip:
    @staticmethod
    async def install(arg):
        # print(arg)
        name = arg if isinstance(arg, str) else arg[-1]
        if name.startswith('static-frame'):
            sys.modules['static_frame'] = MockStaticFrame
        await asyncio.sleep(0)


@contextmanager
def mock_modules():
    sys.modules['micropip'] = MockMicropip
    try:
        yield
    finally:
        for mod in ('micropip', 'static_frame', 'static_frame_pyodide'):
            if mod in sys.modules:
                del sys.modules[mod]


@patch('sys.platform', 'emscripten')
def test_new_loop():
    with mock_modules():
        import static_frame_pyodide as sfpyo
        assert sfpyo.Frame == MockStaticFrame.Frame
        assert sfpyo.Series == MockStaticFrame.Series


@patch('sys.platform', 'emscripten')
def test_found_loop():
    with mock_modules():

        async def g():
            import static_frame_pyodide as sfpyo
            await asyncio.sleep(1) # necessary
            assert sfpyo.Frame == MockStaticFrame.Frame
            assert sfpyo.Series == MockStaticFrame.Series

        async def f():
            await g()

        asyncio.run(f())

if __name__ == '__main__':
    test_new_loop()
    test_found_loop()




