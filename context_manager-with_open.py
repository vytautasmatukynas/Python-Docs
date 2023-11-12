## create file in local folder
with open("data.txt", 'w') as data:
    data.write('data input')

## dir starts in root folder "/" ABSOLUTE FILE PATH
with open("/folder/data.txt", 'w') as data:
    data.write('data input')

## dir starts in root folder "./" (formard) "../" (backwards) RELATIVE FILE PATH(working dir)
with open("./folder/data.txt", 'w') as data:
    data.write('data input')

## OR
with open("folder/data.txt", 'w') as data:
    data.write('data input')

## OR
with open("../folder/data.txt", 'w') as data:
    data.write('data input')


# Syntax:
# open(file, mode)
#
# Parameter -	Description
#
# file -	The path and name of the file
# mode -	A string, define which mode you want to open the file in:
#
# "r" - Read - Default value. Opens a file for reading, error if the file does not exist
#
# "a" - Append - Opens a file for appending, creates the file if it does not exist
#
# "w" - Write - Opens a file for writing, creates the file if it does not exist
#
# "x" - Create - Creates the specified file, returns an error if the file exist
#
# In addition you can specify if the file should be handled as binary or text mode
#
# "t" - Text - Default value. Text mode
#
# "b" - Binary - Binary mode (e.g. images)
