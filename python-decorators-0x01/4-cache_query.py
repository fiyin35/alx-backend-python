import time
import sqlite3 
import functools


query_cache = {}

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    Uses the query parameter as the cache key.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from kwargs or args
        query = kwargs.get('query')
        if query is None:
            # If query is not in kwargs, look for it in args
            # Assuming query is the second argument after conn
            if len(args) >= 2:
                query = args[1]
            else:
                # If we can't find the query, don't cache
                return func(*args, **kwargs)
        
        # Check if result is already cached
        if query in query_cache:
            print(f"Cache hit for query: {query[:50]}...")
            return query_cache[query]
        
        # Execute the function and cache the result
        print(f"Cache miss for query: {query[:50]}...")
        result = func(*args, **kwargs)
        query_cache[query] = result
        
        return result
    
    return wrapper

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

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()