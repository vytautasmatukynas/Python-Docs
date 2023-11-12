PACEHOLDER = "[name]"

# open name file and sort
with open("invited_names.txt") as names_file:
    names = names_file.readlines()
    print(names)

# change data to files
with open("starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()
    for name in names:
        name_strip = name.strip()
        new_letter = letter_contents.replace(PACEHOLDER, name_strip)
        print(new_letter)
        # create files
        with open(f"ready_letters_{name_strip}", "w") as ready_file:
            ready_file.write(new_letter)