# COMPAS Triangle

COMPAS-firendly wrappers for the Triangle library.

## Getting Started

`compas_triangle` can be installed from local source using pip.

```bash
pip install path/to/compas_triangle
```

or directly from the github repo

```bash
pip install git+https://github.com/blockresearchgroup/compas_triangle.git#egg=compas_triangle
```

## Examples

Four examples are available:

* examples/delaunay1.py
* examples/delaunay2.py
* examples/delaunay3.py
* examples/delaunay4_rhino.py

Note that the Rhino example uses `compas.rpc` to provide a proxy for the package.

## License

`compas_triangle` uses the Cython wrapper for Jonathan Richard Shewchuk's Triangle library.
The Cython wrapper is available here: https://github.com/drufat/triangle

Use of the Triangle library is restricted to personal or academic purposes.
The license of the library is included in this repo: [LICENSE.Triangle](LICENSE.Triangle)
