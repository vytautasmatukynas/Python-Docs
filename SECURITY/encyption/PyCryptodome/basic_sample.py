from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

# Define the password and generate a salt
password = "my_secure_password".encode('utf-8')
salt = get_random_bytes(16)

# Hash the password using PBKDF2 with SHA-256
# PBKDF2 applies a key derivation function with multiple iterations
# to make brute-force attacks more difficult.
key = PBKDF2(password, salt, dkLen=32, count=1000000, prf=lambda p, s: HMAC.new(p, s, SHA256).digest())

# Encode the salt and key as base64 strings for storage
salt_encoded = b64encode(salt).decode('utf-8')
key_encoded = b64encode(key).decode('utf-8')

# Print the salt and derived key (store these in your database)
print(f"Salt: {salt_encoded}")
print(f"Key: {key_encoded}")

# To verify a password, retrieve the stored salt and key from your database
# and use the same process to hash the provided password for comparison.

# Example verification code:
def verify_password(stored_salt, stored_key, provided_password):
    salt = b64decode(stored_salt)
    key = PBKDF2(provided_password.encode('utf-8'), salt, dkLen=32, count=1000000, prf=lambda p, s: HMAC.new(p, s, SHA256).digest())
    return b64encode(key).decode('utf-8') == stored_key

# Example usage:
stored_salt = "base64_encoded_salt"
stored_key = "base64_encoded_key"
provided_password = "user_provided_password"

if verify_password(stored_salt, stored_key, provided_password):
    print("Password is correct.")
else:
    print("Password is incorrect.")
