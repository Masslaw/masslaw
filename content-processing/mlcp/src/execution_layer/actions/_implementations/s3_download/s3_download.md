# S3 Download (Application Action)

Downloads one or more files given a specified bucket name and file key to a 
specified local directory with a specified name.

## parameters structure:
```json
{
  "bucket": "some-bucket",
  "files_data": [
    {
      "key": "SomeFile.file",
      "save_as": "ToProcess.file"
    },
    {
      "key": "SomeOtherFile.document",
      "save_as": "ImAFile.file"
    }
    ...
  ]
}
```
