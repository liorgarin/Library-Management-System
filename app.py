from flask import Flask, render_template, request, redirect, url_for, session
from database import Database
from user import UserManager
from customer import Customer
from book import Book
from loan import Loan

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = Database('library.db')
user_manager = UserManager(db)
customer_manager = Customer(db)
book_manager = Book(db)
loan_manager = Loan(db)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        city = request.form['city']
        user_manager.create_user(username, password, age, city)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_manager.verify_user(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        year_published = request.form['year_published']
        book_type = request.form['book_type']
        book_manager.add_book(name, author, year_published, book_type)
        return redirect(url_for('view_books'))
    return render_template('add_book.html')

@app.route('/view_books')
def view_books():
    if 'username' not in session:
        return redirect(url_for('login'))
    books = book_manager.get_all_books()
    return render_template('view_books.html', books=books)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']
        email = request.form['email']
        customer_manager.add_customer(name, city, age, email)
        return redirect(url_for('view_customers'))
    return render_template('add_customer.html')

@app.route('/view_customers')
def view_customers():
    if 'username' not in session:
        return redirect(url_for('login'))
    customers = customer_manager.get_all_customers()
    return render_template('view_customers.html', customers=customers)

@app.route('/loan_book', methods=['GET', 'POST'])
def loan_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        cust_id = request.form['cust_id']
        book_id = request.form['book_id']
        if loan_manager.loan_book(cust_id, book_id):
            return redirect(url_for('view_loans'))
        else:
            flash("Book is already loaned out and not yet returned.", "error")
            return redirect(url_for('loan_book'))
    customers = customer_manager.get_all_customers()
    books = book_manager.get_all_books()
    
    # Add book type information
    book_types = {
        1: "up to 10 days",
        2: "up to 5 days",
        3: "up to 2 days"
    }
    
    books_with_type = []
    for book in books:
        book_id, book_name, _, _, book_type = book
        book_type_meaning = book_types[book_type]
        books_with_type.append((book_id, book_name, book_type, book_type_meaning))
    
    return render_template('loan_book.html', customers=customers, books=books_with_type, loan_manager=loan_manager)

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        cust_id = request.form['cust_id']
        book_id = request.form['book_id']
        loan_manager.return_book(cust_id, book_id)
        return redirect(url_for('view_loans'))
    
    customers = customer_manager.get_all_customers()
    
    # Fetch books loaned to the selected customer
    loans = loan_manager.get_all_loans()
    customer_books = {}
    for loan in loans:
        cust_id, cust_name, book_id, book_name, loan_date, return_date = loan
        if cust_id not in customer_books:
            customer_books[cust_id] = []
        customer_books[cust_id].append((book_id, book_name))
    
    return render_template('return_book.html', customers=customers, customer_books=customer_books)

@app.route('/view_loans')
def view_loans():
    if 'username' not in session:
        return redirect(url_for('login'))
    loans = loan_manager.get_all_loans()
    print("Loans Data Passed to Template: ", loans)  # Debugging print statement
    return render_template('view_loans.html', loans=loans)

@app.route('/late_loans')
def late_loans():
    if 'username' not in session:
        return redirect(url_for('login'))
    late_loans = loan_manager.get_late_loans()
    return render_template('late_loans.html', late_loans=late_loans)

if __name__ == '__main__':
    app.run(debug=True)
