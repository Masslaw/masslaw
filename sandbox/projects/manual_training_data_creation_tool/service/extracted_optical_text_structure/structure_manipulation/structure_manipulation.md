# Structure Manipulation

The *structure manipulation* component is used to manipulate the textual data and structure extracted from an optical 
file or document, and managed by the [extracted optical text structure](../extracted_optical_text_structure.md) component.

---

## Architecture and Design

The *structure manipulation* component is a subcomponent of the [extracted optical text structure](../extracted_optical_text_structure.md)
component. It implements the logic, and exposes the interface, used to manipulate the textual data and structure 
extracted from an optical file or document, and managed by it.

### Requirements

- The *structure manipulation* is required to be able to manipulate the textual data and structure that an 
  'extracted optical text document' holds.

- The *structure manipulation* is required to implement logic and expose the interface used to sort the elements that 
  are in the test structure of a document.

- The *structure manipulation* is required to implement logic and expose the interface used to clean the structure of
  a document.

- The *structure manipulation* is required to implement logic and expose the interface used to merge elements that exist
  as two separate elements in the structure of a document, but should be one.

### Responsibilities

- The *structure manipulation* is responsible for implementing the logic, and exposing the interface, used to manipulate 
  the textual data and structure that an 'extracted optical text document' holds.

- The *structure manipulation* is responsible for being the subcomponent of the [extracted optical text structure](../extracted_optical_text_structure.md)
  component that handles the manipulation of the textual data and structure that an 'extracted optical text document' 
  holds.

## Features

Some of the features the *structure manipulation* are:

- **Structure Sorting** - the component allows sorting the elements that are in the test structure of a document.

- **Structure Cleaning** - the component allows cleaning the structure of a document - from elements that dont hold any
  information.

- **Structure Merging** - the component allows merging elements that exist as two separate elements in the structure of
  a document, but should be one.

## Implementation

### Interface

In the high-level, the *structure manipulation* exposes functionality used to manipulate the textual data and structure
that an 'extracted optical text document' holds.

#### OpticalTextStructureManipulator

This class holds the instance of an `ExtractedOpticalTextDocument` and exposes functionality used to manipulate the
structure data inside it.

### Internal Structure And Implementation

> To be continued...
