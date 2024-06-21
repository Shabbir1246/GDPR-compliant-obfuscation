from src.utils.obfuscator import obfuscator

# if __name__ == "main":
payload = {
    "file_to_obfuscate": "s3://nc-preobfuscation-data/new_data/test_data.csv",
    "pii_fields": ["name", "email","phone_number"]
}
print(obfuscator(payload))
