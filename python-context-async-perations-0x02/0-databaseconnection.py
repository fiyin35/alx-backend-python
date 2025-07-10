import sqlite3

class DatabaseConnection:
    """
    A class-based context manager for handling database connections.
    Automatically opens and closes database connections using the with statement.
    """
    
    def __init__(self, database_path):
        """
        Initialize the context manager with the database path.
        
        Args:
            database_path (str): Path to the SQLite database file
        """
        self.database_path = database_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Enter the context manager - open the database connection.
        
        Returns:
            sqlite3.Connection: The database connection object
        """
        try:
            self.connection = sqlite3.connect(self.database_path)
            self.cursor = self.connection.cursor()
            print(f"Database connection opened: {self.database_path}")
            return self.connection
        except sqlite3.Error as e:
            print(f"Error opening database connection: {e}")
            raise
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - close the database connection.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_value: Exception value if an exception occurred
            traceback: Traceback object if an exception occurred
        
        Returns:
            bool: False to propagate exceptions, True to suppress them
        """
        if self.connection:
            try:
                if exc_type is None:
                    # No exception occurred, commit any pending transactions
                    self.connection.commit()
                    print("Database changes committed successfully")
                else:
                    # An exception occurred, rollback any pending transactions
                    self.connection.rollback()
                    print(f"Database transaction rolled back due to exception: {exc_value}")
                
                # Close the connection
                self.connection.close()
                print("Database connection closed")
                
            except sqlite3.Error as e:
                print(f"Error closing database connection: {e}")
        
        # Return False to propagate any exceptions that occurred
        return False


def setup_sample_database(db_path):
    """
    Create a sample database with users table for demonstration.
    
    Args:
        db_path (str): Path to the database file
    """
    try:
        with DatabaseConnection(db_path) as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER
                )
            ''')
            
            # Insert sample data (using INSERT OR IGNORE to avoid duplicates)
            sample_users = [
                ('John Doe', 'john.doe@example.com', 30),
                ('Jane Smith', 'jane.smith@example.com', 25),
                ('Bob Johnson', 'bob.johnson@example.com', 35),
                ('Alice Brown', 'alice.brown@example.com', 28),
                ('Charlie Wilson', 'charlie.wilson@example.com', 32)
            ]
            
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.executemany(
                    'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                    sample_users
                )
                print("Sample data inserted into users table")
            else:
                print(f"Users table already contains {count} records")
                
    except sqlite3.Error as e:
        print(f"Error setting up sample database: {e}")


def demonstrate_context_manager():
    """
    Demonstrate using the DatabaseConnection context manager.
    """
    database_path = 'users.db'
    
    print("=== Database Context Manager Demo ===\n")
    
    # First, set up the sample database
    print("1. Setting up sample database:")
    setup_sample_database(database_path)
    print()
    
    # Now demonstrate querying with the context manager
    print("2. Querying users with context manager:")
    try:
        with DatabaseConnection(database_path) as conn:
            cursor = conn.cursor()
            
            # Execute the query
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            
            # Print the results
            print("\nQuery Results:")
            print("-" * 60)
            print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Age':<5}")
            print("-" * 60)
            
            for row in results:
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<25} {row[3]:<5}")
            
            print(f"\nTotal users found: {len(results)}")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    print("\n3. Demonstrating error handling:")
    try:
        with DatabaseConnection(database_path) as conn:
            cursor = conn.cursor()
            
            # This will cause an error to demonstrate rollback
            cursor.execute("SELECT * FROM non_existent_table")
            
    except sqlite3.Error as e:
        print(f"Expected error caught: {e}")
    
    print("\n4. Demonstrating connection reuse:")
    try:
        with DatabaseConnection(database_path) as conn:
            cursor = conn.cursor()
            
            # Multiple queries in the same context
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"Total users: {count}")
            
            cursor.execute("SELECT name FROM users WHERE age > 30")
            older_users = cursor.fetchall()
            print(f"Users over 30: {[user[0] for user in older_users]}")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")


if __name__ == "__main__":
    demonstrate_context_manager()