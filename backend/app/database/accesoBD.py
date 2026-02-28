import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

#------------------------------------------------------------------------------------------------------------------------
# Clase para realizar operaciones sobre la BD que sean unicas (select, insert, update, delete)
# autocommit=True
#------------------------------------------------------------------------------------------------------------------------
class OperarBD:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una conexión a la bd, con autocommit=True
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_connect():
        try:
            conn = mysql.connector.connect(
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                database = os.getenv('DB_NAME'),
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                autocommit = True,            
            )
            return conn
        except mysql.connector.Error as una_excepccion:
            print(f'Base de Datos: Ocurrió una excepción al intentar conectarse: {una_excepccion}')
            raise

    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener resgistros, se debe usar con SELECT en el parametro sql
    # Retorna: - Un conjunto de registros.
    #          - None si hubo alguna excepción de la BD.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def obtenerReg(sql: str, params: tuple=()) -> list[dict] | None:
        conexion = None
        try:
            conexion = OperarBD.get_connect()
            with conexion.cursor(dictionary=True) as un_cursor:
                un_cursor.execute(sql,params)
                return un_cursor.fetchall()
        except mysql.connector.Error as una_excepccion:
            print(f'Base de Datos: Ocurrió una excepción al intentar obtener datos {una_excepccion}')
            return None
        finally:
            if conexion and conexion.is_connected():
                conexion.close()

    #--------------------------------------------------------------------------------------------------------
    # Método estático para modificar resgistros, se debe usar con INSERT, UPDATE o DELETE en el parametro sql
    # Retorna: 
    # - None si se detecto una excepción.
    # - Un entero:
    #      a) si es un INSERT con PK autoincrement, devuelve el nuevo Id.
    #      b) sino devuelve el numero de filas afectadas (puede ser 0).
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def modifBD(sql: str, params: tuple=()) -> int | None:
        conexion = None
        try:
            conexion = OperarBD.get_connect()
            with conexion.cursor(dictionary=True) as un_cursor:
                un_cursor.execute(sql, params)
                if sql.strip().upper().startswith("INSERT") and un_cursor.lastrowid:
                    # Para un INSERT en una tabla con clave primaria autoincrement.
                    # Devuelve el ID generado
                    return un_cursor.lastrowid
                
                # Para un INSERT en una tabla con clave primaria NO autoincrement, o un UPDATE o DELETE, 
                # devuelve el número de filas afectadas (puede ser 0 si no hubo cambios (UPDATE) o no se 
                # encontró el registro (UPDATE/DELETE))
                return un_cursor.rowcount 
        except mysql.connector.Error as una_excepccion:
            print(f'Base de Datos: Ocurrió una excepción al intentar manipular datos: {una_excepccion}')
            return None
        finally:
            if conexion and conexion.is_connected():
                conexion.close()

#------------------------------------------------------------------------------------------------------------------------
# Clase para realizar operaciones sobre la BD que NO sean unicas, sino varias en una transaccion (autocommit=False)
#------------------------------------------------------------------------------------------------------------------------
class TransaccionBD:
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.nuevo_id = 0 # Almacena el último ID generado (si se insertó en una tabla con PK autoincrement)

    def get_nuevo_id(self):
        return self.nuevo_id
    
    #--------------------------------------------------------------------------------------------------------
    # Método para inicializar una transacción y su conexión
    #--------------------------------------------------------------------------------------------------------
    def iniciar_transaccion(self):
        if self.conexion and self.conexion.is_connected():  # Por si quedo una transaccion activa
            self.finalizar_transaccion() 
        try:
            self.conexion = mysql.connector.connect(
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                database = os.getenv('DB_NAME'),
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                autocommit = False
            )
            self.cursor = self.conexion.cursor(dictionary=True)
            self.nuevo_id = 0
        except mysql.connector.Error as una_excepccion:
            raise RuntimeError(f'Base de Datos: Ocurrió una excepción al intentar iniciar una transacción: {una_excepccion}') 
    #--------------------------------------------------------------------------------------------------------
    # Metodo para hacer un commit
    #--------------------------------------------------------------------------------------------------------          
    def confirmar_transaccion(self):
        if not (self.conexion and self.conexion.is_connected()):
            print("Base de Datos: No hay una transacción activa para realizar commit.")
            return None
        try:
            self.conexion.commit()
            return True
        except mysql.connector.Error as una_excepcion:
            print(f"Base de Datos: Excepción al hacer commit: {una_excepcion}")
            return None

    #--------------------------------------------------------------------------------------------------------
    # Metodo para hacer un rollback
    #--------------------------------------------------------------------------------------------------------
    def revertir_transaccion(self):
        if not (self.conexion and self.conexion.is_connected()):
            print("Base de Datos: No hay una transacción activa para realizar rollback.")
            return None
        try:
            self.conexion.rollback()
            return True
        except mysql.connector.Error as una_excepcion:
            print(f"Base de Datos: Excepción al hacer rollback: {una_excepcion}")
            return None
        
    #--------------------------------------------------------------------------------------------------------
    # Metodo para finalizar la transaccion, liberando los recursos
    #--------------------------------------------------------------------------------------------------------
    def finalizar_transaccion(self):
        if self.cursor:
            try:
                self.cursor.close()
            except mysql.connector.Error as una_excepccion:
                print(f"Base de Datos: Excepción al cerrar el cursor: {una_excepccion}")
            finally:
                self.cursor = None
        if self.conexion:
            try:
                if self.conexion.is_connected():
                    self.conexion.close() 
            except mysql.connector.Error as una_excepccion:
                print(f"Base de Datos: Excepción al cerrar la conexión: {una_excepccion}")
            finally: 
                self.conexion = None
    
    #--------------------------------------------------------------------------------------------------------
    # Metodo para obtener datos de la BD (SELECT)
    #--------------------------------------------------------------------------------------------------------
    def obtenerReg(self, sql: str, params: tuple=()) -> list[dict] | None:
        if not (self.conexion and self.conexion.is_connected()):
            print("Base de Datos: No hay una transacción activa para obtener registros.")
            return None
           
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as una_excepccion:
            print(f'Base de Datos: Excepción al intentar obtener datos {una_excepccion}')
            return None

    #--------------------------------------------------------------------------------------------------------
    # Metodo para modificar datos de la BD (INSERT,UPDATE,DELETE)
    # Retorna: 
    # - None si se detecto una excepcion
    # - Un entero si una operacion INSERT, UPDATE o DELETE:
    #      a) si es un INSERT con PK autoincrement, devuelve el nuevo Id.
    #      b) sino el numero de filas afectadas (puede ser 0)
    #--------------------------------------------------------------------------------------------------------
    def operacionBD(self, sql: str, params: tuple=()) -> int | None:
        if not (self.conexion and self.conexion.is_connected()):
            print("Base de Datos: No hay una transacción activa para poder manipular datos.")
            return None
        try:
            self.cursor.execute(sql, params)
            if sql.strip().upper().startswith("INSERT") and self.cursor.lastrowid:
                # Para INSERT de una tabla con clave primaria autoincrement.
                # Devuelve el ID generado
                self.nuevo_id = self.cursor.lastrowid
                return self.cursor.lastrowid
        
            # Para INSERT de una tabla con clave primaria NO autoincrement.
            # Para UPDATE y DELETE, devolve el número de filas afectadas
            # Puede ser 0 si no hubo cambios (UPDATE) o no se encontró el registro (DELETE)
            return self.cursor.rowcount 
        except mysql.connector.Error as una_excepccion:
            print(f'Base de Datos: Excepción al intentar manipular datos: {una_excepccion}')
            return None