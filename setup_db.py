import sqlite3

# connect (will create verified_sites.db if not exists)
conn = sqlite3.connect("verified_sites.db")
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS verified_sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ verified_sites table created successfully.")
