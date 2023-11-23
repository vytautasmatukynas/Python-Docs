from cryptography.fernet import Fernet

# Generate a new encryption key (you should save this securely)
key = Fernet.generate_key()
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

# Load the encryption key from a file (in practice, you would load this securely)
with open("encryption_key.key", "rb") as key_file:
    key = key_file.read()

# Initialize the Fernet symmetric key cipher with the loaded key
cipher_suite = Fernet(key)

# Specify the file you want to encrypt
input_file = "plaintext.txt"
output_file = "encrypted_file.encrypted"

# Read the file to be encrypted
with open(input_file, "rb") as file:
    plaintext = file.read()

# Encrypt the file contents
encrypted_data = cipher_suite.encrypt(plaintext)

# Write the encrypted data to a new file
with open(output_file, "wb") as file:
    file.write(encrypted_data)

print(f"File '{input_file}' has been encrypted to '{output_file}'")
