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
def obtener_transporte():
    while True:
        nombre_transporte = input("Nombre del transporte: ")
        if nombre_transporte:
            return nombre_transporte
        else:
            print("El nombre del transporte es obligatorio. Ingresa el nombre del transporte.")

def crear_transporte(conexion):
    try:
        nombre_transporte = obtener_transporte()
        telefono_transporte = input("Ingrese el número de teléfono: ")
        email_transporte = input("Ingrese el email: ")
        localidad_transporte = input("Ingrese la localidad: ")
        nombre_chofer = input("Ingrese el nombre del chofer: ")
        codigo_postal = input("Ingrese el código postal: ")

        # Lógica para insertar un nuevo transporte en la base de datos
        cursor = conexion.cursor()
        query = "INSERT INTO transportes (nombre_transporte, telefono_transporte, email_transporte, localidad_transporte, nombre_chofer, codigo_postal) VALUES (%s, %s, %s, %s, %s, %s)"
        datos = (nombre_transporte, telefono_transporte, email_transporte, localidad_transporte, nombre_chofer, codigo_postal)

        cursor.execute(query, datos)
        conexion.commit()

        print("Transporte creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el transporte: {e}")
    finally:
        cursor.close()


def listar_transportes(conexion):
    try:
        cursor = conexion.cursor()
        query = "SELECT * FROM transportes"
        cursor.execute(query)
        transportes = cursor.fetchall()

        if not transportes:
            print("No hay transportes registrados.")
        else:
            headers = ["ID", "Nombre", "Teléfono", "Email", "Localidad", "Chofer", "Código Postal"]
            table_data = [[t[0], t[1], t[2], t[3], t[4], t[5], t[6]] for t in transportes]

            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    except Exception as e:
        print(f"Error al listar transportes: {e}")
    finally:
        cursor.close()
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

def crear_cargas(conexion):
    while True:
        # Captura de datos de carga
        lote = input("Ingrese el nombre del lote: ")
        if lote:
            break
        else:
            print("El nombre del lote es obligatorio. Ingrese un nombre de lote válido.")

    fecha_carga = input("Ingrese la fecha de carga (YYYY-MM-DD): ")
    cantidad = int(input("Ingrese la cantidad: "))
    kilos_transporte = float(input("Ingrese los kilos de transporte: "))
    destino = input("Ingrese el destino: ")
    id_transporte = int(input("Ingrese el ID del transporte: "))

    try:
        with conexion.cursor() as cursor:
            # Consulta SQL para insertar datos de carga
            query_insert_carga = "INSERT INTO cargas (lote, fecha_carga, cantidad, kilos_transporte, destino, id_transporte) VALUES (%s, %s, %s, %s, %s, %s)"
            
            # Ejecutar la consulta SQL con los datos proporcionados
            cursor.execute(query_insert_carga, (lote, fecha_carga, cantidad, kilos_transporte, destino, id_transporte))
            
            # Obtener el ID de la última fila insertada
            id_carga = cursor.lastrowid

            # Actualizar el stock en la tabla produccion
            query_update_stock = "UPDATE produccion SET stock = stock - %s WHERE lote = %s AND stock >= %s"
            cursor.execute(query_update_stock, (cantidad, lote, cantidad))

            # Hacer commit para confirmar los cambios en la base de datos
            conexion.commit()

            print("\nCarga realizada con éxito.")
            
            # Devolver el ID de la última fila insertada
            return id_carga
    except Exception as e:
        print(f"Error al crear carga: {e}")
        return None

