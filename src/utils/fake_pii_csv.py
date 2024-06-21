import os
import csv
from faker import Faker

fake = Faker()

# Define the headers for your CSV file
headers = ['student_id', 'name', 'course', 'cohort', 'graduation_date',
           'email', 'phone_number']
# Open the file in write mode
with open('test_data.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)

    # Write the headers to the CSV file
    writer.writeheader()

    # Keep adding rows until the file size is approximately 1 MB
    while os.path.getsize('test_data.csv') < 1024 * 1024:
        writer.writerow({
            'student_id': fake.random_int(min=1000, max=9999),
            'name': fake.name(),
            'course': fake.random_element(elements=(
                        'Math', 'Science', 'History', 'English')),
            'cohort': fake.random_element(
                elements=('Software', 'Cloud', 'DE')),
            'graduation_date': fake.date_this_decade(),

            'email': fake.email(),
            'phone_number': fake.phone_number(),
        })
