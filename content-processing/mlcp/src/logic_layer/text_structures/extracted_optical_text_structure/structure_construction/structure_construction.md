# Structure Construction

The *structure construction* component is used to construct the initial structure of the textual content extracted from 
an optical file or document, and managed by the [extracted optical text structure](../extracted_optical_text_structure.md)
component, using low level individual raw data entries.

---

## Architecture and Design

The *structure visualizer* component is a subcomponent of the [extracted optical text structure](../extracted_optical_text_structure.md)
component. It implements the logic, and exposes the interface, used to construct the initial structure of the textual
content extracted from an optical file or document, and managed by the [extracted optical text structure](../extracted_optical_text_structure.md)
component, using low level individual raw data entries.

### Requirements

- The *structure visualizer* is required to be able to construct the initial structure of the textual content that an 
  'extracted optical text document' holds.

- The *structure visualizer* is required to be able to parse, handle, and manage the low level individual raw data entries
  and use them to construct the element hierarchy of the textual content that an 'extracted optical text document' holds.

- The *structure visualizer* is required to always refer to the hierarchy formation specified in the structure root it
  constructs.

- The *structure visualizer* is required to be able to identify, and breakup entries according to the element type
  their value represents in the hierarchy formation specified in the structure root it constructs.

### Responsibilities

- The *structure visualizer* is responsible for implementing the logic, and exposing the interface, used to construct 
  the initial structure of the textual content that an 'extracted optical text document' holds.

- The *structure visualizer* is responsible for being the subcomponent of the [extracted optical text structure](../extracted_optical_text_structure.md)
  component that handles the low level individual raw data entries and uses them to construct the element hierarchy of
  the textual content that an 'extracted optical text document' holds.

- The *structure visualizer* is responsible for always referring to the hierarchy formation specified in the structure
  root it constructs.

- The *structure visualizer* is responsible for identifying, and breakup entries according to the element type
  their value represents in the hierarchy formation specified in the structure root it constructs.

- The *structure visualizer* is responsible for building the initial structure of the textual content that an 'extracted
  optical text document' holds.

- The *structure visualizer* is responsible for being on of the main entry points of the the component [extracted optical text structure](../extracted_optical_text_structure.md)
  as it is the one responsible for building the initial structure of its data.

## Features

Some of the features the *structure visualizer* are:

- **Structure Construction** - the component allows constructing the initial structure of the textual content that an
  'extracted optical text document' holds, using low level individual raw data entries.

## Implementation

### Interface

In the high-level, the *structure construction* exposes functionality used to construct the initial structure of the
textual content that an 'extracted optical text document' holds.

#### OpticalTextStructureConstructor

This class holds an instance of an `ExtractedOpticalTextDocument` and exposes functionality used to construct the
initial structure of the textual content that it holds.

### Internal Structure And Implementation

> To be continued...
