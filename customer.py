from database import Database

class Customer:
    def __init__(self, db: Database):
        self.db = db

    def add_customer(self, name, city, age, email):
        query = "INSERT INTO Customers (Name, City, Age, Email) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (name, city, age, email))

    def get_all_customers(self):
        query = "SELECT * FROM Customers"
        return self.db.fetch_all(query)

    def find_customer_by_name(self, name):
        query = "SELECT * FROM Customers WHERE Name LIKE ?"
        return self.db.fetch_all(query, ('%' + name + '%',))

    def remove_customer(self, customer_id):
        query = "DELETE FROM Customers WHERE Id = ?"
        self.db.execute_query(query, (customer_id,))