#--------------------------------------------------------  
# Función para listar la producción y cargas por número de lote
def listar_datos_productivos_y_cargas(conexion):
    try:
        cursor = conexion.cursor()

        # Input del lote para el que deseas listar los datos
        lote = input("Ingrese el número de lote para listar datos productivos y cargas: ")

        # Consulta SQL para obtener los datos productivos y de carga para el lote específico
        query = """
        SELECT 
            p.id_registro as id_produccion,
            p.id_calibre,
            cal.nombre_calibre,
            p.id_segregacion,
            s.tipo_segregacion,
            p.lote as lote_produccion,
            p.fecha_inicio,
            p.hora_inicio,
            p.fecha_final,
            p.hora_final,
            p.envases,
            p.kilos,
            p.deposito,
            p.rack,
            p.stock,
            p.reclamo,
            c.id_carga,
            c.lote as lote_carga,
            c.fecha_carga,
            c.cantidad,
            c.kilos_transporte,
            c.destino,
            t.id_transporte,
            t.nombre_transporte,
            t.nombre_chofer
        FROM produccion p
        LEFT JOIN produccion_cargas pc ON p.id_registro = pc.id_produccion
        LEFT JOIN cargas c ON pc.id_carga = c.id_carga OR p.lote = c.lote
        LEFT JOIN transportes t ON c.id_transporte = t.id_transporte
        LEFT JOIN calibres cal ON p.id_calibre = cal.id_calibre
        LEFT JOIN segregacion s ON p.id_segregacion = s.id_segregacion
        WHERE p.lote = %s OR c.lote = %s
        """

        cursor.execute(query, (lote, lote))
        resultados = cursor.fetchall()

        if not resultados:
            print(f"No hay registros para el lote {lote}.")
        else:
            print("\n*** Listado de Datos Productivos y Cargas para el Lote {} ***".format(lote))
            for resultado in resultados:
                print("\nID Registro Producción: ", resultado[0])
                print("ID Calibre:             ", resultado[1])
                print("Nombre Calibre:         ", resultado[2])
                print("ID Segregación:         ", resultado[3])
                print("Tipo Segregación:       ", resultado[4])
                print("Lote Producción:        ", resultado[5])
                print("Fecha Inicio:           ", f"{resultado[6]} {resultado[7]}")
                print("Fecha Final:            ", f"{resultado[8]} {resultado[9]}")
                print("Envases:                ", resultado[10])
                print("Kilos:                  ", resultado[11])
                print("Depósito:               ", resultado[12])
                print("Rack:                   ", resultado[13])
                print("Stock:                  ", resultado[14])
                print("Reclamo:                ", resultado[15])
                print("ID Registro Carga:      ", resultado[16])
                print("Lote Carga:             ", resultado[17])
                print("Fecha Carga:            ", resultado[18])
                print("Cantidad:               ", resultado[19])
                print("Kilos de Transporte:    ", resultado[20])
                print("Destino:                ", resultado[21])
                print("ID Transporte:          ", resultado[22])
                print("Nombre Transporte:      ", resultado[23])
                print("Nombre Chofer:          ", resultado[24])
                print("-------------------------")

    except Exception as e:
        print(f"Error al listar datos productivos y cargas: {e}")
    finally:
        if cursor:
            cursor.close()
#-------------------------------------------------------------

def trazabilidad(conexion):
    while True:
        print("\n*** Menú Principal ***")
        print("1. Crear Calibre")
        print("2. Crear Segregación")
        print("3. Crear Transportes")
        print("4. Crear Producción")
        print("5. Crear Cargas")
        print("-------------------------")
        print("*** Menú de Listados ***")
        print("6. Listar Calibres")
        print("7. Listar Segregaciones")
        print("8. Listar Transportes")
        print("9. Listar Datos Productivos") 
        print("10. Listar Cargas")
        #print("11.Lotes en stock")
        #print("12. Kilos en Stock Por Calibre")
        print("-------------------------")
        print("13. Salir")

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
            crear_transporte(conexion)  

        elif opcion == "4" :
            crear_produccion(conexion) 
        elif opcion == "5"  :
            crear_cargas(conexion)    

        elif opcion == "6":
           listar_calibres(conexion)

        elif opcion == "7":
           listar_segregacion(conexion)  
        elif opcion == "8"  :
            listar_transportes(conexion) 
        elif opcion == "9" :
            listar_produccion(conexion)
        elif opcion == "10"   :
            listar_datos_productivos_y_cargas(conexion)

       
        
        elif opcion == "11":
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
