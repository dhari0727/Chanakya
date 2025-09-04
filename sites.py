import sqlite3

# Connect to DB
conn = sqlite3.connect("verified_sites.db")
cursor = conn.cursor()

# Fetch all URLs
cursor.execute("SELECT url FROM verified_sites ORDER BY id ASC")
urls = cursor.fetchall()

# Build HTML content
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Verified Sites</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f4f4f9; }
        h1 { text-align: center; color: #333; }
        ul { list-style: none; padding: 0; }
        li { margin: 8px 0; }
        a { text-decoration: none; color: #007bff; }
        a:hover { text-decoration: underline; }
        .card {
            max-width: 600px;
            margin: auto;
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>✅ Verified Sites</h1>
        <ul>
"""

# Add each URL as a list item
for (url,) in urls:
    html_content += f'            <li><a href="{url}" target="_blank">{url}</a></li>\n'

# Close HTML
html_content += """        </ul>
    </div>
</body>
</html>
"""

# Save HTML file
with open("verified_sites.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ HTML file 'verified_sites.html' created successfully!")