import json
from src.utils.response import handle_lambda_success, handle_lambda_exception
from src.utils.obfuscator import obfuscator

def lambda_handler(event, context):
    """Main handler for the Lambda function."""
    try:

        body = json.loads(event.get('body', '{}'))

        # calling obfuscator function to handle the obfuscation process
        obfuscated_data, file_key = obfuscator(body)

        # Return a successful response
        return handle_lambda_success(obfuscated_data)

    except Exception as e:
        # Log and return an error response
        print(f"Error processing file from S3: {e}")
        return handle_lambda_exception(e)
