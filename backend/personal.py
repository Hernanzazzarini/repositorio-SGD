import mysql.connector
from mysql.connector import Error
from conexion import create_db_connection, close_db_connection

def crear_personal(conexion, apellido, nombre, email,id_sector):
    try:
        cursor = conexion.cursor()

        # Utilizar parámetros en lugar de concatenación de cadenas
        query = "INSERT INTO personal (apellido, nombre, email, id_sector) VALUES (%s, %s, %s , %s)"
        data = (apellido, nombre, email,id_sector)
        cursor.execute(query, data)

        # Confirmar la transacción
        conexion.commit()

        print("Registro de personal creado exitosamente.")

    except Error as e:
        print(f"Error al crear registro de personal: {e}")

    finally:
        if cursor:
            cursor.close()

def actualizar_personal(conexion, id_legajo, nuevo_apellido, nuevo_nombre, nuevo_email, nuevo_id_sector):
    try:
        cursor = conexion.cursor()

        query = "UPDATE personal SET apellido=%s, nombre=%s, email=%s, id_sector=%s WHERE id_legajo=%s"
        data = (nuevo_apellido, nuevo_nombre, nuevo_email, nuevo_id_sector, id_legajo)
        cursor.execute(query, data)

        conexion.commit()

        print("Registro de personal modificado exitosamente.")

    except Error as e:
        print(f"Error al modificar registro de personal: {e}")

    finally:
        if cursor:
            cursor.close()        

def eliminar_personal(conexion, id_legajo):
    try:
        cursor = conexion.cursor()

        query = "DELETE FROM personal WHERE id_legajo=%s"
        data = (id_legajo,)
        cursor.execute(query, data)

        conexion.commit()

        print("Registro de personal eliminado exitosamente.")

    except Error as e:
        print(f"Error al eliminar registro de personal: {e}")

    finally:
        if cursor:
            cursor.close()    


def listar_personal(conexion):
    try:
        cursor = conexion.cursor()

        query = "SELECT * FROM personal"
        cursor.execute(query)

        personal_records = cursor.fetchall()

        if not personal_records:
            print("No hay registros de personal.")
        else:
            print("\nLista de Personal:")
            print("{:<5} {:<15} {:<15} {:<30} {:<10}".format("ID", "Apellido", "Nombre", "Email", "ID de Sector"))
            print("-" * 75)
            
            for record in personal_records:
                print("{:<5} {:<15} {:<15} {:<30} {:<10}".format(record[0], record[1], record[2], record[3], record[4]))

    except Error as e:
        print(f"Error al listar personal: {e}")

    finally:
        if cursor:
            cursor.close()


def cargar_capacitacion_persona(conexion, id_legajo, id_capacitacion, fecha_tomada):
    try:
        cursor = conexion.cursor()

        query = "INSERT INTO personal_capacitaciones (id_legajo, id_capacitacion, fecha_tomada) VALUES (%s, %s, %s)"
        data = (id_legajo, id_capacitacion, fecha_tomada)
        cursor.execute(query, data)

        conexion.commit()

        print("Capacitación tomada registrada exitosamente.")

    except Error as e:
        print(f"Error al registrar capacitación tomada: {e}")

    finally:
        if cursor:
            cursor.close()           

def listar_capacitaciones_por_id_legajo(conexion, id_legajo):
    try:
        cursor = conexion.cursor()

        query = '''
            SELECT 
                p.apellido, p.nombre, s.sector, c.nombre_capacitacion, DATE_FORMAT(pc.fecha_tomada, '%Y-%m-%d') as fecha_tomada
            FROM 
                personal p
                JOIN personal_capacitaciones pc ON p.id_legajo = pc.id_legajo
                JOIN capacitaciones c ON pc.id_capacitacion = c.id_capacitacion
                JOIN sector s ON p.id_sector = s.id_sector
            WHERE p.id_legajo = %s
        '''

        cursor.execute(query, (id_legajo,))

        capacitaciones_records = cursor.fetchall()

        if not capacitaciones_records:
            print(f"No hay registros de capacitaciones para el ID de legajo {id_legajo}.")
        else:
            print("\nCapacitaciones por Persona:")
            print("{:<15} {:<15} {:<25} {:<30} {:<15}".format("Apellido", "Nombre", "Sector", "Capacitación", "Fecha Tomada"))
            print("-" * 90)

            for record in capacitaciones_records:
                print("{:<15} {:<15} {:<25} {:<30} {:<15}".format(record[0], record[1], record[2], record[3], record[4]))

    except Error as e:
        print(f"Error al listar capacitaciones por persona: {e}")

    finally:
        if cursor:
            cursor.close()
def personal(conexion):
    while True:
        print("\nMenú:")
        print("1. Cargar personal")
        print("2. Modificar personal")
        print("3. Eliminar personal")
        print("4. Listar personal")
        print("5. agregar capacitaciones personal")
        print("6. Listar capacitaciones por id legajo")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            apellido = input("Apellido: ")
            nombre = input("Nombre: ")
            email = input("Email: ")
            id_sector = int(input("ID de sector: "))
            
            crear_personal(conexion, apellido, nombre, email,id_sector)

        elif opcion=="2"  :
             id_legajo = int(input("ID legajo a modificar: "))
             nuevo_apellido = input("Nuevo apellido: ")
             nuevo_nombre = input("Nuevo nombre: ")
             nuevo_email = input("Nuevo email: ")
             nuevo_id_sector = int(input("Nuevo ID de sector: "))
            
             actualizar_personal(conexion, id_legajo, nuevo_apellido, nuevo_nombre, nuevo_email, nuevo_id_sector)
        
        elif opcion=="3" :
             id_legajo = int(input("ID del personal a eliminar: "))
             eliminar_personal(conexion, id_legajo)  

        elif opcion == "4":
             listar_personal(conexion)  

        elif opcion=="5":
            id_legajo = int(input("ID legajo de la persona: "))
            id_capacitacion = int(input("ID de la capacitación: "))
            fecha_tomada = input("Fecha tomada (YYYY-MM-DD): ")

            cargar_capacitacion_persona(conexion, id_legajo, id_capacitacion, fecha_tomada)



        elif opcion == "6":
       # Inicializa id_legajo en None
          id_legajo = None
          # Sigue solicitando hasta que se proporcione una entrada válida
          while id_legajo is None:
             id_legajo_input = input("ID legajo de la persona: ")
              # Verifica si la entrada no está vacía y es un entero válido
             if id_legajo_input.strip() and id_legajo_input.strip().isdigit():
              # Convierte la entrada válida a un entero
                 id_legajo = int(id_legajo_input)
             else:
                print("Por favor, ingrese un ID legajo válido.")
             listar_capacitaciones_por_id_legajo(conexion, id_legajo)
               
       

        elif opcion == "7":
            print("Saliendo del módulo personal")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


    

if __name__ == "__main__":
    conexion = create_db_connection()

    try:
        if conexion:
            personal(conexion)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conexion:
            close_db_connection(conexion)
