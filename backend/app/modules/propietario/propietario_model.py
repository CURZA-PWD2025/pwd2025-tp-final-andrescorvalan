from ...database.accesoBD import OperarBD
from ...database.erroresBD import DBErrorData, DBException

class ModelException(Exception):
    # Errores ya procesados por el Model.
    # Se pueden enviar al frontend.
    pass

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Propietario.
#------------------------------------------------------------------------------------------------------------------------

class PropietarioModel:
    PREFIX = "Base de Datos (Propietario): "
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, nombre: str="", apellido: str="", dni: str="", telefono: str="", email: str=""):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.email = email
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "apellido" : self.apellido,
            "dni" : self.dni,
            "telefono" : self.telefono,
            "email" : self.email
        }
    @staticmethod
    def deserializar(data: dict) -> 'PropietarioModel':
        return PropietarioModel(
            id = data.get('id', 0),
            nombre = data.get('nombre', ""),
            apellido = data.get('apellido', ""),
            dni = data.get('dni', ""),
            telefono = data.get('telefono', ""),
            email = data.get('email', "")
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos los Propietarios.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            return OperarBD.obtenerReg(
                "SELECT id, nombre, apellido, dni, telefono, email "
                "FROM PROPIETARIOS"
            )
        except DBException:
            print(f"DEBUG - {PropietarioModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de propiedades. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Propietario por Id.
    # Retorna:  - Un diccionario con los datos si encontró el propietario.
    #           - {} si no encontró el propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, nombre, apellido, dni, telefono, email "
                "FROM PROPIETARIOS "
                "WHERE id=%s",
                (id,)
            )
            if registros:
                return registros[0]
            return {}
        except DBException:
            print(f"DEBUG - {PropietarioModel.PREFIX} (get_one):")
            raise ModelException(
                "No se pudo obtener el propietario. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )    #--------------------------------------------------------------------------------------------------------
    # Método para crear un Propietario.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool:
        try:
            result = OperarBD.modifBD(
                "INSERT "
                "INTO PROPIETARIOS (nombre, apellido, dni, telefono, email) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.nombre, self.apellido, self.dni, self.telefono, self.email)
            )
            if result > 0:
                self.id = result    # Se actualiza el atributo id (el nuevo id asignado).
                return True
            return False
        except DBErrorData as e:
            raise ValueError(f"No se pudo crear el propietario. {e}")
        except DBException:
            print(f"DEBUG - {PropietarioModel.PREFIX} (create):")
            raise ModelException('No se pudo crear el propietario en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar un Propietario.
    # Retorna: - True si se modificó correctamente.
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool:
        try:
            result =  OperarBD.modifBD(
                "UPDATE PROPIETARIOS "
                "SET nombre=%s, apellido=%s, dni=%s, telefono=%s, email=%s "
                "WHERE id=%s",
                (self.nombre, self.apellido, self.dni, self.telefono, self.email, self.id)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo actualizar el propietario. {e}")
        except DBException:
            print(f"DEBUG - {PropietarioModel.PREFIX} (update):")
            raise ModelException('No se pudo actualizar el propietario en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar un Propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool:
        try:
            result = OperarBD.modifBD(
                "DELETE FROM PROPIETARIOS WHERE id=%s", (id,)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo eliminar el propietario. {e}")
        except DBException:
            print(f"DEBUG - {PropietarioModel.PREFIX} (delete):")
            raise ModelException('No se pudo eliminar el propietario en la base de datos.')