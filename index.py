import os
import mysql.connector
from dotenv import load_dotenv

# Cargar las credenciales del archivo .env oculto
load_dotenv()

config_bd = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': 3306
}

def conectar_bd():
    """Conectar a la base de datos MySQL en la nube"""
    return mysql.connector.connect(**config_bd)

def listar_clientes():
    """Muestra todos los clientes registrados"""
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT id_cliente, dni, nombre, apellido, telefono FROM cliente ORDER BY apellido")
    clientes = cursor.fetchall()
    
    print("\n--- LISTA DE CLIENTES ---")
    print("ID   DNI             Nombre y Apellido              Teléfono")
    print("-" * 60)
    for c in clientes:
        print(f"{c[0]:<4} {c[1]:<15} {c[2]} {c[3]:<20} {c[4]}")
        
    cursor.close()
    conexion.close()

def agregar_cliente():
    """Agrega un nuevo cliente a la base de datos"""
    print("\n--- NUEVO CLIENTE ---")
    dni = input("DNI: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    telefono = input("Teléfono: ")
    
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    sql = "INSERT INTO cliente (dni, nombre, apellido, telefono) VALUES (%s, %s, %s, %s)"
    valores = (dni, nombre, apellido, telefono)
    
    cursor.execute(sql, valores)
    conexion.commit()
    
    print("Cliente agregado exitosamente.")
    
    cursor.close()
    conexion.close()

def actualizar_cliente():
    """Actualiza los datos de un cliente existente"""
    listar_clientes()
    print("\n--- ACTUALIZAR CLIENTE ---")
    id_cliente = input("Ingrese el ID del cliente a actualizar: ")
    
    nombre = input("Nuevo nombre: ")
    apellido = input("Nuevo apellido: ")
    telefono = input("Nuevo teléfono: ")
    
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    sql = "UPDATE cliente SET nombre = %s, apellido = %s, telefono = %s WHERE id_cliente = %s"
    valores = (nombre, apellido, telefono, id_cliente)
    
    cursor.execute(sql, valores)
    conexion.commit()
    
    if cursor.rowcount > 0:
        print("Cliente actualizado correctamente.")
    else:
        print("No se encontró un cliente con ese ID.")
        
    cursor.close()
    conexion.close()

def eliminar_cliente():
    """Elimina un cliente de la base de datos"""
    listar_clientes()
    print("\n--- ELIMINAR CLIENTE ---")
    id_cliente = input("Ingrese el ID del cliente a eliminar: ")
    
    confirmar = input("¿Está seguro de eliminar este cliente? (s/n): ")
    if confirmar.lower() == 's':
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        conexion.commit()
        
        if cursor.rowcount > 0:
            print("Cliente eliminado correctamente.")
        else:
            print("No se encontró un cliente con ese ID.")
            
        cursor.close()
        conexion.close()
    else:
        print("Operación cancelada.")

# MENÚ PRINCIPAL


def main():
    print("💪 SISTEMA DE GESTIÓN DE GIMNASIO (Nube)")
    
    # Probar conexión inicial
    try:
        prueba = conectar_bd()
        print("Conexión exitosa a Clever Cloud.")
        prueba.close()
    except Exception as e:
        print(f"Error al conectar: {e}")
        return

    while True:
        print("\n" + "="*40)
        print("          MENÚ PRINCIPAL")
        print("="*40)
        print("1. Ver clientes")
        print("2. Agregar cliente")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. Salir")
        print("="*40)
        
        opcion = input("Seleccione una opción (1-5): ")
        
        if opcion == "1":
            listar_clientes()
        elif opcion == "2":
            agregar_cliente()
        elif opcion == "3":
            actualizar_cliente()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
            
        input("\nPresione Enter para continuar")

if __name__ == "__main__":
    main()
