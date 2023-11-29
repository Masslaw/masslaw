# Logic Layer

The *logic layer* implements the code that actually performs any low level computational task
needed to perform any capability the MLCP may or may not need for any [action](../execution_layer/actions/actions.md)
it should perform.

----

## Architecture and Design

This component acts as one of the highest level layers of the MLCP core application.
Review the MLCP layered architecture [here](../../architecture.md).

### Requirements

- The *logic layer* is required to expose entry points to the functionality it implements to the
  [execution layer](../execution_layer/execution_layer.md) as well as using, and in most cases
  forced to implement wrappers to, the functionality exposed by
  the [resources layer](../resources_layer/resources_layer.md).

- The *logic layer* is required to implement the code that performs the low level computational
  tasks needed to perform any capability the MLCP may or may not need for any action it should perform.

### Responsibilities

- The *logic layer* is responsible for implementing complex computational tasks flawlessly, and
  is responsible to test both normal usage and edge cases to eliminate internal exceptions - as it
  is the place in which they will be most common.

- The *logic layer* is responsible for implementing the code that performs the low level computational
  tasks needed to perform any capability the MLCP may or may not need for any action it should perform.

  #### Some of the capabilities the logic layer is responsible for:
    - OCR Text Extraction
    - Image Processing
    - File Processing
    - Audio Processing
    - Natural Language Processing
    - Data Processing

## Features

## Features

Some of the main features of the *logic layer* are:

- **File Processing** - process a file in a way that is specific to the file type. The processing
  a file goes

## Implementation

### Interface

The *logic layer* exposes its functionality through a set of interfaces that are implemented by the components
inside it. The *logic layer* doesn't expose any functionality directly, but rather through its internal components
that implement their own, in other words the interface of this large component is made up of the interfaces of the
components inside it.

```python
from logic_layer.file_processing import FileProcessing

example_file = 'some_pdf_file.pdf'

processor = FileProcessing.create_processor(example_file)

processor.process()
processor.export_text('some/directory/for/text/export')
processor.export_assets('some/directory/for/assets/export')
```

### Internal Structure And Implementation

The *logic layer* is a monster of many big or small, complex or simple components, each taking care of a specific
capability the MLCP needs to be able to perform. Each component can be both independent of the other components in the
layer or not, but never dependent on components outside the layer itself or the one below it (
the [resources layer](../resources_layer/resources_layer.md)).
