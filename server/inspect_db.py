import sqlite3
import os

def inspect_database():
    db_path = os.path.join(os.path.dirname(__file__), 'bible-sqlite.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Database Tables:")
    for table in tables:
        print(f"\nTable: {table[0]}")
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Get sample data
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 1")
        sample = cursor.fetchone()
        if sample:
            print("Sample data:")
            print(f"  {sample}")
    
    conn.close()

if __name__ == '__main__':
    inspect_database()