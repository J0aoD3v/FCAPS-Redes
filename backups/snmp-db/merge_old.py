import sqlite3

src = sqlite3.connect('/tmp/old_check.db')
dst = sqlite3.connect('/data/snmp_metrics.db')

src_data = src.execute('SELECT * FROM metrics').fetchall()
inserted = 0

for row in src_data:
    try:
        dst.execute('INSERT OR IGNORE INTO metrics VALUES (?,?,?,?,?,?,?)', row)
        if dst.total_changes > 0:
            inserted += 1
    except Exception as e:
        pass

dst.commit()
print(f'Inserted {inserted} new records from old database')
print(f'Total records now: {dst.execute("SELECT COUNT(*) FROM metrics").fetchone()[0]}')

src.close()
dst.close()
