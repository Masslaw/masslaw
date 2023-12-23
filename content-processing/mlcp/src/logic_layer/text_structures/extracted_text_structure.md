# Extracted Text Structure

This component is one of the foundation components of the MLCP. It is used to both build and handle the complex
and hierarchical structure of text elements extracted from an optical document or image. It acts as a convenient
place to load all textual data extracted from an optical document, regardless of the actual tool that was used
to extract it, and exposes functionality to very easily manipulate it to get the best out of it.

---

## Architecture and Design

The *extracted text structure component* is part of the [logic layer](../logic_layer.md) of the MLCP. It is used to
handle and build the text structure of the textual content extracted from a file or document. It is made up of a set of
subcomponents that each handle a different kind of extracted textual data.

### Requirements

- The *extracted text structure component* is required to be able to load and handle the textual content extracted from
  a file or document.

- The *extracted text structure component* is required to be able to build a hierarchical structure of the textual
  content extracted from a
  file or document.

- The *extracted text structure component* is required to implement logic for handling the textual output extracted from
  any file type the
  MLCP supports.

- The *extracted text structure component* is required to implement export logic to the data it handles.

- The *extracted text structure component* is required to implement loading logic to the data it handles and
  previously executed.

### Responsibilities

`create a list of the responsibilities of the component. what is this component responsible for? what are the things
that need to be taken into account when implementing this component?`

- The *extracted text structure component* is responsible for handling the textual content extracted from a file or
  document.

- The *extracted text structure component* is responsible for building a hierarchical structure of the textual content
  extracted from a file or document.

- The *extracted text structure component* is responsible for being the main component that handles the textual output
  extracted from any file type the MLCP supports.

- The *extracted text structure component* is responsible for implementing logic for handling the textual output given
  to it in a way that represents the business, design, and technical requirements of the MLCP and masslaw in general.

- The *extracted text structure component* is responsible for implementing export logic to the data it handles.
  preferably in multiple format, but at least in the format required by the rest of the masslaw system

## Features

Some of the features the *extracted text structure component* are:

- **text structure construction** - the *extracted text structure component* implements the logic needed to build a
  hierarchical structure of the textual content extracted from a file or document.

- **textual structure identification** - the *extracted text structure component* implements logic used to identify
  different kinds of textual structures in the textual content extracted from a file or document.

- **textual structure manipulation** - the *extracted text structure component* implements logic used to manipulate
  different kinds of textual structures in the textual content extracted from a file or document - correcting
  mistakes, identifying lines of text, paragraphs, and arrangements that indicate the reading order of individual
  elements, handling bidirectional text, and many more…

- **textual structure exporting** - the *extracted text structure component* implements logic used to export the textual
  content extracted from a file or document in a way that represents the business, design, and technical requirements
  of the MLCP and masslaw in general.

- **textual structure loading** - the *extracted text structure component* implements logic used to load previously
  exported textual content extracted from a file or document in a way that represents the business, design, and
  technical requirements of the MLCP and masslaw in general.

- **textual structure visualization** - the *extracted text structure component* implements logic used to visualize the
  textual content extracted from a file or document in a way that represents the business, design, and technical
  requirements of the MLCP and masslaw in general.

## Implementation

### Interface

`a brief about the interface of the component, how to interact with it and what it exposes
a short example or snippet for an external interaction with the component is highly recomended in here.`
The *extracted text structure component* exposes its functionality through the components inside it. Each is used to
handle a different kind of extracted text (i.e. text extracted from an optical document, text extracted from an audio
file, etc...) and each exposes its own interface. Each of these interfaces are largely made up of a central interface
used to expose the main working objects and types of the component, and a set of interfaces implemented by the internal
component of it, that are used manipulate and operate on these objects and types.
For example, the optical form of the *extracted text structure component* exposes an interface made up of:

- **Main Document** - The main data holder, to use this component, a main document needs to be created. It is the one
  that holds all the data of the extracted text from a file. It is the one that the user of the component operates on.
- **Single Entry** - The type used to identify and declare the structure of a single data entry provided to the
  component in order to add a data item to the document.
  Here is an example for how the raw output of tessearct is handled, transformed into entry items and provided to the
  constructor subcomponent to be added to a newly created document.

```python
from typing import List
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalElementRawDataEntry
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction import OpticalTextStructureConstructor
from logic_layer.text_structures.extracted_optical_text_structure.document_metadata import DocumentMetadataHandler
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting import DocumentExporter

# some function that takes a list of images and returns the elements inside it
export_text_from_images = ...
# some function that takes the output of the ocr and returns a list of entries for a single image
get_entries_from_ocr_output_for_single_image = ...

images = ['some_image.png', 'some_other_image.png']
ocr_output = export_text_from_images(images)

# build the array of groups (an array of arrays of entries)
# each group represents the list of entries that came from a single image
entry_groups = []
for image_output in ocr_output:
  # an entry group represents the entries to the element that all exist in a single structure child/group (image)
  entry_group: List[OpticalElementRawDataEntry] = get_entries_from_ocr_output_for_single_image(image_output)
  entry_groups.append(entry_group)

# create a new document
document = ExtractedOpticalTextDocument()
# define the hierarchy formation
hierarchy_formation = [...]

# create a constructor for the document
constructor = OpticalTextStructureConstructor(document, hierarchy_formation)
# add the groups to the structure as a individual children (each image is a child)
constructor.add_entry_groups_to_structure(entry_groups)

# create a metadata handler for the document
metadata_handler = DocumentMetadataHandler(document)
# use the metadata handler to add the image metadata to the document
for image_num, image_dir in enumerate(images):
  image_data = ...
  metadata_handler.put_metadata_item(['structure', 'image_sizes', str(image_num)], image_data)

# create an exporter for the document
exporter = DocumentExporter(document)
# use the exporter to export the document's content to a file
with open('some_file.xml', 'w') as xml_file:
  exporter.export_xml(xml_file)
```

### Internal Structure And Implementation

As previously mentioned, the *extracted text structure component* is made up of a set of subcomponents, each handling a
different kind of extracted text. Though, each subcomponent has its own internal structure and implementation as
follows:
Since the amount of "moving parts" or functionalities that each subcomponent needs to implement is so large, it is made
up of a set of even more subcomponents, each handling a different kind of functionality that is performed on a single
datastructure called the "document" (as described in the [interface](#interface) section).
