from werkzeug.security import generate_password_hash, check_password_hash

# Create a password and hash it
password = "my_secure_password"
hashed_password = generate_password_hash(password, method='sha256')

# Print the hashed password (store this in your database)
print("Hashed Password:", hashed_password)

# Verify a provided password against the stored hash
provided_password = "user_provided_password"
if check_password_hash(hashed_password, provided_password):
    print("Password is correct.")
else:
    print("Password is incorrect.")
