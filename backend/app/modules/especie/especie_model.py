from ...database.accesoBD import OperarBD

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Especie.
#------------------------------------------------------------------------------------------------------------------------

class EspecieModel:
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, nombre: str="", nombre_cientifico: str="", clase: str=""):
        self.id = id
        self.nombre = nombre
        self.nombre_cientifico = nombre_cientifico
        self.clase = clase
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "nombre_cientifico" : self.nombre_cientifico,
            "clase" : self.clase
        }
    @staticmethod
    def deserializar(data: dict) -> 'EspecieModel':
        return EspecieModel(
            id = data.get('id', 0),
            nombre = data.get('nombre', ""),
            nombre_cientifico = data.get('nombre_cientifico', ""),
            clase = data.get('clase', "")
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos las Especies.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict] | None:
       return OperarBD.obtenerReg(
           "SELECT * "
           "FROM ESPECIES")
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Especie por Id.
    # Retorna:  - un diccionario con los datos si encontró la especie.
    #           - {} si no encontró la especie.
    #           - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        registros = OperarBD.obtenerReg(
            "SELECT * "
            "FROM ESPECIES "
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
    # Método para crear una Especie.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #          - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool | None:
        result = OperarBD.modifBD(
            "INSERT "
            "INTO ESPECIES (nombre, nombre_cientifico, clase) "
            "VALUES (%s, %s, %s)",
            (self.nombre, self.nombre_cientifico, self.clase)
        )
        if result == None:
            return None         # Alguna excepción.
        if result > 0:
            self.id = result    # Se actualiza el atributo id (el nuevo id asignado).
            return True         # Se insertó correctamente.
        else:
            return False        # No se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar una Especie.
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios).
    #          - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool | None:        
        result = OperarBD.modifBD(
            "UPDATE ESPECIES "
            "SET nombre=%s, nombre_cientifico=%s, clase=%s "
            "WHERE id=%s",
            (self.nombre, self.nombre_cientifico, self.clase, self.id)
        )
        if result == None:
            return None     # Alguna excepción.
        return result == 1  # True si se actualizó correctamente, False si no se cambio la BD.
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar una Especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool | None:
        result = OperarBD.modifBD(
            "DELETE "
            "FROM ESPECIES "
            "WHERE id=%s",
            (id,)
        )
        if result == None:
            return None     # Alguna excepción.
        return result == 1  # True si se elimino, sino False.