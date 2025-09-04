import sqlite3

# Connect to your database
conn = sqlite3.connect("verified_sites.db")
cursor = conn.cursor()

# Fetch all records from verified_sites table
cursor.execute("SELECT * FROM verified_sites")
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

conn.close()
