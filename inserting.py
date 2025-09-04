import sqlite3

# All verified URLs to add
new_sites = [
    # 1. Central Government & Key Ministries
    "https://www.pmindia.gov.in",
    "https://www.india.gov.in",
    "https://www.meity.gov.in",
    "https://www.mha.gov.in",
    "https://www.mea.gov.in",
    "https://pib.gov.in",

    # 2. Parliament & Judiciary
    "https://loksabha.nic.in",
    "https://rajyasabha.nic.in",
    "https://www.sci.gov.in",
    "https://www.highcourtofgujarat.nic.in",

    # 3. Law Enforcement & Security
    "https://cbi.gov.in",
    "https://ncb.gov.in",
    "https://ncrb.gov.in",
    "https://bsf.gov.in",

    # 4. Education (National)
    "https://www.nios.ac.in",
    "https://jeemain.nta.ac.in",
    "https://neet.nta.nic.in",
    "https://cuet.samarth.ac.in",
    "https://scholarships.gov.in",

    # 5. Gujarat State Specific
    "https://www.gujaratuniversity.ac.in",
    "https://www.gtu.ac.in",
    "https://www.spuvvn.edu",
    "https://gsssb.gujarat.gov.in",
    "https://gpsc.gujarat.gov.in",
    "https://sebs.gujarat.gov.in",

    # 6. Finance & Banking
    "https://www.npci.org.in",
    "https://www.sbi.co.in",
    "https://www.bankofbaroda.in",

    # 7. Science & Technology
    "https://www.isro.gov.in",
    "https://www.drdo.gov.in",
    "https://www.csir.res.in",

    # 8. News & Media (Govt Only)
    "https://newsonair.gov.in",
    "https://ddnews.gov.in",
]

# Connect to database
conn = sqlite3.connect("verified_sites.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS verified_sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE
)
""")

# Insert and track newly added
added = []
for url in new_sites:
    cursor.execute("INSERT OR IGNORE INTO verified_sites (url) VALUES (?)", (url,))
    if cursor.rowcount > 0:
        added.append(url)

conn.commit()

# Show results
if added:
    print("✅ Newly added sites:")
    for u in added:
        print("   -", u)
else:
    print("ℹ️ No new sites added (all were already in DB)")

cursor.execute("SELECT COUNT(*) FROM verified_sites")
print("\n📊 Total verified sites in database:", cursor.fetchone()[0])

conn.close()
