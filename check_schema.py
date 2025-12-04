import sqlite3

# Connect to the database
conn = sqlite3.connect('/data/snmp_metrics.db')
cursor = conn.cursor()

# Get table info for metrics
cursor.execute('PRAGMA table_info(metrics)')
cols = cursor.fetchall()
print(f'Metrics columns: {len(cols)}')
for col in cols:
    print(f'  {col[0]}: {col[1]} ({col[2]})')

# Get table info for last_metrics
cursor.execute('PRAGMA table_info(last_metrics)')
cols = cursor.fetchall()
print(f'\nLast metrics columns: {len(cols)}')
for col in cols:
    print(f'  {col[0]}: {col[1]} ({col[2]})')

conn.close()