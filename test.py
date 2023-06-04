import sys
import asyncio
from contextlib import contextmanager
from unittest.mock import patch



class MockMicropip:
    @staticmethod
    async def install(*args, **kwargs):
        print(args)
        await asyncio.sleep(0)

class MockStaticFrame:
    pass

@contextmanager
def mock_modules():
    sys.modules['micropip'] = MockMicropip
    sys.modules['static_frame'] = MockStaticFrame
    try:
        yield
    finally:
        del sys.modules['micropip']
        del sys.modules['static_frame']


@patch('sys.platform', 'emscripten')
def test_new_loop():
    with mock_modules():
        import static_frame_pyodide as sfpyo
        print(sfpyo)



if __name__ == '__main__':
    test_new_loop()



