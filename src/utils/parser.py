
def parse_payload_body(body):

    """Parse event body to extract S3 URI, bucket name, file key,
      and PII fields.
    """

    s3_uri = body["file_to_obfuscate"]
    s3_parts = s3_uri.replace("s3://", "").split("/", 1)
    bucket_name = s3_parts[0]
    file_key = s3_parts[1]
    pii_fields = body["pii_fields"]

    return {'bucket_name': bucket_name, 'file_key': file_key,
            'pii_fields': pii_fields, 's3_uri': s3_uri}
