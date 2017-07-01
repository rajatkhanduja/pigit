Pigit
--------------------------

Pigit is both a git library for Python and a git-client written entirely in Python.

Moreover, the motivation behind Pigit was to create git in a way modular way, allowing for use of other backends (like SQLite or MySQL or anything else) to store the objects and references. It is essentially an exercise in exploring the core fundamentals of git and identifying separable components, allowing for custom tools to be built on top. See the end of the document for more details on possible add-ons.


##Using as a library##

All of these can also be found in `demo.py`

- Importing Pigit

```python
from pigit import Pigit
```

`Pigit` class exposes several key ways to create a `Repository` object, which allows various interactions with the repository.


- Different ways to initialize a repository

```python
from pigit import Pigit
from pathlib import Path

# Initialize a bare repository
repo = Pigit.init(Path('/tmp/project'))

# Initialize repository object from an existing repository on local system
repo = Pigit.repo(Path('/tmp/project'))

```