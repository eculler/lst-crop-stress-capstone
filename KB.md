# Knowledge Base

This file is available to capture knowledge related to this project.

## Project structure

How should the project be structured? For this project, which is primarily intended to store a Jupyter Notebook, the following structure is used:

```
*
|--* exploratory/
|--* data/
   |--* inputs/
   |--* outputs/
|--* assets/
|--* library/
   |--* __init__.py
   |--* utils.py
   |--* [other modules as needed]
|--* secrets/
.gitignore
environment.yml
blog.ipynb
blog.html
LICENSE
README.md
KB.md
```

* `library/`: This directory stores modularized code for use in the notebook. This allows the library module to be imported directly (as opposed to a "src layout that would need to be installed).
* `exploratory/`: A place for Jupyter notebooks used in data exploration.
* `assets/`: stores images and gifs used in the final blog
* `secrets/`: store individuals credentials here, so that anyone can run anyone else's code, provided they have input their own credentials in the correct format.

### "Library" as module name

There are as many opinions as options for python project structure, especially for storing local modules. I've seen `bin`, `lib`, `library`, `src`, `local`, `utils` and more explicit names used for local code. For the sake of simplicity we use `library` as the directory name for our modules and `utils.py` for functions and `models.py` for classes, unless a more specific name better captures the purpose of the code within. 

ChatGPT offers these conventions:

* "lib" or "library": These directory names are often used to store reusable code libraries or modules that are specific to your project. It can be a good choice if you have custom code that is not intended to be published as a separate package but is still meant to be reused within your project.
* "local": The "local" directory can be used to store project-specific dependencies or local installations of third-party libraries. This can be useful if you want to keep your project's dependencies isolated from the system-wide Python installation or if you have customized versions of libraries for your project.
* "bin": The "bin" directory is typically used to store executable scripts or command-line utilities associated with your project. If your project includes any standalone scripts or command-line tools, placing them in a "bin" directory can help keep them organized.

We avoid the convention "src" as that should be the directory in which `library/` is nested if we were to package the code for distribution using the [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout).

### Importing `library` in notebooks in the `exploratory` directory

The `library` module can be imported directly like any other package in files in the root of the project directory. However, to import the `library` module in notebooks in the nested `exploratory` directory, first add the project path to the system PATH.

```python
import sys
project_path = os.path.abspath(os.path.join('..'))
if project_path not in sys.path:
    sys.path.append(project_path)
from library import utils
```



