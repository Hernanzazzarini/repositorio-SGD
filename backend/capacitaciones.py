import mysql.connector
from mysql.connector import Error
from conexion import create_db_connection, close_db_connection
from tabulate import tabulate


def crear_capacitacion(conexion, nombre_capacitacion):
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO capacitaciones (nombre_capacitacion) VALUES (%s)"
        cursor.execute(query, (nombre_capacitacion,))
        conexion.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error al crear capacitación: {e}")
        return None
    finally:
        if cursor:
            cursor.close()


def listar_capacitaciones(conexion):
    try:
        cursor = conexion.cursor()
        query = "SELECT * FROM capacitaciones"
        cursor.execute(query)

        categorias = cursor.fetchall()

        if categorias:
            print("\nLista de capacitaciones:")
            for categoria in categorias:
                print(categoria[0], categoria[1])
        else:
            print("No hay capacitaciones registradas.")
    except mysql.connector.Error as e:
        print(f"Error al listar capacitaciones: {e}")
    finally:
        if cursor:
            cursor.close()

def eliminar_capacitacion(conexion, id_capacitacion):
    try:
        cursor = conexion.cursor()
        query = "DELETE FROM capacitaciones WHERE id_capacitacion = %s"
        cursor.execute(query, (id_capacitacion,))
        conexion.commit()
        print("Capacitación eliminada correctamente.")
    except mysql.connector.Error as e:
        print(f"Error al eliminar capacitación: {e}")
    finally:
        if cursor:
            cursor.close()


def capacitaciones(conexion):
    while True:
        print("\nMenú:")
        print("1. Cargar capacitacion")
        print("2. Listar capacitaciones")
        print("3. Eliminar capacitaciones")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            nombre_capacitacion = input("Nombre de la nueva capacitacion: ")
            crear_capacitacion(conexion, nombre_capacitacion)
            print("Categoría creada")

        elif opcion == "2":
            listar_capacitaciones(conexion)
            
        elif opcion == "3":
            id_capacitacion = int(input("ID de la categoría a eliminar: "))
            eliminar_capacitacion(conexion, id_capacitacion)
            print("Capacitacion eliminada")
            
        elif opcion == "4":
            print("salio del modulo capacitaciones")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    conexion = create_db_connection()

    try:
        if conexion:
            capacitaciones(conexion)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conexion:
            close_db_connection(conexion)
