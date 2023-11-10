# Execution Layer

The *Execution Layer* is responsible for implementing, managing and allowing the execution of
all the [actions](actions/actions.md) the MLCP is able to perform. Each action is implemented separately
and should not depend on any other action.

---

## Architecture and Design

This component acts as one of the highest level layers of the MLCP core application.
Review the MLCP layered architecture [here](../../architecture.md).

### Requirements

- The *Execution Layer* is required to expose all functionality that allows creating and executing
  different actions independently.

- The *Execution Layer* is required to allow the [interface layer](../interface_layer/interface_layer.md) to
  interact with it, as well as interacting with the [logic layer](../logic_layer/logic_layer.md).

### Responsibilities

- The *Execution Layer* is responsible for implementing all the actions the MLCP should be able
  to perform.

- The *Execution Layer* is responsible for handling the logic of managing, loading, executing
  and handling the actions.

- The *Execution Layer* is responsible for implementing internally all logic that's used to manage
  the execution of each action.

- The *Execution Layer* is responsible for using the **Logic Layer** and its exposed capabilities to
  perform the steps needed to execute an action.

- The *Execution Layer* is responsible for implementing the actions in a way that maintains the
  integrity of the statement made in the following quote (taken from the [mlcp](../../mlcp.md) main page):
  > An action - is the smallest operation the MLCP is designed to do. Each individual action is executed
  independently and does not depend on the execution of another. However, in some, probably most cases,
  multiple actions are executed in some order one by one, where one does depend on the execution of the
  other. For example, this series of actions: download a file --> process it --> upload the result;
  In this very simple example, each process depends on the execution of the one previous to it to function
  correctly, though, at the single action level, each process has its own execution and logic and is not
  designed exclusively to be executed after one or some set of specific actions - the “process file” action
  doesn’t “know” or “require” that the files are downloaded using the “download files” action, they can very
  well be created for example, and the “upload file” action doesn’t know that
  the target files are the result of the file processing action etc…

## Features

Some of the main features of the *execution layer* are:

- **actions** - the *Execution Layer* implements all the actions the MLCP is able to perform.

## Implementation

### Interface

The *execution layer* exposes its functionality through a set of interfaces that are implemented by the components
inside it. The *execution layer* doesn't expose any functionality directly, but rather through its internal components
that implement their own, in other words the interface of this large component is made up of the interfaces of the
components inside it. 
An example for the usage of the execution layer from an external component:

```python
from execution_layer.actions import ApplicationActionLoader


def __load_process_actions(self):
  process_actions_data = self.__process_configuration.get("actions", [])
  for action_data in process_actions_data:
    process_action = ApplicationActionLoader()
    action_name = action_data.get("name", {})
    action_params = action_data.get("params", {})
    action_required = action_data.get("required", False)
    process_action.set_name(action_name)
    process_action.set_params(action_params)
    process_action.set_required(action_required)
    self.__process_actions.append(process_action)
```

### Internal Structure And Implementation

The *execution layer* component is a collection of components that together implement the functionalities needed to
fulfill the requirements and responsibilities of this component. As described both in the requirements of the MLCP's
high level layerd architecture and in the requirements of this component, the *execution layer* is required to use
and almost "wrap" the functionality of the [logic layer](../logic_layer/logic_layer.md).
