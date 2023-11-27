# Extract Knowledge (Application Action)

Runs the processing tasks of extracting knowledge from a file. Currently supporting only text file,
in the future we plan to support processing the extracted xml data of an optical text structure document. 
The extracted knowledge is loaded to a neptune db.

## parameters structure:

```json
{
  "files_data": [
    {
      "file_name": "some_text.txt",
      "languages": ["en", "heb"], // currently only english is supported
      "neptune_endpoints": {
        "read": {
          "endpoint": "some-read-endpoint",
          "port": "8182",
          "type": "gremlin"
        },
        "write": {
          "endpoint": "some-write-endpoint",
          "port": "8182",
          "type": "sparql"
        }
      },
      "knowledge_record_data": {
        "node_properties": {
          "this-property": "will be present on all nodes in the uploaded subgraph with this value"
        },
        "edge_properties": {
          "this-property": "will be present on all edges in the uploaded subgraph with this value"
        }
      }
    }
  ]
}
```
