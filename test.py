import sys
import asyncio
from contextlib import contextmanager
from unittest.mock import patch

# import micropip; await micropip.install('static-frame-pyodide==0.1.5'); import static_frame_pyodide as sf; print(dir(sf))

class MockMicropip:
    @staticmethod
    async def install(*args, **kwargs):
        print(args)
        await asyncio.sleep(0)

class MockStaticFrame:
    Frame = 0
    Series = 1


@contextmanager
def mock_modules():
    sys.modules['micropip'] = MockMicropip
    sys.modules['static_frame'] = MockStaticFrame
    try:
        yield
    finally:
        del sys.modules['micropip']
        del sys.modules['static_frame']
        if 'static_frame_pyodide' in sys.modules:
            del sys.modules['static_frame_pyodide']


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
            await asyncio.sleep(0)
            assert sfpyo.Frame == MockStaticFrame.Frame
            assert sfpyo.Series == MockStaticFrame.Series

        async def f():
            await g()

        asyncio.run(f())

if __name__ == '__main__':
    # test_new_loop()
    test_found_loop()




