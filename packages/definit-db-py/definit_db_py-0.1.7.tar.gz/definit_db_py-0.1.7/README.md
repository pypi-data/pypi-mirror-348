```
(optional cleanup) rm -rf dist/ build/ src/*.egg-info/

python -m build

python -m twine upload dist/*
```