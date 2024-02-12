import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            port=3306,
            password='hernan',
            database='dbolega'
        )
        if conexion.is_connected():
            print("Conexión a la base de datos exitosa")
        return conexion
    except Error as e:
        print(f"Error durante la conexión a la base de datos: {e}")
        return None

def close_db_connection(conexion):
    if conexion.is_connected():
        conexion.close()
        print("Conexión a la base de datos cerrada")

