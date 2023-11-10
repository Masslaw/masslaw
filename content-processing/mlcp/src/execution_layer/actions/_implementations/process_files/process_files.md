# Process Files (Application Action)

Runs the initial processing tasks files in Masslaw should go through (extract text, optimization, compression,
transformation etc...) on one or more files given a specified directory, and outputs the results to a set of specified
directories.

## parameters structure:

```json
{
  "files_data": [
    {
      "file_name": "ToProcess.file",
      "text_export_directory": "ExportedText/",
      "assets_export_directory": "ExportedAssets/"
    }
  ]
}
```
