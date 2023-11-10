# S3 Upload (Application Action)

Uploads one or more files or folders given a specified bucket name and file key located in a 
specified local directory.

## parameters structure:
```json
{
  "bucket_name": "some-bucket",
  "files_data": [
    {
      "saved_as": "SomeFile/OrDirectory",
      "key": "Uploaded-file-key"
    },
    {
      "saved_as": "SomeFile/OrDirectory",
      "key": "Uploaded-file-key"
    }
    ...
  ]
}
```
