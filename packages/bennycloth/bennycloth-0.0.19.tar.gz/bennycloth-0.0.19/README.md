# BennyCloth

The name BennyCloth is a combination of **Benny** the Beaver and a **synonym for Canvas**, whose [REST API](https://canvas.instructure.com/doc/api/index.html) was the means for delivering homework assignments, randomized using many of the functions in this package.

BennyCloth is available on [pypi](https://pypi.org/project/bennycloth/).

## Packages

+ `loads`
+ `steel`
+ `concrete`
+ `wood`
+ `canvas`
+ `matrix`
+ `beaverFrame`
+ `images`

### Local Development

To install locally in development mode:
```bash
pip install -e .
```
The `-e` option updates the package automatically everytime a source file is changed.

### Upload to pypi

1. bump verson number in `setup.py`, e.g., 0.0.12
2. `rm dist/bennycloth-<old versions>*`
3. `python3 -m build --sdist`
4. `python3 -m build --wheel`
5. `twine check dist/bennycloth-0.0.12*`
6. `twine upload --repository bennycloth dist/bennycloth-0.0.12*`

### pypi Tutorials

Tutorials used in figuring out how to make a Python package then deploy it to [pypi](https://pypi.org/):

+ https://towardsdatascience.com/create-your-own-python-package-and-publish-it-into-pypi-9306a29bc116

+ https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/

+ https://packaging.python.org/en/latest/tutorials/packaging-projects/

+ https://www.freecodecamp.org/news/how-to-create-and-upload-your-first-python-package-to-pypi/

+ https://www.freecodecamp.org/news/build-your-first-python-package/

+ https://medium.com/@udiyosovzon/things-you-should-know-when-developing-python-package-5fefc1ea3606
