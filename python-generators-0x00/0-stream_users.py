#!/usr/bin/env python3
from seed import connect_to_prodev
from typing import Generator, Dict, Any

def stream_users() -> Generator[Dict[str, Any], None, None]:
    """
    Generator function that fetches rows one by one from the user_data table.
    
    Yields:
        Dict[str, Any]: Each row as a dictionary with column names as keys
    """
    # Create database connection
    conn = connect_to_prodev()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data")
        
        # Single loop to fetch and yield rows one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield dict(row)
    
    finally:
        conn.close()

