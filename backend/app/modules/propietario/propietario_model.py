from ...database.accesoBD import OperarBD

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Propietario.
#------------------------------------------------------------------------------------------------------------------------

class PropietarioModel:
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
    def get_all() -> list[dict] | None:
        return OperarBD.obtenerReg(
           "SELECT * "
           "FROM PROPIETARIOS"
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Propietario por Id.
    # Retorna:  - un diccionario con los datos si encontró el propietario.
    #           - {} si no encontró el propietario.
    #           - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        registros = OperarBD.obtenerReg(
            "SELECT * "
            "FROM PROPIETARIOS "
            "WHERE id=%s",
            (id,)
        )
        if registros is None:
            return None
        if registros:
            return registros[0]
        else:
            return {}
    #--------------------------------------------------------------------------------------------------------
    # Método para crear un Propietario.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #          - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool | None:
        result = OperarBD.modifBD(
            "INSERT "
            "INTO PROPIETARIOS (nombre, apellido, dni, telefono, email) "
            "VALUES (%s, %s, %s, %s, %s)",
            (self.nombre, self.apellido, self.dni, self.telefono, self.email)
        )
        if result == None:
            return None         # Alguna excepción.
        if result > 0:
            self.id = result    # Se actualiza el atributo id (el nuevo id asignado).
            return True         # Se insertó correctamente.
        else:
            return False        # No se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar un Propietario.
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios).
    #          - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool | None:
        result = OperarBD.modifBD(
            "UPDATE PROPIETARIOS "
            "SET nombre=%s, apellido=%s, dni=%s, telefono=%s, email=%s WHERE id=%s",
            (self.nombre, self.apellido, self.dni, self.telefono, self.email, self.id)
        )
        if result == None:
            return None     # Alguna excepción.
        return result == 1  # True si se actualizó correctamente, False si no se cambio la BD.
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar un Propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool | None:
        result = OperarBD.modifBD(
            "DELETE "
            "FROM PROPIETARIOS "
            "WHERE id=%s",
            (id,))
        if result == None:
            return None     # Alguna excepción.
        return result == 1  # True si se elimino, sino False.