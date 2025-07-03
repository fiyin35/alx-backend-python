#!/usr/bin/env python3
from seed import connect_to_prodev
from typing import Generator, List, Dict, Any

def paginate_users(page_size: int, offset: int) -> List[Dict[str, Any]]:
    """
    Fetch a specific page of users from the database.
    
    Args:
        page_size (int): Number of users to fetch per page
        offset (int): Starting position for the page (0-indexed)
    
    Returns:
        List[Dict[str, Any]]: List of users for the requested page
    """
    # Create database connection
    conn = connect_to_prodev()
    
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users LIMIT ? OFFSET ?", (page_size, offset))
        rows = cursor.fetchall()
        
        # Convert rows to list of dictionaries
        return [dict(row) for row in rows]
    
    finally:
        conn.close()


def lazy_paginate(page_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Generator function that lazily loads paginated data from the users database.
    Only fetches the next page when needed, starting at offset 0.
    
    Args:
        page_size (int): Number of users to fetch per page
    
    Yields:
        List[Dict[str, Any]]: Each page as a list of user dictionaries
    """
    offset = 0
    
    # Single loop to fetch pages lazily
    while True:
        # Fetch the current page
        page_data = paginate_users(page_size, offset)
        
        # If no data returned, we've reached the end
        if not page_data:
            break
        
        # Yield the current page
        yield page_data
        
        # Move to the next page
        offset += page_size


# Example usage:
if __name__ == "__main__":
    page_size = 5
    
    print(f"Lazily paginating users with page size: {page_size}")
    
    # Process pages lazily - only fetches when needed
    for page_num, page in enumerate(lazy_paginate(page_size), 1):
        print(f"\nPage {page_num} ({len(page)} users):")
        for user in page:
            print(f"  - ID: {user.get('id', 'Unknown')}, Name: {user.get('name', 'Unknown')}")
        
        # Example: Break after 3 pages to demonstrate lazy loading
        if page_num >= 3:
            print("\n... (stopping after 3 pages for demo)")
            break