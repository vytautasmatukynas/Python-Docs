import os

# Get the current working directory
current_directory = os.getcwd()
print("Current Directory:", current_directory)

# Get the user's home directory
home_directory = os.path.expanduser("~")
print("Home Directory:", home_directory)

# Get the real (canonical) path of a given path
given_path = "~/Desktop/../Documents/file.txt"
real_path = os.path.realpath(given_path)
print("Real Path:", real_path)

# Get the absolute path of a relative path
relative_path = "../path/to/some/file.txt"
absolute_path = os.path.abspath(relative_path)
print("Absolute Path:", absolute_path)

# Get the base name (last part) of a path
path_to_split = "/path/to/some/file.txt"
base_name = os.path.basename(path_to_split)
print("Base Name:", base_name)

# Get the directory name of a path
directory_name = os.path.dirname(path_to_split)
print("Directory Name:", directory_name)

# Split the path into directory and base name
dir_name, base_name = os.path.split(path_to_split)
print("Directory Name:", dir_name)
print("Base Name:", base_name)

# Get the size of a file in bytes
file_path = "/path/to/some/file.txt"
file_size = os.path.getsize(file_path)
print("File Size:", file_size, "bytes")

# Get information about a file or directory
file_info = os.stat(file_path)
print("File Info:", file_info)

# Check if a path is an absolute path
is_absolute = os.path.isabs(relative_path)
print("Is Absolute Path?", is_absolute)

# Get a list of all drives on Windows (returns empty list on non-Windows)
drive_list = os.listdir("/")
print("Drive List:", drive_list)

# Get environment variables
env_var_value = os.environ.get("PATH")  # Example: Retrieving the value of the PATH variable
print("PATH Environment Variable:", env_var_value)

# Change the current working directory
new_directory = "/path/to/new/directory"
os.chdir(new_directory)
print("Changed to:", os.getcwd())

# List files and directories in a directory
directory_contents = os.listdir()
print("Directory Contents:", directory_contents)

# Check if a path exists
path_to_check = "/path/to/check"
if os.path.exists(path_to_check):
    print("Path exists:", path_to_check)
else:
    print("Path does not exist:", path_to_check)

# Check if a path is a file
file_path = "/path/to/some/file.txt"
if os.path.isfile(file_path):
    print("It's a file:", file_path)
else:
    print("It's not a file:", file_path)

# Check if a path is a directory
directory_path = "/path/to/some/directory"
if os.path.isdir(directory_path):
    print("It's a directory:", directory_path)
else:
    print("It's not a directory:", directory_path)

# Join paths intelligently, handling separators
path1 = "/path/to/some"
path2 = "subdirectory"
full_path = os.path.join(path1, path2)
print("Joined Path:", full_path)

# Split a path into directory and filename
path_to_split = "/path/to/some/file.txt"
directory, filename = os.path.split(path_to_split)
print("Directory:", directory)
print("Filename:", filename)

# Create a new directory
new_directory_path = "/path/to/new/directory"
os.makedirs(new_directory_path, exist_ok=True)  # Creates recursively

# Remove a file
file_to_remove = "/path/to/file/to/remove.txt"
os.remove(file_to_remove)
print("Removed:", file_to_remove)

# Remove an empty directory
empty_directory = "/path/to/empty/directory"
os.rmdir(empty_directory)
print("Removed:", empty_directory)

# Remove a directory and its contents recursively
directory_to_remove = "/path/to/directory/to/remove"
os.system("rm -r " + directory_to_remove)
print("Removed:", directory_to_remove)



