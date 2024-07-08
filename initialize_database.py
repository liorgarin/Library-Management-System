import sqlite3

def create_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        Id INTEGER PRIMARY KEY,
        Username TEXT NOT NULL,
        Password TEXT NOT NULL,
        Age INTEGER NOT NULL,
        City TEXT NOT NULL
    )
    ''')

    # Create Customers table with Email column
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        Id INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        City TEXT NOT NULL,
        Age INTEGER NOT NULL,
        Email TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        Id INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Author TEXT NOT NULL,
        YearPublished INTEGER NOT NULL,
        Type INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Loans (
        CustID INTEGER,
        BookID INTEGER,
        LoanDate TEXT NOT NULL,
        ReturnDate TEXT NOT NULL,
        FOREIGN KEY (CustID) REFERENCES Customers(Id),
        FOREIGN KEY (BookID) REFERENCES Books(Id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
