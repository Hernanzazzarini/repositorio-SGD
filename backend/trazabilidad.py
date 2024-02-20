import mysql.connector
from mysql.connector import Error
from conexion import create_db_connection, close_db_connection
from tabulate import tabulate
import datetime


def obtener_calibre():
    while True:
        nombre_calibre = input("Nombre del nuevo calibre: ")
        if nombre_calibre:
            return nombre_calibre
        else:
            print("El nombre del calibre es obligatorio. Ingresa calibre.")

def crear_calibre(conexion):
    nombre_calibre = obtener_calibre()
    
    try:
        with conexion.cursor() as cursor:
            query = "INSERT INTO calibres (nombre_calibre) VALUES (%s)"
            # Añade una coma para crear una tupla
            cursor.execute(query, (nombre_calibre,))
            conexion.commit()
            return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error al crear el calibre: {e}")
        return None
    
def listar_calibres(conexion):
    try:
        with conexion.cursor() as cursor:
            query = "SELECT * FROM calibres"
            cursor.execute(query)
            calibres = cursor.fetchall()
            if calibres:
                print("Lista de Calibres:")
                for calibre in calibres:
                    print(f"ID: {calibre[0]}, calibre: {calibre[1]}")
            else:
                print("No hay calibres registrados.")
    except mysql.connector.Error as e:
        print(f"Error al listar calibres: {e}")

#--------------------------------------------------------

def obtener_segregacion():
    while True:
        nombre_segregacion = input("Nombre segregacion: ")
        if nombre_segregacion:
            return nombre_segregacion
        else:
            print("El nombre de la segregacion es obligatoria. Ingresa segregacion.")

def crear_segregacion(conexion):
    tipo_segregacion = obtener_segregacion()
    descripcion_segregacion = input("Descripción de la segregación: ")
    
    try:
        with conexion.cursor() as cursor:
            query = "INSERT INTO segregacion (tipo_segregacion, descripcion_segregacion) VALUES (%s, %s)"
            cursor.execute(query, (tipo_segregacion, descripcion_segregacion))
            conexion.commit()
            return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error al crear segregacion: {e}")
        return None
    
def listar_segregacion(conexion):
    try:
        with conexion.cursor() as cursor:
            query = "SELECT * FROM segregacion"
            cursor.execute(query)
            segregaciones = cursor.fetchall()

            if segregaciones:
                headers = ["ID", "Tipo", "Descripción"]
                table_data = [[s[0], s[1], s[2]] for s in segregaciones]

                print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
            else:
                print("No hay segregaciones registradas.")
    except mysql.connector.Error as e:
        print(f"Error al listar segregaciones: {e}")

#--------------------------------------------------------

#--------------------------------------------------------        
def crear_produccion(conexion):
    # Capturar datos de producción
    id_calibre = int(input("Ingrese el ID del calibre: "))
    id_segregacion = int(input("Ingrese el ID de la segregación: "))
    lote = input("Ingrese el lote: ")
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    hora_inicio = input("Ingrese la hora de inicio (HH:MM:SS): ")
    fecha_final = input("Ingrese la fecha final (YYYY-MM-DD): ")
    hora_final = input("Ingrese la hora final (HH:MM:SS): ")
    envases = input("envases N/U: ")
    kilos = float(input("Ingrese la cantidad de kilos: "))
    deposito = input("Ingrese el depósito: ")
    rack = input("Ingrese el rack: ")
    stock = int(input("Ingrese el stock: "))
    reclamo = input("Ingrese el reclamo: ")

    # Crear el comando SQL para insertar datos de producción
    sql = """INSERT INTO produccion (
                id_calibre, id_segregacion, lote, fecha_inicio, hora_inicio,
                fecha_final, hora_final, envases, kilos, deposito, rack, stock, reclamo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    # Obtener la fecha y hora actuales
    now = datetime.datetime.now()
    fecha_actual = now.strftime("%Y-%m-%d")
    hora_actual = now.strftime("%H:%M:%S")

    # Ejecutar la consulta SQL
    with conexion.cursor() as cursor:
        cursor.execute(sql, (
            id_calibre, id_segregacion, lote, fecha_inicio, hora_inicio,
            fecha_final, hora_final, envases, kilos, deposito, rack, stock, reclamo
        ))
        conexion.commit()

    print("\nProducción creada con éxito.")
    print(f"Fecha y hora de creación: {fecha_actual} {hora_actual}")

def listar_produccion(conexion):
    cursor = None
    try:
        cursor = conexion.cursor()
        query = "SELECT * FROM produccion"
        cursor.execute(query)
        produccion = cursor.fetchall()

        if not produccion:
            print("No hay registros de producción.")
        else:
            print("\n*** Listado de Producción ***")
            for p in produccion:
                print("\nID Registro:     ", p[0])
                print("ID Calibre:      ", p[1])
                print("ID Segregación:  ", p[2])
                print("Lote:            ", p[3])
                print("Fecha Inicio:    ", f"{p[4]} {p[5]}")
                print("Fecha Final:     ", f"{p[6]} {p[7]}")
                print("Envases:         ", p[8])
                print("Kilos:           ", p[9])
                print("Depósito:        ", p[10])
                print("Rack:            ", p[11])
                print("Stock:           ", p[12])
                print("Reclamo:         ", p[13])
                print("-------------------------")
    except Exception as e:
        print(f"Error al listar producción: {e}")
    finally:
        if cursor:
            cursor.close()
#--------------------------------------------------------              
def trazabilidad(conexion):
    while True:
        print("\n*** Menú Principal ***")
        print("1. Crear Calibre")
        print("2. Crear Segregación")
        print("3. Crear Producción")
        print("-------------------------")
        print("*** Menú de Listados ***")
        print("4. Listar Calibres")
        print("5. Listar Segregaciones")
        print("6. Listar Datos Productivos") 
        print("-------------------------")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            calibre_creado = crear_calibre(conexion)
            if calibre_creado is not None:
                print("calibre creado")
            else:
                print("Error al crear el calibre Por favor, inténtalo de nuevo.")

        elif opcion == "2":
            segregacion_creada = crear_segregacion(conexion)
            if segregacion_creada is not None:
                print("segregacion creada")
            else:
                print("Error al crear la segregacion Por favor, inténtalo de nuevo.")

    
        elif opcion == "3" :
            crear_produccion(conexion) 
        
        elif opcion == "4":
           listar_calibres(conexion)

        elif opcion == "5":
           listar_segregacion(conexion)  
        
        elif opcion == "6" :
            listar_produccion(conexion)
        
        elif opcion == "7":
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

















if __name__ == "__main__":
    conexion = create_db_connection()

    try:
        if conexion:
            trazabilidad(conexion)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conexion:
            close_db_connection(conexion)
