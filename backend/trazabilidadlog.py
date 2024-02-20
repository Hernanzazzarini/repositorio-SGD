import mysql.connector
from mysql.connector import Error
from conexion import create_db_connection, close_db_connection
from tabulate import tabulate


def validar_campo(valor, nombre_campo):
    while not valor:
        valor = input(f"¡Campo {nombre_campo} obligatorio! Ingrese el valor: ")
    return valor

def crear_transporte(conexion):
    nombre_transporte = validar_campo(input("Ingrese el nombre del transporte: "), "Nombre del Transporte")
    telefono_transporte = validar_campo(input("Ingrese el teléfono del transporte: "), "Teléfono del Transporte")
    email_transporte = validar_campo(input("Ingrese el correo electrónico del transporte: "), "Correo Electrónico del Transporte")
    localidad_transporte = validar_campo(input("Ingrese la localidad del transporte: "), "Localidad del Transporte")
    nombre_chofer = validar_campo(input("Ingrese el nombre del chofer: "), "Nombre del Chofer")
    codigo_postal = validar_campo(input("Ingrese el código postal: "), "Código Postal")

    try:
        with conexion.cursor() as cursor:
            query = "INSERT INTO transportes (nombre_transporte, telefono_transporte, email_transporte, localidad_transporte, nombre_chofer, codigo_postal) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (nombre_transporte, telefono_transporte, email_transporte, localidad_transporte, nombre_chofer, codigo_postal)
            cursor.execute(query, valores)
            conexion.commit()
            return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error al crear el transporte: {e}")
        return None

def listar_transportes(conexion):
    try:
        with conexion.cursor() as cursor:
            query = "SELECT * FROM transportes"
            cursor.execute(query)
            transportes = cursor.fetchall()

            if not transportes:
                print("No hay transportes registrados.")
            else:
                headers = ["ID", "Nombre", "Teléfono", "Correo Electrónico", "Localidad", "Chofer", "Código Postal"]
                print(tabulate(transportes, headers=headers, tablefmt="pretty"))

    except mysql.connector.Error as e:
        print(f"Error al listar transportes: {e}")    

def validar_campo(valor, nombre_campo):
    while not valor:
        valor = input(f"¡Campo {nombre_campo} obligatorio! Ingrese el valor: ")
    return valor

# Función para crear una nueva carga
def crear_carga(conexion):
    lote = input("Ingrese el lote: ")

    # Validar si el lote ha sido producido (puedes personalizar esta lógica según tu necesidad)
    if not lote_fue_producido(conexion, lote):
        print(f"Error: El lote {lote} no ha sido producido. No se puede crear la carga.")
        return None

    fecha_carga = input("Ingrese la fecha de carga (YYYY-MM-DD): ")
    cantidad = int(input("Ingrese la cantidad: "))
    kilos_transporte = float(input("Ingrese los kilos de transporte: "))
    destino = input("Ingrese el destino: ")
    id_transporte = int(input("Ingrese el ID del transporte: "))

    try:
        with conexion.cursor() as cursor:
            # Verificar si hay suficiente cantidad en stock
            query_stock = "SELECT cantidad FROM stock WHERE numero_lote = %s"
            cursor.execute(query_stock, (lote,))
            stock_actual = cursor.fetchone()

            if stock_actual and stock_actual[0] >= cantidad:
                # Insertar la nueva carga en la tabla de cargas
                query_carga = "INSERT INTO cargas (lote, fecha_carga, cantidad, kilos_transporte, destino, id_transporte) VALUES (%s, %s, %s, %s, %s, %s)"
                valores_carga = (lote, fecha_carga, cantidad, kilos_transporte, destino, id_transporte)
                cursor.execute(query_carga, valores_carga)
                conexion.commit()

                # Actualizar la tabla de stock restando la cantidad
                query_update_stock = "UPDATE stock SET cantidad = cantidad - %s WHERE numero_lote = %s"
                valores_update_stock = (cantidad, lote)
                cursor.execute(query_update_stock, valores_update_stock)
                conexion.commit()

                print("Carga y actualización de stock realizadas con éxito.")
                return cursor.lastrowid
            else:
                print("Error: No hay suficiente cantidad en stock.")
                return None

    except mysql.connector.Error as e:
        print(f"Error al crear la carga: {e}")
        return None

