# static-frame-pyodide
StaticFrame packaged for use in Pyodide, PyScript, and WebAssembly/Emscripten environments.

This package, on import, uses `micropip` to install versions of StaticFrame dependencies (`arraykit` and `arraymap`) compiled for Emscripten.

## Usage in Pyodide:

```python-repl
>>> import micropip; await micropip.install('static-frame-pyodide')
>>> import static_frame_pyodide as sf
```

![Pyodide screen shot]()

