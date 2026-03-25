from ...database.accesoBD import OperarBD
from ...database.erroresBD import DBErrorData, DBException

class ModelException(Exception):
    # Errores ya procesados por el Model.
    # Se pueden enviar al frontend.
    pass

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Especie.
#------------------------------------------------------------------------------------------------------------------------

class EspecieModel:
    PREFIX = 'Base de Datos (Especie): '
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, nombre: str="", nombre_cientifico: str="", clase: str="", esperanza_vida: int=0, exotica :int=0):
        self.id = id
        self.nombre = nombre
        self.nombre_cientifico = nombre_cientifico
        self.clase = clase
        self.esperanza_vida = esperanza_vida
        self.exotica = exotica
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "nombre_cientifico" : self.nombre_cientifico,
            "clase" : self.clase,
            "esperanza_vida": self.esperanza_vida,
            "exotica": self.exotica
        }
    @staticmethod
    def deserializar(data: dict) -> 'EspecieModel':
        return EspecieModel(
            id = data.get('id', 0),
            nombre = data.get('nombre', ""),
            nombre_cientifico = data.get('nombre_cientifico', ""),
            clase = data.get('clase', ""),
            esperanza_vida = data.get('esperanza_vida', 0),
            exotica = data.get('exotica', 0)
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos las Especies.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            return OperarBD.obtenerReg(
                "SELECT id, nombre, nombre_cientifico, clase, esperanza_vida, exotica "
                "FROM ESPECIES"
            )
        except DBException:
            print(f"DEBUG - {EspecieModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de especies. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Especie por Id.
    # Retorna:  - un diccionario con los datos si encontró la especie.
    #           - {} si no encontró la especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, nombre, nombre_cientifico, clase, esperanza_vida, exotica "
                "FROM ESPECIES "
                "WHERE id=%s",
                (id,)
            )
            if registros:
                return registros[0]
            return {}
        except DBException:
            print(f"DEBUG - {EspecieModel.PREFIX} (get_one):")
            raise ModelException(
                "No se pudo obtener la especie. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #--------------------------------------------------------------------------------------------------------
    # Método para crear una Especie.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool:
        try:
            result = OperarBD.modifBD(
                "INSERT " 
                "INTO ESPECIES (nombre, nombre_cientifico, clase, esperanza_vida, exotica) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.nombre, self.nombre_cientifico, self.clase, self.esperanza_vida, self.exotica)
            )
            if result > 0:
                self.id = result    # Se actualiza el atributo id (el nuevo id asignado).
                return True
            return False
        except DBErrorData as e:
            raise ValueError(f"No se pudo crear la especie. {e}")
        except DBException:
            print(f"DEBUG - {EspecieModel.PREFIX} (create):")
            raise ModelException('No se pudo crear la especie en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar una Especie.
    # Retorna: - True si se modificó correctamente.
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool:
        try:      
            result = OperarBD.modifBD(
                "UPDATE ESPECIES "
                "SET nombre=%s, nombre_cientifico=%s, clase=%s, esperanza_vida=%s, exotica=%s "
                "WHERE id=%s",
                (self.nombre, self.nombre_cientifico, self.clase, self.esperanza_vida, self.exotica, self.id)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo actualizar la especie. {e}")
        except DBException:
            print(f"DEBUG - {EspecieModel.PREFIX} (update):")
            raise ModelException('No se pudo actualizar la especie en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar una Especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool:
        try:
            result = OperarBD.modifBD(
                "DELETE "
                "FROM ESPECIES "
                "WHERE id=%s",
                (id,)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo eliminar la especie. {e}")
        except DBException:
            print(f"DEBUG - {EspecieModel.PREFIX} (delete):")
            raise ModelException('No se pudo eliminar la especie en la base de datos.')