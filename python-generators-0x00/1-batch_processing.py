#!/usr/bin/env python3
from seed import connect_to_prodev
from typing import Generator, List, Dict, Any

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Generator function that fetches rows in batches from the users database.
    
    Args:
        batch_size (int): Number of rows to fetch per batch
    
    Yields:
        List[Dict[str, Any]]: Each batch as a list of dictionaries
    """
    # Create database connection
    conn = connect_to_prodev()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        
        # Loop 1: Fetch rows in batches
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            
            # Convert rows to list of dictionaries
            batch = [dict(row) for row in rows]
            yield batch
    
    finally:
        conn.close()


def batch_processing(batch_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Process each batch to filter users over the age of 25.
    
    Args:
        batch_size (int): Number of rows to process per batch
    
    Yields:
        List[Dict[str, Any]]: Filtered batch containing only users over 25
    """
    # Loop 2: Process each batch from the stream
    for batch in stream_users_in_batches(batch_size):
        filtered_users = []
        
        # Loop 3: Filter users in current batch
        for user in batch:
            if user.get('age', 0) > 25:
                filtered_users.append(user)
        
        # Only yield batch if it contains filtered users
        if filtered_users:
            yield filtered_users


# Example usage:
if __name__ == "__main__":
    batch_size = 10
    
    print("Processing users in batches, filtering for age > 25:")
    
    # Process batches and print results
    for filtered_batch in batch_processing(batch_size):
        print(f"Batch of {len(filtered_batch)} users over 25:")
        for user in filtered_batch:
            print(f"  - {user.get('name', 'Unknown')}, Age: {user.get('age', 'Unknown')}")
        print("---")