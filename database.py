import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={os.getenv("AZURE_SERVER")};'
        f'DATABASE={os.getenv("AZURE_DATABASE")};'
        f'UID={os.getenv("AZURE_USERNAME")};'
        f'PWD={os.getenv("AZURE_PASSWORD")}'
    )
    return conn
