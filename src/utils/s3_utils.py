import boto3


def get_s3_client():
    """
    Initialize and return an S3 client.
    """
    return boto3.client('s3')


def get_s3_file_content(s3_client, bucket_name, file_key):
    """
    Get the content of the file to be obfuscated from the specified S3 bucket.

    Parameters:
    s3_client (boto3.client): The S3 client.
    bucket_name (str): The name of the S3 bucket home for file to be processed
    file_key (str): The key of the file in the S3 bucket.

    Returns:
    str: File content in a buffer for processing.
    """
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    return response['Body'].read().decode('utf-8')


def put_s3_file(s3_client, bucket_name, file_key, data):
    """
    Put the obfuscated data back to a given S3 bucket if specified.

    Parameters:
    s3_client (boto3.client): The S3 client.
    bucket_name (str): The name of the S3 bucket for saving data.
    file_key (str): The key of the file in the S3 bucket.
    data (str): The obfuscated data to be put in the file.
    """
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=data)
