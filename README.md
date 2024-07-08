# Library Management System

A simple library management system built with Flask and SQLite.

## Features

- User registration and login
- Add, view, loan, and return books
- View and manage customers
- View all loans and late loans

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/Library-Management-System.git
    cd Library-Management-System
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Initialize the database:

    ```sh
    python initialize_database.py
    ```

## Usage

1. Run the application:

    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
