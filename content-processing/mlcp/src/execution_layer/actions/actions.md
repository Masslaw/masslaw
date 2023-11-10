# Actions

An **action** is one independent ability the MLCP is able to perform.

## Implementation of actions

### Actions

The actions are implemented as separate python modules. Each action module contains the implementation of a class
in its `__init__.py` file. This class extends the [ApplicationAction](_application_action.py) class, specifies
values specific to its own such as "required_params" and "name" and implements the abstruct methods of the
ApplicationAction class. The ApplicationAction class both implements the basic structure of an action, providing the
[ActionLoader](../actions.py) class a single interface and structure to work with, as well as implements some
generic utilities and functionalities that actions commonly use.

### ActionLoader

The action loader is the one the actions module as well as the execution layer eventually expose for external usage.
This class used and is responsible for managing, loading, executing and handling the actions available in the MLCP.
To load a function, the name of the action is provided to the ActionLoader (the name of an action is exactly the name
of the python component that implements it), the action loader then loads the python code that the action uses, loads
the class implementation of the action and them proceeds to execute it.
By loading the component dynamically (rather than statically), the action loader makes sure only the code the action
is dependent on is loaded (instead of statically importing the component which will then recursively import and load
all nested dependencies of that component)

The actions the MLCP currently implements are:

- [s3_download](_implementations/s3_download/s3_download.md)
- [s3_upload](_implementations/s3_upload/s3_upload.md)
- [process_files](_implementations/process_files/process_files.md)
