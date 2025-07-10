import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_name='users.db'):
        self.query = query
        self.params = params or ()
        self.db_name = db_name
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open database connection and execute the query
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always close the connection
        if self.conn:
            self.conn.close()

# --- Usage
query = "SELECT * FROM users WHERE age > ?"
param = (25,)

with ExecuteQuery(query, param) as results:
    print("Query Results:")
    for row in results:
        print(row)