# Función para verificar si un lote ha sido producido
def lote_fue_producido(conexion, lote):
    try:
        with conexion.cursor() as cursor:
            query = "SELECT * FROM produccion WHERE lote = %s"
            cursor.execute(query, (lote,))
            produccion = cursor.fetchone()

            return produccion is not None
    except mysql.connector.Error as e:
        print(f"Error al verificar si el lote fue producido: {e}")
        return False

# Función para listar cargas con información del transporte y chofer y buscar por número de lote
def listar_cargas(conexion):
    try:
        with conexion.cursor() as cursor:
            lote_a_buscar = input("Ingrese el número de lote para buscar (deje en blanco para listar todas las cargas): ")
            
            # Construir la consulta SQL
            query = """
                SELECT cargas.id_carga, cargas.lote, cargas.fecha_carga, cargas.cantidad,
                       cargas.kilos_transporte, cargas.destino, cargas.id_transporte, 
                       transportes.nombre_transporte, transportes.nombre_chofer
                FROM cargas
                INNER JOIN transportes ON cargas.id_transporte = transportes.id_transporte
            """
            
            # Añadir la condición de búsqueda por número de lote si se proporciona
            if lote_a_buscar:
                query += " WHERE cargas.lote = %s"
                cursor.execute(query, (lote_a_buscar,))
            else:
                cursor.execute(query)

            cargas = cursor.fetchall()

            if not cargas:
                print("No se encontraron cargas para el número de lote proporcionado." if lote_a_buscar else "No hay cargas registradas.")
            else:
                headers = ["ID", "Lote", "Fecha de Carga", "Cantidad", "Kilos de Transporte", "Destino", "ID del Transporte", "Nombre del Transporte", "Nombre del Chofer"]
                print(tabulate([(carga[0], carga[1], carga[2], carga[3], carga[4], carga[5], carga[6], carga[7], carga[8]) for carga in cargas], headers=headers, tablefmt="pretty"))

                # Calcular y mostrar los kilos totales de transporte cargados
                kilos_totales = sum(carga[4] for carga in cargas)
                print(f"\nKilos totales de transporte cargados: {kilos_totales:.2f}")

    except mysql.connector.Error as e:
        print(f"Error al listar cargas: {e}")

def crear_stock_fisico(conexion):
    id_calibre = int(validar_campo(input("Ingrese el ID del calibre: "), "ID del Calibre"))
    numero_lote = validar_campo(input("Ingrese el número de lote: "), "Número de Lote")
    cantidad = int(validar_campo(input("Ingrese la cantidad: "), "Cantidad"))
    kilos = float(validar_campo(input("Ingrese los kilos: "), "Kilos"))

    try:
        with conexion.cursor() as cursor:
            query = "INSERT INTO stock (id_calibre, numero_lote, cantidad, kilos) VALUES (%s, %s, %s, %s)"
            valores = (id_calibre, numero_lote, cantidad, kilos)
            cursor.execute(query, valores)
            conexion.commit()
            print("Carga de stock físico realizada con éxito.")
            return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error al crear la carga de stock físico: {e}")
        return None



def trazabilidadlog(conexion):
    while True:
        print("\n*** Menú Principal ***")
        print("1. Crear Transporte")
        print("2. Crear cargas")
        print("3. crear stock fisico")
        print("-------------------------")
        print("*** Menú de Listados ***")
        print("4. Listar transportes")
        print("5. Listar cargas")
        print("6. Listar trazabilidad") 
        print("7. Listar stock") 
        print("-------------------------")
        print("8. Salir")

        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            transporte_creado = crear_transporte(conexion)
            if transporte_creado is not None:
                print("transporte creado")
            else:
                print("Error al crear el transporte Por favor, inténtalo de nuevo.")

        elif opcion == "2":
            crear_carga(conexion)   

        elif opcion == "3":
           crear_stock_fisico(conexion)     
        elif opcion == "4":
            listar_transportes(conexion) 
        elif opcion == "5":
            listar_cargas(conexion)
        elif opcion == "8":
            break  
        


if __name__ == "__main__":
    conexion = create_db_connection()

    try:
        if conexion:
            trazabilidadlog(conexion)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conexion:
            close_db_connection(conexion)