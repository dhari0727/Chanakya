import sqlite3

# Full list of verified site URLs
sites = [
    "https://www.g20.in/en/g20-india-2023/new-delhi-summit/new-delhi-summit.html",
    "https://gujaratindia.gov.in/Index",
    "https://www.india.gov.in/",
    "https://uidai.gov.in/",
    "https://www.passportindia.gov.in/psp",
    "https://www.epfindia.gov.in/site_en/index.php",
    "https://www.incometax.gov.in/iec/foportal/",
    "https://www.python.org",
    "https://www.madhubanresortsandspa.co.in",
    "https://madhubhanresortandspa.com/"
]

# Connect to the database
conn = sqlite3.connect("verified_sites.db")
cursor = conn.cursor()

# Empty the table
cursor.execute("DELETE FROM verified_sites")

# Insert new URLs
for url in sites:
    cursor.execute("INSERT INTO verified_sites (url) VALUES (?)", (url,))

conn.commit()
conn.close()
print("✅ Verified sites table updated successfully")
