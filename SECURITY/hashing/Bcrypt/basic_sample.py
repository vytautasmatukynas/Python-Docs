import bcrypt

# Example 1: Hashing a Password

# Create a sample password
password = "my_secure_password".encode('utf-8')

# Hash the password with a randomly generated salt
salt = bcrypt.gensalt()  # Generate a new random salt
hashed_password = bcrypt.hashpw(password, salt)

# Print the hashed password (store this in your database)
print("Hashed Password:", hashed_password)

# Example 2: Verifying a Password

# Retrieve the stored hashed password from your database
stored_hashed_password = hashed_password

# Provide a password for verification
provided_password = "user_provided_password".encode('utf-8')

# Verify the provided password against the stored hash
if bcrypt.checkpw(provided_password, stored_hashed_password):
    print("Password is correct.")
else:
    print("Password is incorrect.")