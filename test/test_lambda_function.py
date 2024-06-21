import pytest
from moto import mock_aws
from src.utils.s3_utils import get_s3_client, get_s3_file_content, put_s3_file
from src.utils.obfuscator import obfuscate_pii_fields
from src.utils.obfuscator import obfuscator
import warnings


@pytest.fixture(autouse=True)
def ignore_deprecation_warning():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        yield


@mock_aws
def test_get_s3_file_content():
    s3_client = get_s3_client()
    s3_client.create_bucket(Bucket='test-bucket',
                            CreateBucketConfiguration={
                                'LocationConstraint': 'eu-west-2'})
    s3_client.put_object(Bucket='test-bucket', Key='test-file.csv',
                         Body='name,email\nJohn Doe,john@example.com')

    content = get_s3_file_content(s3_client, 'test-bucket', 'test-file.csv')
    assert content == 'name,email\nJohn Doe,john@example.com'


@mock_aws
def test_obfuscate_pii_fields():
    data = """name,email,phone
John Doe,john@example.com,1234567890
Jane Smith,jane@example.com,0987654321"""
    pii_fields = ['name', 'email']
    s3_client = get_s3_client()
    s3_client.create_bucket(Bucket='test-bucket',
                            CreateBucketConfiguration={
                                'LocationConstraint': 'eu-west-2'})
    s3_client.put_object(Bucket='test-bucket', Key='test/key.csv', Body=data)
    obfuscated_data, df = obfuscate_pii_fields(s3_client, 'test-bucket',
                                               pii_fields, 'test/key.csv')

    # Assert that the PII fields are obfuscated
    assert df['name'][0] == '***'
    assert df['email'][0] == '***'


@mock_aws
def test_put_s3_file():
    s3_client = get_s3_client()
    s3_client.create_bucket(Bucket='test-bucket',
                            CreateBucketConfiguration={
                                'LocationConstraint': 'eu-west-2'})

    data = 'name,email\nJohn Doe,john@example.com'.encode('utf-8')
    put_s3_file(s3_client, 'test-bucket', 'test-file.csv', data)

    response = s3_client.get_object(Bucket='test-bucket', Key='test-file.csv')
    content = response['Body'].read().decode('utf-8')
    assert content == 'name,email\nJohn Doe,john@example.com'


@mock_aws
def test_obfuscator(caplog):
    # Create a test bucket and upload a test file
    # with PII fields to obfuscate
    s3_client = get_s3_client()
    s3_client.create_bucket(Bucket='test-bucket',
                            CreateBucketConfiguration={
                                'LocationConstraint': 'eu-west-2'})

    data = 'name,email\nJohn Doe,john@example.com'.encode('utf-8')
    put_s3_file(s3_client, 'test-bucket', 'test-file.csv', data)

    # Define the payload
    payload = {
        'file_to_obfuscate': 's3://test-bucket/test-file.csv',
        'pii_fields': ['name', 'email'],
    }

    # Obfuscate the PII fields in the test file
    content, file_key = obfuscator(payload)
    assert content == b'name,email\n***,***\n'
    assert file_key == 'test-file.csv'


@mock_aws
def test_obfuscator_with_non_csv_file():
    s3_client = get_s3_client()
    s3_client.create_bucket(Bucket='test-bucket',
                            CreateBucketConfiguration={
                                'LocationConstraint': 'us-west-2'})
    s3_client.put_object(Bucket='test-bucket', Key='test-file.txt',
                         Body='This is a test file that is not a CSV.')

    payload = {
        'file_to_obfuscate': 's3://test-bucket/test-file.txt',
        'pii_fields': ['name', 'email']
    }

    with pytest.raises(ValueError,
                       match="The provided file is not a CSV file"):
        obfuscator(payload)
