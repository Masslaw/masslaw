account_id = '746826375642'


CASE_BUCKET_CORS = {
    "CORSRules": [
        {
            "AllowedHeaders": [
                "*"
            ],
            "AllowedMethods": [
                "GET",
                "PUT",
                "POST",
            ],
            "AllowedOrigins": [
                "*"
            ],
            "ExposeHeaders": ["etag"]
        }
    ]
}


CASE_ASSUME_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/LambdaFullyAccessingIAM"},
            "Action": "sts:AssumeRole"
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/LambdaMasslawCasesHandlerRole"},
            "Action": "sts:AssumeRole"
        }
    ]
}


FILE_DOWNLOAD_URL_EXPIRATION_SECONDS = 5 * 60  # 5 minutes


class CaseRoles:
    s3_bucket_access_role = "s3_role"
    dynamo_db_item_access_role = "db_item_role"