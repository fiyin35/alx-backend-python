import time
import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that automatically handles database connection opening and closing.
    Creates a connection, passes it as the first argument to the decorated function,
    and ensures the connection is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        
        try:
            # Call the original function with connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection, even if an exception occurs
            conn.close()
    
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function a specified number of times if it raises an exception.
    
    Args:
        retries (int): Number of retry attempts (default: 3)
        delay (int): Delay in seconds between retries (default: 2)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            # Try the function up to (retries + 1) times (initial attempt + retries)
            for attempt in range(retries + 1):
                try:
                    # Attempt to execute the function
                    result = func(*args, **kwargs)
                    return result
                    
                except Exception as e:
                    last_exception = e
                    
                    # If this was the last attempt, re-raise the exception
                    if attempt == retries:
                        print(f"Function '{func.__name__}' failed after {retries + 1} attempts")
                        raise last_exception
                    
                    # Log the retry attempt
                    print(f"Attempt {attempt + 1} failed for '{func.__name__}': {str(e)}")
                    print(f"Retrying in {delay} seconds... ({retries - attempt} attempts remaining)")
                    
                    # Wait before retrying
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            raise last_exception
        
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)