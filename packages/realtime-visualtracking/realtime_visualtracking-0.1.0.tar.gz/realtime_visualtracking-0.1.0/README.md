## How to publish this package:

1. Create distribution files:
    pip install setuptools wheel
2. Generate the files:
    python setup.py sdist bdist_wheel
3. Installer the Twine para send the package:
    pip install twine
4. Send package to pyPip
    twine upload dist/*
