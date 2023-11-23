import hashlib


# Create a sample string
data = "Hello, World!"

# Initialize a hashlib object for SHA-256 hashing
sha256_hash = hashlib.sha256()

# Update the hash object with the bytes of the string
sha256_hash.update(data.encode('utf-8'))

# Get the hexadecimal representation of the hash
hash_hex = sha256_hash.hexdigest()

# Print the SHA-256 hash value
print("SHA-256 Hash (String):", hash_hex)

# Example 2: Hashing a File

# Specify the file you want to hash
file_path = "example.txt"

# Initialize a hashlib object for SHA-256 hashing
sha256_hash = hashlib.sha256()

# Open the file in binary mode and read it in chunks
with open(file_path, "rb") as file:
    while True:
        chunk = file.read(4096)  # Read 4 KB at a time
        if not chunk:
            break
        sha256_hash.update(chunk)

# Get the hexadecimal representation of the hash
hash_hex = sha256_hash.hexdigest()

# Print the SHA-256 hash value for the file
print("SHA-256 Hash (File):", hash_hex)
