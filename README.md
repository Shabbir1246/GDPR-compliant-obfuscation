<!-- README.md -->

# GDPR Obfuscator Project

## Overview

This project aims to provide an obfuscation tool that can process data ingested to an AWS bucket, intercept personally identifiable information (PII), and anonymize it according to GDPR requirements.  The obfuscation tool is written in Python, is unit tested, PEP-8 compliant, and tested for security vulnerabilities, with no credentials recorded in the code.


## Features of the project:
1. A simple lambda handler (`src/lambda_function.py`) that accepts an S3 event, checks if it refers to a `csv` file and then anonymises PII fields and saves processed file to a given S3 bucket.

1. The code features trapping of specific errors (including a custom error) and handles unexpected `RuntimeErrors`.
1. The code is tested (`test/test_file_reader/test_lambda.py`) using the `moto` library to mock AWS artefacts. 

1. The project build is via a `Makefile` which allows `bandit` and `safety` checks for security vulnerabilities, and `flake8` checks for PEP8 compliance.

## Assumptions and Prerequisites
1. Data is stored in CSV-, JSON-, or parquet-formatted files in an AWS S3 bucket.
2. Fields containing GDPR-sensitive data are known and will be  supplied in advance.
3. Data records will be supplied with a primary key.

**Note: This initial iteration of the tool provides for obfuscation
of CSV files only**


## Project Structure

- **obfuscator_function_lambda/**: Parent folder, contains the following sub folders:
- `src/`
  - `lambda_function.py`: Contains the Lambda handler function `lambda_handler` for processing files.
  - `utils`: Contains utility functions for processing files and generating fake test data.
- `tests/`: Contains unit tests for the functions in `lambda_function.py` and `utils/*.py`.
   - `test_data`: test_data.csv and wrong_file.txt which can be used for testing (need to uploaded to s3 bucket)
- `obfuscator_cmd_example.py` - a python program that can be called from a python interpreter 
   from within AWS CLI  
- `cmd_line_test.sh` - a shell program that can be used for testing from an AWS CLI
  
- `requirements.txt`: Contains the required Python packages for the project.
- `Makefile` - file to build the project environment and run various check mentioned previously
- `lambda.zip` - a zip file for deploying to the AWS Lambda

## Deployment

### Lambda Setup

1. Create a new Lambda function in the AWS Management Console.
2. Upload `lambda.zip` in the lambda function resulting in  creation of `src` and `util` folders
3. Set the handler to `src.lambda_function.lambda_handler`.
5. Create an API Gateway trigger for the Lambda function and configure it as below.

### API Gateway Setup

1. Create a new API Gateway in the AWS Management Console.
2. Create a new resource and method (POST) for triggering the Lambda function.
3. Configure the integration type as "Lambda Function" and select your Lambda function.
4. Deploy the API to a stage.

### S3 Bucket Setup

1. **Create Source Bucket:** This bucket will be used to store the files that need to be obfuscated.
2. **Create Destination Bucket:** This is an optional bucket to be used to store the obfuscated files.

### Grant Permissions

Ensure that your Lambda function has the necessary permissions to access these buckets. You can do this by attaching the appropriate IAM role to your Lambda function.


## Usage

To obfuscate a file, send a POST request to the API Gateway endpoint with a JSON payload. 
Examples of API Gateway endpoint and JSON are as follows:

- `API Gateway endpoint`: https://hylv4wxyw7.execute-api.ap-southeast-2.amazonaws.com/obfuscator
- `Json post request`:
```json
{
  "file_to_obfuscate": "s3://your-bucket-name/path/to/file.csv",
  "pii_fields": ["name", "email"]
}
```


## Running Tests

To run the unit tests locally, follow these steps:

1. **Initialize the virtual environment:**
   ```bash
   python3 -m venv venv
2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Set PYTHONPATH:**
   ```bash
   export PYTHONPATH=$PYTHONPATH:/path/to/your/project/src
5. **Run the test cases:**
   ```bash
   pytest test
**Make sure to replace /path/to/your/project/src with the actual path to your project's source code.**
