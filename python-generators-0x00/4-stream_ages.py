#!/usr/bin/env python3
from seed import connect_to_prodev
from typing import Generator

def stream_user_ages() -> Generator[int, None, None]:
    """
    Generator function that yields user ages one by one from the database.
    
    Yields:
        int: Each user's age
    """
    # Create database connection
    conn = connect_to_prodev()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM users WHERE age IS NOT NULL")
        
        # Loop 1: Fetch and yield ages one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]  # Yield the age value
    
    finally:
        conn.close()


def calculate_average_age() -> float:
    """
    Calculate the average age of users using the generator.
    Memory-efficient approach that doesn't load entire dataset.
    
    Returns:
        float: Average age of all users
    """
    total_age = 0
    user_count = 0
    
    # Loop 2: Process each age from the generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    # Calculate and return average
    if user_count == 0:
        return 0.0
    print
    return total_age / user_count

# Main execution
if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
    
    # Optional: Demonstrate the memory efficiency
    print(f"\nMemory-efficient calculation completed!")
    print("Ages were processed one by one without loading entire dataset into memory.")