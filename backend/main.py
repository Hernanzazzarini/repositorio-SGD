from conexion import create_db_connection, close_db_connection
from capacitaciones import capacitaciones
from personal import personal
from tareas import *
from trazabilidad import *
from trazabilidadlog import *



def verificar_credenciales(conexion, nombre_usuario, contrasena):
    try:
        cursor = conexion.cursor()
        query = "SELECT id_usuario, nombre_usuario FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
        cursor.execute(query, (nombre_usuario, contrasena))
        usuario = cursor.fetchone()

        return usuario  # Devuelve None si no se encuentra el usuario

    except Exception as e:
        print(f"Error al verificar credenciales: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

def menu_principal():
    while True:
        print("\n•·.·•·.··• SISTEMA DE GESTION DE DOCUMENTOS •·.·•·.·•·.·•·.·•\n")
        nombre_usuario = input("Ingrese su nombre de usuario: ")
        contrasena = input("Ingrese su contraseña: ")

        conexion = create_db_connection()

        if conexion:
            usuario = verificar_credenciales(conexion, nombre_usuario, contrasena)

            if usuario:
                print(f"Bienvenido, {usuario[1]}!")
                mostrar_menu_capacitaciones(conexion)
                break  # Sale del bucle cuando las credenciales son válidas
            else:
                print("Credenciales incorrectas. Por favor, inténtelo nuevamente.")

            close_db_connection(conexion)

def mostrar_menu_capacitaciones(conexion):
    while True:
        print("\nMENU DE CAPACITACIONES:")
        print("1. Gestionar Capacitaciones")
        print("2. Personal")
        print("3. cronograma de tareas")
        print("4. sistema de trazabilidad produccion")
        print("5. Sistema de trazabilidad expedicion ")
        print("6. Salir")

        opcion = input("\n⮞ Ingrese una opción: ")

        if opcion == "1":
            capacitaciones(conexion)
        elif opcion == "2":
            personal(conexion)
        elif opcion == "3" :
            tareas(conexion)
        elif opcion == "4" :
            trazabilidad(conexion)
        elif opcion == "5" :
            trazabilidadlog(conexion)       

        elif opcion == "8":
            print("Saliendo de la app.")
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")

if __name__ == "__main__":
    menu_principal()
