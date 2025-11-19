import sqlite3
import pandas as pd

def export_saints_to_csv(db_path, csv_path):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM saints"  # Change 'saints' if your table name is different
    df = pd.read_sql_query(query, conn)
    df.to_csv(csv_path, index=False)
    conn.close()
    print(f"Exported table 'saints' to {csv_path}")

if __name__ == "__main__":
    export_saints_to_csv("scotsirishsaints.db", "saints.csv")
