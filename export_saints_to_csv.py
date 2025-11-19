import sqlite3
import pandas as pd

# Export the 'saints' table from scotsirishsaints.db to saints.csv
conn = sqlite3.connect('scotsirishsaints.db')
df = pd.read_sql_query('SELECT * FROM saints', conn)
df.to_csv('saints.csv', index=False)
conn.close()
print("Exported saints.csv to FlaskApp directory.")
