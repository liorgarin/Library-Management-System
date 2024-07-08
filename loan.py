from database import Database
from datetime import datetime, timedelta

class Loan:
    def __init__(self, db: Database):
        self.db = db

    def loan_book(self, cust_id, book_id):
        if not self.is_book_available(book_id):
            return False  # Book is not available for loan

        loan_date = datetime.now().strftime("%Y-%m-%d")
        book_type_query = "SELECT Type FROM Books WHERE Id = ?"
        book_type = self.db.fetch_one(book_type_query, (book_id,))[0]

        max_loan_days = {1: 10, 2: 5, 3: 2}[book_type]
        return_date = (datetime.now() + timedelta(days=max_loan_days)).strftime("%Y-%m-%d")

        query = "INSERT INTO Loans (CustID, BookID, LoanDate, ReturnDate) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (cust_id, book_id, loan_date, return_date))
        return True

    def return_book(self, cust_id, book_id):
        query = "DELETE FROM Loans WHERE CustID = ? AND BookID = ?"
        self.db.execute_query(query, (cust_id, book_id))

    def is_book_available(self, book_id):
        query = "SELECT * FROM Loans WHERE BookID = ?"
        loan = self.db.fetch_one(query, (book_id,))
        return loan is None

    def get_all_loans(self):
        query = """
        SELECT Customers.Id as CustomerId, Customers.Name as CustomerName, Books.Id as BookId, Books.Name as BookName, Loans.LoanDate, Loans.ReturnDate
        FROM Loans
        JOIN Customers ON Loans.CustID = Customers.Id
        JOIN Books ON Loans.BookID = Books.Id
        """
        loans = self.db.fetch_all(query)
        return loans

    def get_late_loans(self):
        today = datetime.now().strftime("%Y-%m-%d")
        query = "SELECT * FROM Loans WHERE ReturnDate < ?"
        return self.db.fetch_all(query, (today,))
