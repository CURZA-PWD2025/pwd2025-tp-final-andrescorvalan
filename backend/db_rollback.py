import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()
database_name = os.getenv("DB_NAME")

database_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'port': os.getenv("DB_PORT"),
    'raise_on_warnings': True,
    "database": database_name
}

DROPPED_TB = {}

DROPPED_TB["VETERINARIO_ESPECIALIDAD"] = "DROP TABLE IF EXISTS VETERINARIO_ESPECIALIDAD;"
DROPPED_TB["VETERINARIOS"] = "DROP TABLE IF EXISTS VETERINARIOS;"
DROPPED_TB["ESPECIALIDADES"] = "DROP TABLE IF EXISTS ESPECIALIDADES;"
DROPPED_TB["MASCOTAS"] = "DROP TABLE IF EXISTS MASCOTAS;"
DROPPED_TB["ESPECIES"] = "DROP TABLE IF EXISTS ESPECIES;"
DROPPED_TB["PROPIETARIOS"] = "DROP TABLE IF EXISTS PROPIETARIOS;"

def rollback_db():
    cxn = mysql.connector.connect(**database_config)
    cursor = cxn.cursor()
    for table in DROPPED_TB:
        print(f"Dropped table: {table}", end=" ")
        try:
            cursor.execute(DROPPED_TB[table])
            print('ok')
            cxn.commit()
        except Error as e:
            print(f"{e}")
    
    cursor.close()
    cxn.close()

if __name__ == "__main__":
    rollback_db()