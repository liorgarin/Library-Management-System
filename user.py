from database import Database
import hashlib

class UserManager:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, username, password, age, city):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "INSERT INTO Users (Username, Password, Age, City) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (username, hashed_password, age, city))

    def verify_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "SELECT * FROM Users WHERE Username = ? AND Password = ?"
        return self.db.fetch_one(query, (username, hashed_password))
