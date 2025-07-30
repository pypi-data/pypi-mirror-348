# TurtleShell

Convenience wrapper around Python turtle standard library.

## Development
Do all this in a virtual environment, e.g.
```
python3 -m venv venv
./venv/bin/activate
```

Test changes:
```
pip install pytest
pytest
```

Push changes.

Update package version:
```
pip install bumpver
bumpver update --minor
```

Build and check package with twine:
```
pip install build twine
python -m build
twine check dist/*
```

Upload to Test PyPI, install, and test:
```
twine upload -r testpypi dist/*
pip install -i https://test.pypi.org/simple turtleshell
```

Upload to PyPI:
```
twine upload dist/*
```
