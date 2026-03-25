import mysql.connector
from .erroresBD import DBException,DBErrorData
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
        except mysql.connector.Error as e:
            raise DBException(f'DB: Exception en OperarBD.get_connect. {e}')
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener resgistros, se debe usar con SELECT en el parametro sql
    # Retorna un conjunto de registros
    # Lanza mysql.connector.Error si ocurre una falla en la base de datos
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def obtenerReg(sql: str, params: tuple=()) -> list[dict]:
        conexion = None
        try:
            conexion = OperarBD.get_connect()
            with conexion.cursor(dictionary=True) as un_cursor:
                un_cursor.execute(sql,params)
                return un_cursor.fetchall()
        except mysql.connector.Error as e:
            print(f'DEBUG - MySQL: Exception en OperarBD.obtenerReg. {e}')
            raise DBException(str(e))
        finally:
            if conexion and conexion.is_connected():
                conexion.close()
    #--------------------------------------------------------------------------------------------------------
    # Método estático para modificar registros, se debe usar con INSERT, UPDATE o DELETE en el parametro sql
    # - Lanza mysql.connector.Error si ocurre una falla en la base de datos
    # - Retorna un entero:
    #      a) si es un INSERT con PK autoincrement, devuelve el nuevo Id
    #      b) sino devuelve el numero de filas afectadas (puede ser 0)
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def modifBD(sql: str, params: tuple=()) -> int:
        conexion = None
        try:
            conexion = OperarBD.get_connect()
            with conexion.cursor(dictionary=True) as un_cursor:
                un_cursor.execute(sql, params)
                if sql.strip().upper().startswith("INSERT") and un_cursor.lastrowid:
                    # Para un INSERT en una tabla con clave primaria autoincrement
                    # Devuelve el ID generado
                    return un_cursor.lastrowid
                # Para un INSERT en una tabla con clave primaria NO autoincrement, o un UPDATE o DELETE, 
                # devuelve el número de filas afectadas (puede ser 0 si no hubo cambios (UPDATE) o no se 
                # encontró el registro (UPDATE/DELETE))
                return un_cursor.rowcount 
        except mysql.connector.Error as e:
            print(f'DEBUG - MySQL: Exception en OperarBD.modifBD. {e}')
            if e.errno == 1062:
                msg_original = str(e.msg)
                detalle = msg_original.replace("Duplicate entry", "Dato duplicado").split(" for key")[0]
                raise DBErrorData(f'{detalle}. Ya existe un registro con este dato, que debe ser único.')
            if e.errno == 1451:
                raise DBErrorData("Este registro está siendo usado por otras entidades de la base de datos.")
            if e.errno == 1452:
                raise DBErrorData("Error de referencia: se quiere asociar una entidad que ya no existe en la base de datos.")        
            raise DBException(f'DB: Exception en OperarBD.modifBD(). {e}')
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
        except mysql.connector.Error as e:
            raise DBException(f'DB: Exception en TransaccionBD.iniciar_transaccion. {e}')
    #--------------------------------------------------------------------------------------------------------
    # Metodo para hacer un commit
    #--------------------------------------------------------------------------------------------------------          
    def confirmar_transaccion(self) -> bool:
        if not (self.conexion and self.conexion.is_connected()):
            raise DBException(f'DB: Exception en TransaccionBD.confirmar_transaccion (sin transaccion). {e}')
        try:
            self.conexion.commit()
            return True
        except mysql.connector.Error as e:
            raise DBException(f'DB: Exception en TransaccionBD.confirmar_transaccion (commit). {e}')
    #--------------------------------------------------------------------------------------------------------
    # Metodo para hacer un rollback
    #--------------------------------------------------------------------------------------------------------
    def revertir_transaccion(self) -> bool:
        if not (self.conexion and self.conexion.is_connected()):
            raise DBException(f'DB: Exception en TransaccionBD.revertir_transaccion (sin transaccion). {e}')
        try:
            self.conexion.rollback()
            return True
        except mysql.connector.Error as e:
            raise DBException(f'DB: Exception en TransaccionBD.revertir_transaccion (rollback). {e}')
    #--------------------------------------------------------------------------------------------------------
    # Metodo para finalizar la transaccion, liberando los recursos
    #--------------------------------------------------------------------------------------------------------
    def finalizar_transaccion(self):
        if self.cursor:
            try:
                self.cursor.close()
            except mysql.connector.Error as e:
                raise DBException(f'DB: Exception en TransaccionBD.finalizar_transaccion (cursor.close). {e}')
            finally:
                self.cursor = None
        if self.conexion:
            try:
                if self.conexion.is_connected():
                    self.conexion.close() 
            except mysql.connector.Error as e:
                raise DBException(f'DB: Exception en TransaccionBD.finalizar_transaccion (conexion.close). {e}')
            finally: 
                self.conexion = None
    #--------------------------------------------------------------------------------------------------------
    # Metodo para obtener datos de la BD (SELECT)
    # Retorna un conjunto de registros
    # Lanza mysql.connector.Error si ocurre una falla en la base de datos
    #--------------------------------------------------------------------------------------------------------
    def obtenerReg(self, sql: str, params: tuple=()) -> list[dict]:
        if not (self.conexion and self.conexion.is_connected()):
            raise DBException(f'DB: Exception en TransaccionBD.obtenerReg (sin transaccion). {e}')
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            raise DBException(f'DB: Exception en TransaccionBD.obtenerReg. {e}')
    #--------------------------------------------------------------------------------------------------------
    # Metodo para modificar datos de la BD (INSERT,UPDATE,DELETE) 
    # - Lanza mysql.connector.Error si ocurre una falla en la base de datos
    # - Retorna un entero si una operacion INSERT, UPDATE o DELETE:
    #      a) si es un INSERT con PK autoincrement, devuelve el nuevo Id
    #      b) sino el numero de filas afectadas (puede ser 0)
    #--------------------------------------------------------------------------------------------------------
    def operacionBD(self, sql: str, params: tuple=()) -> int:
        if not (self.conexion and self.conexion.is_connected()):
            raise DBException(f'DB: Exception en TransaccionBD.obtenerReg (sin transaccion).')
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
        except mysql.connector.Error as e:
            if e.errno == 1062:
                msg_original = str(e.msg)
                detalle = msg_original.replace("Duplicate entry", "Dato duplicado").split(" for key")[0]
                raise DBErrorData(f'{detalle}. Ya existe un registro con este dato, que debe ser único.')
            if e.errno == 1451:
                raise DBErrorData("Este registro está siendo usado por otras entidades de la base de datos.")
            if e.errno == 1452:
                raise DBErrorData("Error de referencia: se quiere asociar una entidad que ya no existe en la base de datos.")        
            raise DBException(f'DB: Exception en TransaccionBD.operacionBD(). {e}')