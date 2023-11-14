# __name__ = The name of the class.
# __main__ = The current name of the module in which this code runs.
# The statement if __name__ == '__main__': checks if variable __name__
# is set to the string value '__main__' which holds only within the main
# source file from which you initially execute your code.  In all other
# contexts—such as in imported code files—the variable __name__ is set
# to a different value.
# This is useful because you usually don’t want to run code with side
# effects when importing modules.
def main():
    print(f"First Module's Name: {__name__}")

if __name__ == "__main__":
    main()