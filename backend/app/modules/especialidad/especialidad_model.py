from ...database.accesoBD import OperarBD

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Especialidad.
#------------------------------------------------------------------------------------------------------------------------

class EspecialidadModel:
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, nombre: str="", descripcion: str=""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "descripcion" : self.descripcion
        }
    @staticmethod
    def deserializar(data: dict) -> 'EspecialidadModel':
        return EspecialidadModel(
            id = data.get('id', 0),
            nombre = data.get('nombre', ""),
            descripcion = data.get('descripcion', "")
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos las Especialidades.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict] | None:
       return OperarBD.obtenerReg(
           "SELECT * "
           "FROM ESPECIALIDADES"
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Especialidad por Id.
    # Retorna:  - un diccionario con los datos si encontró la especialidad.
    #           - {} si no encontró la especialidad.
    #           - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        registros = OperarBD.obtenerReg(
            "SELECT * "
            "FROM ESPECIALIDADES "
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
    # Método para crear una Especialidad.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #          - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool | None:
        result = OperarBD.modifBD(
            "INSERT INTO ESPECIALIDADES (nombre, descripcion) "
            "VALUES (%s, %s)",
            (self.nombre, self.descripcion)
        )
        if result == None:
            return None         # Alguna excepción.
        if result > 0:
            self.id = result    # Se actualiza el atributo id (el nuevo id asignado).
            return True         # Se insertó correctamente.
        else:
            return False        # No se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar una Especialidad.
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios).
    #          - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool | None:        
        result = OperarBD.modifBD(
            "UPDATE ESPECIALIDADES "
            "SET nombre=%s, descripcion=%s "
            "WHERE id=%s",
            (self.nombre, self.descripcion, self.id,)
        )
        if result == None:
            return None     # Alguna excepción.
        return result == 1  # True si Se actualizó correctamente, False si no se cambio la BD.
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar una Especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool | None:
        result = OperarBD.modifBD(
            "DELETE "
            "FROM ESPECIALIDADES "
            "WHERE id=%s",
            (id,)
        )
        if result == None:
            return None     # Alguna excepción.
        return result == 1  # True si se elimino, sino False.