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
          "protocol": "wss",
          "port": "8182",
          "type": "gremlin"
        },
        "write": {
          "endpoint": "some-write-endpoint",
          "protocol": "wss",
          "port": "8182",
          "type": "gremlin"
        }
      },
      "knowledge_record_data": {
        "node_properties": {
          "this-property": "will be present on all nodes extracted in the current execution"
        },
        "edge_properties": {
          "this-property": "will be present on all edges extracted in the current execution"
        },
        "subgraph_node_properties": {
          "this-property": "is the one present in all nodes of the subgraph (in neptune) the result of this execution is targeting, and will be on the nodes extracted in the current execution"
        },
        "subgraph_edge_properties": {
          "this-property": "is the one present in all edges of the subgraph (in neptune) the result of this execution is targeting, and will be on the edges extracted in the current execution"
        }
      }
    }
  ]
}
```
