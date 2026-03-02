import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Presume that database and tables have beeen created
cursor.execute('''SELECT * FROM page''')

for row in cursor.fetchall():
    print(row)
    # Process each row as needed

conn.close()
