from src.utils.s3_utils import get_s3_client, put_s3_file
from src.utils.parser import parse_payload_body
from src.utils.s3_utils import get_s3_file_content
import pandas as pd
import io


def obfuscate_pii_fields(s3_client, bucket_name,
                         pii_fields, file_key):

    """For CSV type data file obfuscate PII fields

        Parameters:
        s3_client (boto3.client): The S3 client.
        bucket_name (str): The name of the S3 bucket home for file
                            to be processed.
        file_key (str): The key of the file in the S3 bucket.
       returns: bytes stream obfuscated data buffer
    """

    # Get the file content from the S3 bucket
    file_content = get_s3_file_content(s3_client, bucket_name, file_key)

    # Use an in memory buffer to read the CSV file content
    text_buffer = io.StringIO(file_content)

    # Read the buffer into a pandas dataframe
    df = pd.read_csv(text_buffer)

    # Obfuscate PII fields by masking them with ***
    # Missing or misspelt fields will be ignored
    for field in pii_fields:
        if field in df.columns:
            df[field] = '***'

    # Create a buffer to hold the obfuscated data
    csv_buffer = io.StringIO()

    # Convert the dataframe to csv and write to the buffer
    df.to_csv(csv_buffer, index=False)

    # Return the buffer as bytes stream
    return csv_buffer.getvalue().encode('utf-8'), df


def obfuscator(payload, obfuscate_bucket=None):
    """
    Obfuscate PII fields in the payload and optionally upload the
    obfuscated data to an S3 bucket.
    This implementation supports only CSV files.

    Parameters:
    payload (dict): The payload containing the S3 bucket name,
    file key, PII fields, and S3 URI.
    obfuscate_bucket (str, optional): The name of the S3 bucket
    to which the obfuscated data will be uploaded.
    If this value is None, the obfuscated data will not be uploaded.

    Returns:
    tuple: The obfuscated data and the output file key.
    """

    # Parse the payload body to extract components
    result = parse_payload_body(payload)
    bucket_name = result['bucket_name']
    file_key = result['file_key']
    pii_fields = result['pii_fields']

    # Get the S3 client
    s3_client = get_s3_client()

    # Check if the file is a CSV
    if file_key.lower().endswith('.csv'):
        # Obfuscate PII fields in the file content
        # obfuscated_data_buffer is the obfuscated data in
        # bytes stream
        # obfuscated_data is the obfuscated data in string
        result = obfuscate_pii_fields(s3_client, bucket_name, pii_fields,
                                      file_key)
        obfuscated_data_buffer = result[0]

        # Check if the obfuscated data should be uploaded to a S3 bucket
        # If the obfuscate_bucket is None, the obfuscated data is not loaded
        # by default output file key used will be same as input file key
        if obfuscate_bucket:
            # Put the obfuscated data back to the S3 bucket
            put_s3_file(s3_client, obfuscate_bucket, file_key,
                        obfuscated_data_buffer)

        return obfuscated_data_buffer, file_key
    else:
        raise ValueError("The provided file is not a CSV file")
