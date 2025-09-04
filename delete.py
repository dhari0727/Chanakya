import sqlite3



# Connect to the database
conn = sqlite3.connect("verified_sites.db")
cursor = conn.cursor()

# Empty the table
cursor.execute("DELETE FROM verified_sites where url = 'www.cbibt.com'")


conn.commit()
conn.close()
print("✅ Verified sites table updated successfully")
