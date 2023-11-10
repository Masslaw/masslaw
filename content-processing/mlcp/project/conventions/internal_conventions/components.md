# MLCP Component Construction Conventions

> In the context of this project, a "component" is equivilent to a "module" in Python.

To improve the maintainability, modularity, testability and simplicity of the MLCP, the codebase is divided into
components. Each component implements its own functionality and is responsible for a specific part of the MLCP's
functionality.

## Component Hierarchy

Components exist in a hierarchy of parent components and subcomponents.

The components highest in the hierarchy are the ones that implement the different layers of the MLCP (
see [MLCP Implementation](../../../src/mlcp_implementation.md) to know more about the layered architecture of the mlcp)

If a component is responsible for a part in the high-level functionality of the MLCPs functionality, it should be
implemented as a subcomponent (first child) of the component that represents the layer of which it is a part of.

Components may implement subcomponents of their own. Both to divide their functionality into smaller independent parts
and/or implement internal functionality of their own.

## Component Structure

### Encapsulation and Interface

Every component shall implement a well-defined interface that exposes its functionality to other components.
This interface shall be as small and concise as possible, while still exposing all the functionality that the 
component is designed to expose.

To define the interface of a component, the component will use and implement [encapsulation conventions](./encapsulation.md).
The internal modules of a component, containing inner functionality, will be protected or private. The artifacts that are
meant to be exposed to other components will be public - those will act as the interface of the component.

### Implementation Conventions

#### Subcomponents

A component can expose subcomponents as part of its interface. Every subcomponent not considered as private can and will
be part of the component's interface.
When a component is part of its parent's interface, its own interface is considered part of its parent's interface.

> Subcomponents can both be public and protected. Private subcomponents are not considered part of the interface of a
> component, they only serve the component's internal functionality.

#### Classes, Functions And Variables

These are the lowest level parts of a component's interface. They are the functional entry point for a component's
internal functionality.

Classes, Functions And Variables are implemented within scripts. Though, we forbid importing from a component's internal
scripts directly.

To expose identifiers that act as a component's interface, implemented in the component's internal scripts, import the
identifier from the protected script in the component's `__init__.py` script, and specify it as importable by including 
it in the `__all__ = [...]` list within the `__init__.py` script

This way, all importable identifiers will be listed in the component's `__init__.py` script.

> scripts - shall always be protected, denoted with the single underscore "_" prefix, importing from a component's
> internal script directly is forbidden.


#### Scripts (Anyway)

As mentioned in the previous section, scripts shall always be protected, and importing from them directly is forbidden.

Though, we might find ourselves needing to expose the contents of entire scripts to other components. Such as exposing
a large collection of unscoped utility functions implemented in a script. We can't go over them one by one and expose
them separately as part of the component's interface, that would not be idle.

In these cases, we would rather expose the whole script as a single namespace, containing these individual functions.

To do this correctly, we will import the entire script as a module, and using the `as` keyword rename it as an identifier 
turning its name from being written in snake_case to being written in CamelCase without the underscored prefix, 
and specify it as importable by including it in the `__all__ = [...]` list within the `__init__.py` script of the component.
See [this example](#exposing-a-script-as-a-namespace)

#### \_\_init__.py



As mentioned in the [previous section](#classes-functions-and-variables) - the `__init__.py` script of a component will
hold the list of all the identifiers importable by a component via `__all__ = [...]`

We also require that the `__init__.py` script will not hold or implement anything other than this.

That way, the sole purpose of the `__init__.py` script of a component, is to specify its interface.

--------

> The reason we are so strict with these requirements is very simple - by implementing this set of conventions a 
> developer can imminently know what a component's interface is made out of. This is useful, both from the perspective 
> of a developer that is using the component externally, and from the perspective of a developer working on that component.
> 
> When working on a component's implementation, it is very useful to both **decide** and **know** exactly where external
> access to its internal functionality can be made.

--------

## Examples

### Component Structure

```text
# Bad: 
├── component/
│   ├── _public_sub_component/
│   │   ├── __init__.py
│   │   └── internal_script.py
│   ├── private_sub_component/
│   │   ├── __init__.py
│   │   └── internal_script.py
│   ├── __init__.py
│   └── internal_script.py
└── main.py


# Good: 
├── component/
│   ├── public_sub_component/
│   │   ├── __init__.py
│   │   └── _internal_script.py
│   ├── _private_sub_component/
│   │   ├── __init__.py
│   │   └── _internal_script.py
│   ├── __init__.py
│   └── _internal_script.txt
└── main.py
```

### Component Interface

```python
# Bad:
# ~component/__init__.py

class MyClass:
    ...

def my_function():
    ...


# Good:
# ~component/_internal_script.py

class MyClass:
    ...

def my_function():
    ...
```

```python
# ~component/__init__.py

from ._internal_script import MyClass, my_function

__all__ = [
    'MyClass',
    'my_function',
]
```

### Exposing a Script as a Namespace

```text
└── utility_component/
    ├── __init__.py
    └── _utility_functions.py
```

```python
# ~utility_component/_utility_functions.py

def utility_function1():
    ...


def utility_function2():
    ...


def utility_function3():
    ...
```

```python
# ~utility_component/__init__.py
from . import _utility_functions as UtilityFunctions

__all__ = [
    ...,
    "UtilityFunctions"
]
```
