import mysql.connector

from db_init import DB_CONFIG, DB_NAME, TABLES, SEEDS, create_database, create_tables, seeds_tables

def get_connection(with_db=True):
  #Crear una conexion
  config = DB_CONFIG.copy()
  if with_db:
      config['database'] = DB_NAME
  return mysql.connector.connect(**config)

def run_setup():
  conn = None
  try:
    # Borrar si la BD existe
    run_clear() 
    # Crear la base de datos
    conn = get_connection(with_db=False)
    cursor = conn.cursor()
    create_database(cursor)
    conn.close()
    # Crear las tablas
    conn = get_connection(with_db=True)
    cursor = conn.cursor()
    create_tables(TABLES, cursor)
    conn.commit()
    print("Setup completado con éxito.")
  except mysql.connector.Error as err:
      # Errores específicos de MySQL
      raise Exception(f"Error de base de datos durante el setup: {err.msg}")
  except Exception as e:
      # Otros errores
      raise Exception(f"Fallo inesperado en el setup: {str(e)}")
  finally:
      # Cerrar la conexion
      if conn and conn.is_connected():
          conn.close()

def run_seed():
  conn = None
  try:
    run_setup()
    # Intentar conectarse a la base de datos configurada
    config = DB_CONFIG.copy()
    config['database'] = DB_NAME
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    # Si se conecta, cargar datos
    seeds_tables(SEEDS, cursor)
    conn.commit()
  except mysql.connector.Error as err:
    # Cualquier error de MySQL (duplicados, error de sintaxis, etc.)
    raise Exception(f"Error de base de datos al sembrar: {err.msg}")
  except Exception as e:
    # Cualquier otro error
    raise Exception(f"Fallo inesperado en el proceso de seed: {str(e)}")
  finally:
    if conn and conn.is_connected():
        conn.close()

def run_clear():
  conn = None
  try:
    # Conectarse sin especificar la BD
    conn = get_connection(with_db=False)
    cursor = conn.cursor()
    # Borrar la base de datos completa
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    print(f"Base de datos {DB_NAME} eliminada por completo.")
  except mysql.connector.Error as err:
    if err.errno == 1008:
      print(f"La base de datos {DB_NAME} no existía, procediendo...")
    else:
      # Si es otro error (permisos, conexión, etc.), sí lo lanzamos
      raise Exception(f"Error al eliminar la base de datos: {err.msg}")
  finally:
    if conn and conn.is_connected():
        conn.close()