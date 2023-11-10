# Encapsulation

[Pyhon](../external_conventions/python.md), although being an object-oriented programming language, does not enforce
encapsulation. However, Python does have some naming convnetions that help us implement encapsulation in our code.

> To indicate an artifact or identifier as protected, prefix it with a single underscore "_".

> To indicate an artifact or identifier as private, prefix it with a double underscore "__".
 

Identifiers and artifacts such as variables, functions, classes, scripts and components, prefixed an underscore, 
shall not be accessed from outside their scope, though, they can be accessed freely from inside it.


## Examples:

### Within a class
```python
class MyClass:
    def __init__(self):
        self.public_attribute = 1
        self._protected_attribute = 2
        self.__private_attribute = 3

    def public_method(self):
        pass

    def _protected_method(self):
        pass

    def __private_method(self):
        pass

instance = MyClass()
# bad:
instance._protected_method()
instance.__private_attribute = 4

# good:
instance.public_method()
instance.public_attribute = 5
```

Inside scripts:

```python
# ~any_script.py

def public_function():
    # good:
    _protected_function()
    
def _protected_function():
    pass

```

```python
# ~main.py

# bad:
from my_functionality import _protected_function
_protected_function()

# good:
from my_functionality import public_function
public_function()
```
Scripts and Components:
```text
├── component/
│   ├── public_sub_component/
│   │   ├── __init__.py
│   │   ├── _internal_script1.py
│   │   └── _internal_script2.py
│   ├── _private_sub_component/
│   │   ├── __init__.py
│   │   ├── _internal_script1.py
│   │   └── _internal_script2.py
│   ├── __init__.py
│   └── _internal_script.py
└── main.py
```

```python
# ~main.py

# bad:
from component._private_sub_component import ...

# good:
from component.public_sub_component import ...
```

```python
# ~component/_internal_script.py

# bad:
from .public_sub_component._internal_script1 import ...

# good:
from ._private_sub_component import ...
from .public_sub_component import ...
from ._internal_script1 import ...
```

```python
# ~component/public_sub_component/_internal_script1.py

# bad:
from ..private_sub_component._internal_script1 import ...

# good:
from ._internal_script2 import ...
from .._private_sub_component import ...
```
