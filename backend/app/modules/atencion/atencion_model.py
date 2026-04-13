from ...database.accesoBD import OperarBD
from ...database.erroresBD import DBErrorData, DBException
from ..veterinario.veterinario_model import VeterinarioModel
from ..mascota.mascota_model import MascotaModel
from datetime import date

class ModelException(Exception):
    # Errores ya procesados por el Model.
    # Se pueden encviar al frontend.
    pass

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Atencion.
#------------------------------------------------------------------------------------------------------------------------

class AtencionModel:
    PREFIX = 'Base de Datos (Atencion): '
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, fecha: str="", 
                 diagnostico: str="", tratamiento: str="", observaciones: str="",
                 mascota: MascotaModel=None, 
                 veterinario: VeterinarioModel=None):
        self.id = id
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.mascota = mascota
        self.veterinario = veterinario

    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        fecha_str = self.fecha.isoformat() if isinstance(self.fecha, date) else self.fecha
        return {
            "id": self.id,
            "fecha": fecha_str,
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento,
            "observaciones": self.observaciones,
            "mascota": self.mascota.serializar() if self.mascota else None,
            "veterinario": self.veterinario.serializar() if self.veterinario else None,
        }
    @staticmethod
    def deserializar(data: dict) -> 'AtencionModel':
        mascota_data = data.get('mascota')
        veterinario_data = data.get('veterinario')
        return AtencionModel(
            id = data.get("id", 0),
            fecha = data.get("fecha", ""),
            diagnostico = data.get("diagnostico", ""),
            tratamiento = data.get("tratamiento", ""),
            observaciones = data.get("observaciones", ""),
            mascota = MascotaModel.deserializar(mascota_data) if mascota_data else None,
            veterinario = VeterinarioModel.deserializar(veterinario_data) if veterinario_data else None
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un dict completo, incluyendo el dict de mascota y de veterinario .
    #-------------------------------------------------------------------------------------------------------- 
    @staticmethod
    def get_data_completo(data: dict) -> dict:
        data_db = data.copy()

        if data_db.get('fecha') and isinstance(data_db['fecha'], date):
            data_db['fecha'] = data_db['fecha'].isoformat()

        data_db['mascota'] = MascotaModel.get_one(data_db['mascota_id'])
        if data_db['mascota'] == {}:
            data_db['mascota'] = None
        
        data_db['veterinario'] = VeterinarioModel.get_one(data_db['veterinario_id'])
        if data_db['veterinario'] == {}:
            data_db['veterinario'] = None

        data_db.pop('mascota_id', None)
        data_db.pop('veterinario_id', None)

        return data_db
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas las atenciones.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, fecha, diagnostico, tratamiento, observaciones, mascota_id, veterinario_id "
                "FROM ATENCIONES ORDER BY fecha DESC"
            )
            listado = []
            for atencion_data in registros:
                listado.append(
                    AtencionModel.get_data_completo(atencion_data)
                )
            return listado
        except DBException:
            print(f"DEBUG - {AtencionModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de atenciones. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #---------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Atencion por Id.
    # Retorna:  - Un diccionario con los datos si encontró el registro.
    #           - {} si no encontró el registro.
    # --------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, fecha, diagnostico, tratamiento, observaciones, mascota_id, veterinario_id "
                "FROM ATENCIONES "
                "WHERE id=%s", 
                (id,)
            )
            if registros:
                return AtencionModel.get_data_completo(registros[0])                
            return {}
        except DBException:
            print(f"DEBUG - {AtencionModel.PREFIX} (get_one):")
            raise ModelException(
                "No se pudo obtener la atencion. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #---------------------------------------------------------------------------------------------------------
    # Método estático para obtener las atenciones de un animal.
    # Retorna:  - Un diccionario con los datos si encontró registros.
    #           - {} si no encontró registros.
    # --------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_by_mascota(mascota_id: int) -> list[dict]:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, fecha, diagnostico, tratamiento, observaciones, mascota_id, veterinario_id "
                "FROM ATENCIONES WHERE mascota_id = %s ORDER BY fecha DESC",
                (mascota_id,)
            )
            listado = []
            for atencion_data in registros:
                listado.append(
                    AtencionModel.get_data_completo(atencion_data)
                )
            return listado
        except DBException:
            raise ModelException('No se pudo recuperar el historial clínico.')
    #--------------------------------------------------------------------------------------------------------
    # Método para crear una Atencion.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool:
        if not self.mascota or not self.mascota.id:
            raise ValueError(f"{AtencionModel.PREFIX} Se requiere una mascota para registrar la atención.")
        
        if not self.veterinario or not self.veterinario.id:
            raise ValueError(f"{AtencionModel.PREFIX} Se requiere especificar el veterinario de la atención.")
        
        try:
            result = OperarBD.modifBD(
                "INSERT "
                "INTO ATENCIONES (fecha, diagnostico, tratamiento, observaciones, mascota_id, veterinario_id) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (self.fecha, self.diagnostico, self.tratamiento, 
                 self.observaciones, self.mascota.id, self.veterinario.id)
            )
            if result > 0:
                self.id = result    # Se actualiza el atributo id.
                return True
            return False
        except DBErrorData as e:
            raise ValueError(f"No se pudo crear la atención. {e}")
        except DBException:
            print(f"DEBUG - {AtencionModel.PREFIX} (create):")
            raise ModelException('No se pudo crear la atención en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar una Atencion.
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios).
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool:
        try:
            result = OperarBD.modifBD(
                "UPDATE ATENCIONES "
                "SET fecha=%s, diagnostico=%s, tratamiento=%s, observaciones=%s, mascota_id=%s, veterinario_id=%s "
                "WHERE id=%s",
                (self.fecha, self.diagnostico, self.tratamiento, self.observaciones, self.mascota.id, self.veterinario.id, self.id)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo actualizar la atención. {e}")
        except DBException:
            print(f"DEBUG - {AtencionModel.PREFIX} (update):")
            raise ModelException('No se pudo actualizar la atención en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar una Atencion.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool:
        try:
            result = OperarBD.modifBD(
                "DELETE "
                "FROM ATENCIONES "
                "WHERE id=%s",
                (id,)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo eliminar la atención. {e}")
        except DBException:
            print(f"DEBUG - {AtencionModel.PREFIX} (delete):")
            raise ModelException('No se pudo eliminar la atención en la base de datos.')