# Structure Visualizing

The *structure visualizing* component is used to visualize the structure of the textual content extracted from an 
optical file or document, and managed by the [extracted optical text structure](../extracted_optical_text_structure.md)
component.

---

## Architecture and Design

The *structure visualizing* component is a subcomponent of the [extracted optical text structure](../extracted_optical_text_structure.md)
component. It implements the logic, and exposes the interface, used to visualize the structure of the textual content 
extracted from an optical file or document handled by it.

### Requirements

- The *structure visualizing* is required to be able to visualize the structure of the textual content that an 
  'extracted optical text document' holds.

### Responsibilities

- The *structure visualizing* is responsible for implementing the logic, and exposing the interface, used to visualize 
  the structure of the textual content that an 'extracted optical text document' holds.

## Features

Some of the features the *structure visualizing* are:

- **Visualizing On Images** - the component allows visualizing the textual content and structure of a page on top of if,
  by displaying rectangles that describe the bounding rectangles of the optical elements in it, in the image that
  depicts the page itself.

## Implementation

### Interface

In the high-level, the *structure visualizing* exposes functionality used to visualize the structure of the textual
content that an 'extracted optical text document' holds.

#### StructureVisualizing

This class holds the instance of an `ExtractedOpticalTextDocument` and exposes functionality used to visualize the
data inside it

### Internal Structure And Implementation

#### Image Printing

The *structure visualizing* implements logic that allows allows visualizing the textual content and structure of a page 
on top of if, by displaying rectangles that describe the bounding rectangles of the optical elements in it, in the image 
that depicts the page itself.

Given a document, and the list of images that depict the children of the structure root, the component
will attempt to draw rectangles around the elements in those image, given the information stored inside each of the child
element.
