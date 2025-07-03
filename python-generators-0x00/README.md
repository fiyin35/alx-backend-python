# Python Generators
# This directory contains projects and exercises focused on Python generators and their applications, including streaming data from a database and implementing lazy pagination.

#  Topics Covered
Creating and using generator functions
Streaming database records efficiently
Lazy evaluation and memory efficiency
Implementing pagination with generators
Files
0-stream_users.py: Generator that streams user records from a MySQL database one at a time.
1-main.py: Example usage of the streaming generator to print the first few users.
2-lazy_paginate.py: Implements lazy pagination using generators to fetch batches of users from the database.
4-stream-ages.py: Generator that streams only the ages of users from the database.
seed.py: Utility functions for database connection, table creation, and seeding data.
Usage
To run an example script:

python3 1-main.py
Requirements
Python 3.x
mysql-connector-python
python-dotenv
A running MySQL server with the appropriate database and table
