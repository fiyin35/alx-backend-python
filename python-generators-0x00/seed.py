#!/usr/bin/env python3
"""
MySQL Database Setup Script for ALX_prodev
Creates database and user_data table with specified structure
"""

import mysql.connector
from mysql.connector import Error
import sys
import os
from getpass import getpass
import csv
import uuid

def connect_db():
    """
    Connects to the MySQL database server
    """
    try:
        host = input("Enter MySQL host (default: localhost): ") or 'localhost'
        user = input("Enter MySQL username (default: root): ") or 'root'
        password = getpass("Enter MySQL password: ")
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print(f"Successfully connected to MySQL server at {host}")
            return connection
    
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    """
    try:
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' created successfully (or already exists)")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"Error creating database: {e}")
        return False

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL
    """
    try:
        host = input("Enter MySQL host (default: localhost): ") or 'localhost'
        user = input("Enter MySQL username (default: root): ") or 'root'
        password = getpass("Enter MySQL password: ")
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database='ALX_prodev'
        )
        
        if connection.is_connected():
            print("Successfully connected to ALX_prodev database")
            return connection
    
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields
    """
    try:
        cursor = connection.cursor()
        
        # Create user_data table with specified structure
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_query)
        print("Table 'user_data' created successfully (or already exists)")
        
        # Create index on email for better query performance
        email_index_query = """
        CREATE INDEX IF NOT EXISTS idx_email ON user_data(email)
        """
        
        cursor.execute(email_index_query)
        print("Index on email created successfully")
        
        # Show table structure
        cursor.execute("DESCRIBE user_data")
        columns = cursor.fetchall()
        
        print("\nTable structure:")
        print("Column Name | Data Type | Null | Key | Default | Extra")
        print("-" * 60)
        for column in columns:
            print(f"{column[0]:<11} | {column[1]:<9} | {column[2]:<4} | {column[3]:<3} | {column[4]} | {column[5]}")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"Error creating table: {e}")
        return False
    
def insert_data(connection, csv_file='user_data.csv'):
    """
    Inserts data in the database from a CSV file if it does not exist
    CSV file should have columns: name, email, age
    """
    
    
    try:
        cursor = connection.cursor()
        
        # Check if CSV file exists
        if not os.path.exists(csv_file):
            print(f"Error: CSV file '{csv_file}' not found")
            return False
        
        inserted_count = 0
        skipped_count = 0
        
        # Read data from CSV file
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Validate CSV headers
            expected_columns = {'name', 'email', 'age'}
            if not expected_columns.issubset(csv_reader.fieldnames):
                print(f"Error: CSV file must contain columns: {expected_columns}")
                print(f"Found columns: {csv_reader.fieldnames}")
                return False
            
            print(f"Reading data from '{csv_file}'...")
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (header is row 1)
                try:
                    # Extract and validate data
                    name = row['name'].strip()
                    email = row['email'].strip()
                    age = int(row['age'])
                    
                    # Validate required fields
                    if not name or not email:
                        print(f"Row {row_num}: Skipping - missing name or email")
                        skipped_count += 1
                        continue
                    
                    if age <= 0:
                        print(f"Row {row_num}: Skipping - invalid age: {age}")
                        skipped_count += 1
                        continue
                    
                    # Generate UUID for user_id
                    user_id = str(uuid.uuid4())
                    
                    # Check if email already exists (assuming email should be unique)
                    check_query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
                    cursor.execute(check_query, (email,))
                    count = cursor.fetchone()[0]
                    
                    if count == 0:
                        # Insert data if it doesn't exist
                        insert_query = """
                        INSERT INTO user_data (user_id, name, email, age) 
                        VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(insert_query, (user_id, name, email, age))
                        print(f"Inserted record for user: {name} ({email})")
                        inserted_count += 1
                    else:
                        print(f"Record with email {email} already exists, skipping...")
                        skipped_count += 1
                
                except ValueError as ve:
                    print(f"Row {row_num}: Invalid data format - {ve}")
                    skipped_count += 1
                    continue
                except Exception as e:
                    print(f"Row {row_num}: Error processing row - {e}")
                    skipped_count += 1
                    continue
        
        connection.commit()
        
        print(f"\nData insertion summary:")
        print(f"Records inserted: {inserted_count}")
        print(f"Records skipped: {skipped_count}")
        
        # Display all data in the table
        cursor.execute("SELECT * FROM user_data")
        records = cursor.fetchall()
        
        print(f"\nTotal records in user_data table: {len(records)}")
        print("\nData in user_data table:")
        print("User ID | Name | Email | Age")
        print("-" * 80)
        for record in records:
            print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]}")
        
        cursor.close()
        return True
        
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found")
        return False
    except Error as e:
        print(f"Error inserting data: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
 


def main():
    """
    Main function to set up the database
    """
    print("MySQL Database Setup for ALX_prodev")
    print("=" * 40)
    
    # Step 1: Connect to MySQL server
    connection = connect_db()
    if not connection:
        print("Failed to connect to MySQL server. Exiting...")
        sys.exit(1)
    
    try:
        # Step 2: Create database
        if not create_database(connection):
            print("Failed to create database. Exiting...")
            sys.exit(1)
        
        # Close initial connection
        connection.close()
        
        # Step 3: Connect to ALX_prodev database
        prodev_connection = connect_to_prodev()
        if not prodev_connection:
            print("Failed to connect to ALX_prodev database. Exiting...")
            sys.exit(1)
        
        # Step 4: Create table
        if not create_table(prodev_connection):
            print("Failed to create table. Exiting...")
            sys.exit(1)
        
        # Step 5: Insert sample data (optional)
        insert_sample = input("\nDo you want to insert sample data? (y/n): ").lower()
        if insert_sample in ['y', 'yes']:
            # Sample data with UUID-style user_id
            sample_data = [
                ('550e8400-e29b-41d4-a716-446655440001', 'John Doe', 'john.doe@example.com', 25),
                ('550e8400-e29b-41d4-a716-446655440002', 'Jane Smith', 'jane.smith@example.com', 30),
                ('550e8400-e29b-41d4-a716-446655440003', 'Bob Johnson', 'bob.johnson@example.com', 35)
            ]
            
            if not insert_data(prodev_connection, sample_data):
                print("Failed to insert sample data.")
            else:
                print("Sample data inserted successfully!")
        
        print("\nDatabase setup completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        if 'prodev_connection' in locals() and prodev_connection.is_connected():
            prodev_connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    main()