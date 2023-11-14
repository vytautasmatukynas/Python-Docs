"""
    seek() and tell() methods are used in file handling to control the position of the cursor within a file.
These methods are particularly useful when you need to navigate within a file to read or write data at specific
locations.

    Together, seek() and tell() allow you to navigate within a file and determine the current cursor position. This is
particularly useful when working with large files, binary data, or when you need to perform non-sequential read or
write operations. It's important to remember that the behavior of these methods can depend on the mode in which the
file was opened (read, write, binary, etc.)

    The seek() method is used to move the cursor (also known as the file pointer) to a specified position within the file.
It has two main parameters:
offset: This parameter specifies the number of bytes to move the cursor. It can be positive or negative.
whence (optional): This parameter specifies the reference point for the offset. It can take one of three values:
        0 (default): The offset is relative to the beginning of the file.
        1: The offset is relative to the current cursor position.
        2: The offset is relative to the end of the file.

####################################################
Example usage:
with open("example.txt", "r") as file:
    file.seek(10)      # Move the cursor to the 10th byte from the beginning
    file.seek(20, 0)   # Move the cursor to the 20th byte from the beginning
    file.seek(-5, 2)   # Move the cursor 5 bytes before the end of the file
####################################################

    The tell() method returns the current cursor position within the file. It doesn't take any parameters. The value
returned by tell() represents the number of bytes from the beginning of the file to the current cursor position.

####################################################
Example usage:
with open("example.txt", "r") as file:
    position = file.tell()  # Get the current cursor position
####################################################
"""
# example.txt:
# 123456789
# 123456789
# 123456789

file = open("example.txt", "r")  # Opening a file in read mode
content1 = file.read(10)  # Read the first 10 characters
print("Read content:", content1)
position1 = file.tell()  # Find the current cursor position
print("Current position:", position1)

file.seek(5)  # Move the cursor to the 10th byte from the beginning
content2 = file.read(10)  # Read the next 10 characters from position 5
print("Read content:", content2)
position2 = file.tell()  # Find the current cursor position
print("Current position:", position2)
file.close()  # Closing the file