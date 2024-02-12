import mysql.connector
from mysql.connector import Error
from conexion import create_db_connection, close_db_connection
from tabulate import tabulate

def usuario_existe(conexion, id_usuario):
    try:
        cursor = conexion.cursor()
        query = "SELECT id_usuario FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as e:
        print(f"Error al verificar la existencia del usuario: {e}")
        return False
    finally:
        if cursor:
            cursor.close()

def obtener_nombre_tarea():
    while True:
        nombre_tarea = input("Nombre de la nueva tarea: ")
        if nombre_tarea:
            return nombre_tarea
        else:
            print("El nombre de tarea es obligatorio. Ingresa un nombre válido.")

def obtener_fecha_vencimiento():
    while True:
        fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
        if fecha_vencimiento:
            return fecha_vencimiento
        else:
            print("La fecha de vencimiento es obligatoria. Ingresa una fecha válida en formato YYYY-MM-DD.")

def obtener_estado():
    while True:
        estado = input("Estado de la tarea: ")
        if estado:
            return estado
        else:
            print("El estado de la tarea es obligatorio. Ingresa un estado válido.")

def obtener_id_usuario(conexion):
    while True:
        try:
            id_usuario = int(input("ID del usuario asignado a la tarea: "))
            if usuario_existe(conexion, id_usuario):
                return id_usuario
            else:
                print(f"El usuario con ID {id_usuario} no existe. Ingresa un ID de usuario válido.")
        except ValueError:
            print("El ID de usuario debe ser un número entero. Ingresa un ID de usuario válido.")

def crear_tarea(conexion):
    nombre_tarea = obtener_nombre_tarea()
    fecha_vencimiento = obtener_fecha_vencimiento()
    estado = obtener_estado()
    id_usuario = obtener_id_usuario(conexion)

    try:
        cursor = conexion.cursor()
        query = "INSERT INTO tareas (tarea, fecha_vencimiento, estado, id_usuario) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre_tarea, fecha_vencimiento, estado, id_usuario))
        conexion.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error al crear tarea: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def listar_tareas(conexion):
    try:
        cursor = conexion.cursor()
        query = "SELECT t.id_tarea, t.tarea, t.fecha_vencimiento, t.estado, t.id_usuario, u.nombre_usuario FROM tareas t JOIN usuarios u ON t.id_usuario = u.id_usuario"
        cursor.execute(query)
        tareas = cursor.fetchall()

        if not tareas:
            print("No hay tareas registradas.")
        else:
            headers = ["ID", "Tarea", "Fecha Vencimiento", "Estado", "ID Usuario", "Nombre Usuario"]
            print(tabulate(tareas, headers=headers, tablefmt="pretty"))
    except mysql.connector.Error as e:
        print(f"Error al listar tareas: {e}")
    finally:
        if cursor:
            cursor.close()

def listar_tareas_pendientes(conexion):
    try:
        cursor = conexion.cursor()
        query = "SELECT t.id_tarea, t.tarea, t.fecha_vencimiento, t.estado, t.id_usuario, u.nombre_usuario FROM tareas t JOIN usuarios u ON t.id_usuario = u.id_usuario WHERE t.estado = 'pendiente'"
        cursor.execute(query)
        tareas_pendientes = cursor.fetchall()

        if not tareas_pendientes:
            print("No hay tareas pendientes.")
        else:
            headers = ["ID", "Tarea", "Fecha Vencimiento", "Estado", "ID Usuario", "Nombre Usuario"]
            print(tabulate(tareas_pendientes, headers=headers, tablefmt="pretty"))
    except mysql.connector.Error as e:
        print(f"Error al listar tareas pendientes: {e}")
    finally:
        if cursor:
            cursor.close()

def actualizar_estado_tarea(conexion):
    try:
        id_tarea = int(input("Ingrese el ID de la tarea que desea actualizar: "))
        nuevo_estado = input("Ingrese el nuevo estado de la tarea: ")

        cursor = conexion.cursor()
        query = "UPDATE tareas SET estado = %s WHERE id_tarea = %s"
        cursor.execute(query, (nuevo_estado, id_tarea))
        conexion.commit()

        if cursor.rowcount > 0:
            print(f"Estado de la tarea con ID {id_tarea} actualizado correctamente.")
        else:
            print(f"No se encontró una tarea con ID {id_tarea}. Verifique el ID e inténtelo de nuevo.")
    except ValueError:
        print("Por favor, ingrese un ID de tarea válido.")
    except mysql.connector.Error as e:
        print(f"Error al actualizar estado de tarea: {e}")
    finally:
        if cursor:
            cursor.close()                  

def tareas(conexion):
    while True:
        print("\nMenú:")
        print("1. Crear tarea")
        print("2. Listar tareas")
        print("3. Listar tareas Pendientes")
        print("4. Actualizar Estado")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            tarea_creada = crear_tarea(conexion)
            if tarea_creada is not None:
                print("Tarea creada")
            else:
                print("Error al crear la tarea. Por favor, inténtalo de nuevo.")
        elif opcion == "2":
            listar_tareas(conexion)
        elif opcion =="3" :
            listar_tareas_pendientes(conexion) 
        elif opcion == "4":
            actualizar_estado_tarea(conexion)
            
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")


if __name__ == "__main__":
    conexion = create_db_connection()

    try:
        if conexion:
            tareas(conexion)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conexion:
            close_db_connection(conexion)
