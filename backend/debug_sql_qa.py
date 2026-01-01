import sys
import os
import traceback

print(f"Python: {sys.version}")
print(f"CWD: {os.getcwd()}")
print(f"Files: {os.listdir('.')}")

try:
    import sqlite3
    print("Sqlite3 OK")
    import openai
    print("OpenAI OK")
    import sql_qa
    print("SQL_QA Import OK")
    
    # Test DB connection
    print(f"DB Path: {sql_qa.CHINOOK_DB_PATH}")
    if os.path.exists(sql_qa.CHINOOK_DB_PATH):
        print("DB File exists")
        conn = sqlite3.connect(f"file:{sql_qa.CHINOOK_DB_PATH}?mode=ro", uri=True)
        print("DB Connect OK")
        conn.close()
    else:
        print("DB File MISSING")

except Exception:
    traceback.print_exc()
