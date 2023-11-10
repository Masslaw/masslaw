# Resources Layer

The *resources layer* implements functionality used to interact, manage, and handle the interactions with resources
and entities outside the MLCP application, as well as owns common/uncommon knowledge of the services it interacts
with, and implements code that represents it.

----

## Architecture and Design

This component acts as one of the highest level layers of the MLCP core application.
Review the MLCP layered architecture [here](../../architecture.md).

### Requirements

- The *resources layer* is required to expose entry points to the functionality it implements to the
  [logic layer](../logic_layer/logic_layer.md)

- The *resources layer* is required to implement the code that interacts with resources and entities
  outside the MLCP application.

- The *resources layer* is required to implement the code that represents both common and uncommon
  knowledge about the services it interacts with.

- The *resources layer* is required to implement its functionality in the lowest level possible. It should not
  deal with any logic or computational tasks, neither should it deal with any business logic.

### Responsibilities

- The *resources layer* is responsible for implementing the code that interacts with resources and entities
  outside the MLCP application.

- The *resources layer* is responsible for implementing the code that represents both common and uncommon
  knowledge about the services it interacts with.

  #### Some of the resources the *resources layer* is responsible for interacting with:

  - AWS S3
  - AWS DynamoDB
  - AWS Neptune

## Features

Some of the features the *`component name`* are:

- **aws services interaction** - The *resources layer* implements the code that interacts with AWS services
  such as S3, DynamoDB, Neptune etc... as well as implements the code that represents the knowledge commonly
  needed to implement the interactions with these services.

## Implementation

### Interface

The *resources layer* exposes its functionality through a set of interfaces that are implemented by the components
inside it. The *resources layer* doesn't expose any functionality directly, but rather through its internal components
that implement their own, in other words the interface of this large component is made up of the interfaces of the
components inside it. 
An example for the usage of the *resources layer* from an external component:
```python
from mlcp.src.resources_layer.aws.s3_client import S3BucketManager

# create an instance of a manager that manages an S3 bucket in a certain region 
bucket_manager = S3BucketManager(
    bucket_name = 'some-s3-bucket',
    region_name = 'us-east-1',
)

# use the manager to get a file from the bucket with a specific key to a local path
bucket_manager.get_file_from_bucket(
    file_name = 'some-file.txt',
    target_path = '/some/local/path/to/file.txt'
)
```

### Internal Structure And Implementation

This component is implemented as a bunch of independent components that implement any functionality needed to
interact and manage the interactions with resources and entities outside the MLCP application.
