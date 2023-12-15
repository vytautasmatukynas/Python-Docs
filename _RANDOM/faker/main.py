# Import the Faker library and create fake data. Data will be str.
from faker import Faker

# Create an instance of the Faker class
fake = Faker()

# Generate and print a fake name
fake_name = fake.name()
print("Name:", fake_name)

# Generate and print a fake address
fake_address = fake.address()
print("Address:", fake_address)

# Generate and print a fake email address
fake_email = fake.email()
print("Email:", fake_email)

# Generate and print a fake phone number
fake_phone_number = fake.phone_number()
print("Phone Number:", fake_phone_number)

# Generate and print a fake date of birth between ages 18 and 65
fake_date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=65)
print("Date of Birth:", fake_date_of_birth)

# Generate and print a fake job title
fake_job_title = fake.job()
print("Job Title:", fake_job_title)

# Generate and print a fake company name
fake_company_name = fake.company()
print("Company Name:", fake_company_name)

# Generate and print a fake country name
fake_country = fake.country()
print("Country:", fake_country)

# Generate and print fake text with a maximum of 200 characters
fake_text = fake.text(max_nb_chars=200)
print("Fake Text:")
print(fake_text)

# Generate and print a fake username
fake_username = fake.user_name()
print("Username:", fake_username)

# Generate and print a fake password with specified characteristics
fake_password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
print("Password:", fake_password)
