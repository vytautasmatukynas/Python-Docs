class Book():

    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __repr__(self):
        """returns 'str', something like __str__, just this is __repr__ representation, others uses __str__"""
        return f"Title: {self.title}, Author: {self.author}"

    def __len__(self):
        """returns 'len'"""
        return self.pages

mybook = Book("ooooooo", "kazkas", 300)
print(mybook)
print(len(mybook))