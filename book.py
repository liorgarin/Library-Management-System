from database import Database

class Book:
    def __init__(self, db: Database):
        self.db = db

    def add_book(self, name, author, year_published, book_type):
        query = "INSERT INTO Books (Name, Author, YearPublished, Type) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (name, author, year_published, book_type))

    def get_all_books(self):
        query = "SELECT * FROM Books"
        return self.db.fetch_all(query)

    def find_book_by_name(self, name):
        query = "SELECT * FROM Books WHERE Name LIKE ?"
        return self.db.fetch_all(query, ('%' + name + '%',))

    def remove_book(self, book_id):
        query = "DELETE FROM Books WHERE Id = ?"
        self.db.execute_query(query, (book_id,))
