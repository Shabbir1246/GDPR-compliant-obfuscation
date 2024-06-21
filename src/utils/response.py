import json

# Status codes
SUCCESS = 200
ERROR = 500


def create_response(status_code, data=None):

    """ Create a response object for API Gateway Lambda
        Proxy Integration.
    """

    response = {
        "statusCode": status_code,
    }

    if isinstance(data, dict):  # Check if data is a dictionary
        return {**response, **data}
    else:
        return response


def handle_lambda_success(obfuscate_data):

    """Handle successful obfuscation process."""

    data = {
        'isBase64Encoded': False,
        'headers': {
            'Content-Type': 'application/octet-stream'
        },
        'body': obfuscate_data
    }
    return create_response(SUCCESS, data)


def handle_lambda_exception(e):
    """Handle exceptions."""

    error_message = str(e)

    print(f"Error processing file from S3: {error_message}")
    errorData = {
        'body': json.dumps({
            'error': error_message,
            'message': 'An error occurred while processing your request.'
        })
    }
    return create_response(ERROR, errorData)
