# static-frame-pyodide
[StaticFrame](https://github.com/static-frame/static-frame) packaged for use in Pyodide, PyScript, and WebAssembly/Emscripten environments.

This package, on import, uses `micropip` to install versions of StaticFrame dependencies (`arraykit` and `arraymap`) compiled for Emscripten, and then delegates the StaticFrame API to this module.

## Usage in Pyodide:

Try StaticFrame in Pyodide here: https://pyodide.org/en/stable/console.html

```python-repl
>>> import micropip; await micropip.install('static-frame-pyodide')
>>> import static_frame_pyodide as sf
```

While ``pyodide.http.open_url()`` will not work with any URL, it works with the sample provided by the
[``pyscript-ice-cream``](https://github.com/Cheukting/pyscript-ice-cream) project.


![Pyodide screen shot](https://github.com/static-frame/static-frame-pyodide/blob/main/doc/sf-pyodide.png)


