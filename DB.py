from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate
import threading
import sqlite3

Base = declarative_base()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


lock = threading.Lock()
class DBController:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.connection = sqlite3.connect('./test.db', check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def commit(self):
        self.connection.commit()
        
    def show_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        table_names = [table["name"] for table in tables]
        table_data = [["Table Name"]] + [[name] for name in table_names]
        print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    
    def desc_table(self, table_name):
        query = f"PRAGMA table_info({table_name});"
        self.cursor.execute(query)
        columns = self.cursor.fetchall()
        column_data = [["Column ID", "Name", "Type", "Not Null", "Default Value", "Primary Key"]]
        for col in columns:
            column_data.append([
                col["cid"], col["name"], col["type"], 
                bool(col["notnull"]), col["dflt_value"], bool(col["pk"])
            ])
        print(tabulate(column_data, headers="firstrow", tablefmt="grid"))
        
    def print_table(self, table_name):
        # Get the column names and data
        desc_query = f"PRAGMA table_info({table_name});"
        self.cursor.execute(desc_query)
        columns = self.cursor.fetchall()
        column_names = [col["name"] for col in columns]

        select_query = f"SELECT * FROM {table_name};"
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()

        # Format the data for printing
        table_data = [column_names] + [list(row) for row in rows]
        print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    
    def close(self):
        self.connection.close()
        DBController._instance = None

