# Shared Layer

The *shared layer* implements any code that may or may not be used throughout the entire MLCP application.
It is a "layer" that is not part of the layered architecture of the MLCP, but rather a collection of
components and shared generic functionality (not targeting any specific layer or use case) that is used by the
entire MLCP application and any component in it.

----

## Architecture and Design

This component acts as one of the highest level layers of the MLCP core application.
Review the MLCP layered architecture [here](../../architecture.md).

### Requirements

- The *shared layer* is required to expose entry points to the functionality it implements to every component
  in the MLCP application.

- The *shared layer* is required to implement the code that is used by the entire MLCP application.

- The *shared layer* is required to implement its internal functionality in a way that is generic and
  reusable by any component in the MLCP application. The code inside the *shared layer* should not be
  specific to any component or layer.

### Responsibilities

- The *shared layer* is responsible for implementing the code that is used by the entire MLCP application.

  #### Some of the capabilities the shared layer is responsible for:
    - Generic concurrency management
    - Generic logging
    - Generic dictionary handling
    - Generic memory utilities
    - Generic file system utilities

## Features

Some of the main features of the *shared layer* are:

- **concurrency management** - the *shared layer* implements the code that manages concurrency in the MLCP
  application used to simply handle and manage concurrency and multiprocessing/threading.

- **logging** - the *shared layer* implements the code that manages logging in the MLCP application. It extends the
  python ```logging``` module to implement a custom logger that is used by the entire MLCP application to log lines
  that are formatted to the mlcp logging format. As well as handling logging the nested main processes and subprocesses
  the mlcp goes through in its runtime as well as information about them such as execution time and maximum memory to 
  allow easy debugging and monitoring of the MLCP runtime processes.

- **file system utilities** - the *shared layer* implements reusable code used to perform operations/checks/interactions
  with the file system with a single function call.

## Implementation

### Interface

The *shared layer* exposes its functionality through a set of interfaces that are implemented by the components inside
it. The *shared layer* doesn't expose any functionality directly, but rather through its internal components that
implement
their own, in other words the interface of this large component is made up of the interfaces of the components inside
it.
An example for the usage of the shared layer from an external component:

```python
from shared_layer.mlcp_logger import logger

logger.log("This is a log message")
```

### Internal Structure And Implementation

The *shared layer* component is a collection of independent and generic subcomponents, that individually implement
a specific functionality that is used by the entire MLCP application, the internal components of this layer don't
target any specific use case, or any specific layer, they are generic and reusable by any component in the MLCP.
