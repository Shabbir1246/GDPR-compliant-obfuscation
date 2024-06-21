#!/bin/bash


#  change the location to the API Gateway end point for your instance (following is just an example)
#  change the file_to_obfuscate to the S3 location of the file you want to obfuscate
#  change the pii_fields to the fields you want to obfuscate

curl --location 'https://hylv4wxyw7.execute-api.ap-southeast-2.amazonaws.com/obfuscator' \
--header 'Content-Type: application/json' \
--data '{
    "file_to_obfuscate": "s3://nc-preobfuscation-data/new_data/student-dataset.csv",
    
    "pii_fields": ["name", "email"]
}'
