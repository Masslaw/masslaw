# Interface Layer

The interface layer is where the MLCP interface is implemented, along with the code that
handles all the inputs it should receive.

----

## Architecture and Design

This component acts as one of the highest level layers of the MLCP core application.
Review the MLCP layered architecture [here](../../architecture.md).

### Requirements

- The interface layer is required to implement the entry point of every execution of the MLCP.

- The interface layer is required to load and execute the actions described in the MLCP process
  configuration.

### Responsibilities

- The interface layer is responsible for handling the MLCP process configuration correctly.

- The interface layer is responsible for being the main entry point of the application and
  every external execution of it

## Features

Some of the main features of the *interface layer* are:

- **application** - the entry point of the MLCP runtime process. The *execution layer* implements
  the application as a class that implements the `Application` interface and handles running
  the runtime processes correctly.

## Implementation

### Interface

The *interface layer*'s interface, consists of a single element, the `Application`.
Implemented as a class, the `Application` can be used to run the MLCP runtime process.
Simply create an instance of the `Application` class, and call the instance as a function,
the MLCP will start running.

In addition, the *interface layer* accepts another layer of interaction, an indirect interface,
the *interface layer* parses the MLCP process configuration and handles it.
The MLCP process configuration is a JSON object, either serialized or not, written to the machine's
environment via the variable key: `"mlcp_process_configuration"`

```python
import os
from mlcp.src.interface_layer.application import Application

process_configuration = {
    "actions": [
        ...
    ]
}

os.environ["mlcp_process_configuration"] = process_configuration

app = Application()
app()
```

In a production environment the MLCP process configuration is provided to the application externally, from
the entity that submitted the MLCP's container execution.

### Internal Structure And Implementation

The *interface layer* implements a single component, the `application`, which implements both the `Application`
class used as the interface, as well as the logic that handles the MLCP process configuration and the application
high level execution logic.
