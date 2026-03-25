from ...database.accesoBD import OperarBD
from ...database.erroresBD import DBErrorData, DBException

class ModelException(Exception):
    # Errores ya procesados por el Model.
    # Se pueden enviar al frontend.
    pass

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Especialidad.
#------------------------------------------------------------------------------------------------------------------------

class EspecialidadModel:
    PREFIX = 'Base de Datos (Especialidad): '
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, nombre: str="", descripcion: str="", activa: int=0):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.activa = activa
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "descripcion" : self.descripcion,
            "activa" : self.activa
        }
    @staticmethod
    def deserializar(data: dict) -> 'EspecialidadModel':
        return EspecialidadModel(
            id = data.get('id', 0),
            nombre = data.get('nombre', ""),
            descripcion = data.get('descripcion', ""),
            activa = data.get('activa', 0)
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas las Especialidades.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
           return OperarBD.obtenerReg(
            "SELECT id, nombre, descripcion, activa "
            "FROM ESPECIALIDADES"
            )
        except DBException:
            print(f"DEBUG - {EspecialidadModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de especialidades. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Especialidad por Id.
    # Retorna:  - un diccionario con los datos si encontró la especialidad.
    #           - {} si no encontró la especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, nombre, descripcion, activa "
                "FROM ESPECIALIDADES "
                "WHERE id=%s",
                (id,)
            )
            if registros:
                return registros[0]
            return {}
        except DBException:
            print(f"DEBUG - {EspecialidadModel.PREFIX} (get_one):")
            raise ModelException(
                "No se pudo obtener el listado de especialidades. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #--------------------------------------------------------------------------------------------------------
    # Método para crear una Especialidad.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool:
        try:
            result = OperarBD.modifBD(
                "INSERT "
                "INTO ESPECIALIDADES (nombre, descripcion, activa) "
                "VALUES (%s, %s, %s)",
                (self.nombre, self.descripcion, self.activa)
            )
            if result > 0:
                self.id = result    # Se actualiza el atributo id (el nuevo id asignado).
                return True
            return False
        except DBErrorData as e:
            raise ValueError(f"No se pudo crear la especialidad. {e}")
        except DBException:
            print(f"DEBUG - {EspecialidadModel.PREFIX} (create):")
            raise ModelException('No se pudo crear la especialidad en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar una Especialidad.
    # Retorna: - True si se modificó correctamente.
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool:        
        try:
            result = OperarBD.modifBD(
                "UPDATE ESPECIALIDADES "
                "SET nombre=%s, descripcion=%s, activa=%s "
                "WHERE id=%s",
                (self.nombre, self.descripcion, self.activa, self.id)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo actualizar la especialidad. {e}")
        except DBException:
            print(f"DEBUG - {EspecialidadModel.PREFIX} (update):")
            raise ModelException('No se pudo actualizar la especialidad en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar una Especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool:
        try:
            result = OperarBD.modifBD(
                "DELETE "
                "FROM ESPECIALIDADES "
                "WHERE id=%s",
                (id,)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo eliminar la especialidad. {e}")
        except DBException:
            print(f"DEBUG - {EspecialidadModel.PREFIX} (delete):")
            raise ModelException('No se pudo eliminar la especialidad en la base de datos.')