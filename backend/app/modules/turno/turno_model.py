from ...database.accesoBD import OperarBD
from ...database.erroresBD import DBErrorData, DBException
from ..veterinario.veterinario_model import VeterinarioModel
from ..mascota.mascota_model import MascotaModel
from datetime import datetime

class ModelException(Exception):
    # Errores ya procesados por el Model.
    # Se pueden encviar al frontend.
    pass

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidadTurno.
#------------------------------------------------------------------------------------------------------------------------

class TurnoModel:
    PREFIX = 'Base de Datos (Turno): '
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, fecha_hora: str="", 
                 estado: str="", motivo: str="",
                 mascota: MascotaModel=None, 
                 veterinario: VeterinarioModel=None):
        self.id = id
        self.fecha_hora = fecha_hora
        self.motivo = motivo
        self.estado = estado
        self.mascota = mascota
        self.veterinario = veterinario
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        fecha_con_t = self.fecha_hora.replace(' ', 'T') if self.fecha_hora else ""
        return {
            "id": self.id,
            "fecha_hora": fecha_con_t,
            "motivo": self.motivo,
            "estado": self.estado,
            "mascota": self.mascota.serializar() if self.mascota else None,
            "veterinario": self.veterinario.serializar() if self.veterinario else None,
        }
    @staticmethod
    def deserializar(data: dict) -> 'TurnoModel':
        mascota_data = data.get('mascota')
        veterinario_data = data.get('veterinario')
        return TurnoModel(
            id = data.get("id", 0),
            fecha_hora = data.get("fecha_hora", ""),
            motivo = data.get("motivo", ""),
            estado = data.get("estado", ""),
            mascota = MascotaModel.deserializar(mascota_data) if mascota_data else None,
            veterinario = VeterinarioModel.deserializar(veterinario_data) if veterinario_data else None
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un dict completo, incluyendo el dict de mascota y de veterinario.
    #-------------------------------------------------------------------------------------------------------- 
    @staticmethod
    def get_data_completo(data: dict) -> dict:
        data_db = data.copy()

        if data_db.get('fecha_hora'):
            fecha = data_db['fecha_hora']
            if isinstance(fecha, datetime):
                data_db['fecha_hora'] = fecha.isoformat()
            elif isinstance(fecha, str):
                data_db['fecha_hora'] = fecha.replace(' ', 'T')

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
    # Método estático para obtener todas los turnos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, fecha_hora, motivo, estado, mascota_id, veterinario_id "
                "FROM TURNOS ORDER BY fecha_hora DESC"
            )
            listado = []
            for turno_data in registros:
                listado.append(
                   TurnoModel.get_data_completo(turno_data)
                )
            return listado
        except DBException:
            print(f"DEBUG - {TurnoModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de turnos. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #---------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Turno por Id.
    # Retorna:  - Un diccionario con los datos si encontró el registro.
    #           - {} si no encontró el registro.
    # --------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, fecha_hora, motivo, estado, mascota_id, veterinario_id "
                "FROM TURNOS "
                "WHERE id=%s", 
                (id,)
            )
            if registros:
                return TurnoModel.get_data_completo(registros[0])                
            return {}
        except DBException:
            print(f"DEBUG - {TurnoModel.PREFIX} (get_one):")
            raise ModelException(
                "No se pudo obtener el turno. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #---------------------------------------------------------------------------------------------------------
    # Método estático para obtener las turnos futuros.
    # Retorna:  - Un diccionario con los datos si encontró registros.
    #           - {} si no encontró registros.
    # --------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_proximos() -> list[dict]:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, fecha_hora, motivo, estado, mascota_id, veterinario_id "
                "FROM TURNOS "
                "WHERE DATE(fecha_hora) >= CURDATE() ORDER BY fecha_hora ASC"
            )
            listado = []
            for turno_data in registros:
                listado.append(
                   TurnoModel.get_data_completo(turno_data)
                )
            return listado
        except DBException:
            print(f"DEBUG - {TurnoModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de turnos futuros. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #---------------------------------------------------------------------------------------------------------
    # Método estático para obtener las turnos futuros.
    # Retorna:  - Un diccionario con los datos si encontró registros.
    #           - {} si no encontró registros.
    # --------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_historial() -> list[dict]:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, fecha_hora, motivo, estado, mascota_id, veterinario_id "
                "FROM TURNOS "
                "WHERE DATE(fecha_hora) < CURDATE() ORDER BY fecha_hora DESC"
            )
            listado = []
            for turno_data in registros:
                listado.append(
                   TurnoModel.get_data_completo(turno_data)
                )
            return listado
        except DBException:
            print(f"DEBUG - {TurnoModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de turnos pasados. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )
    #--------------------------------------------------------------------------------------------------------
    # Método para crear un Turno.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool:
        if not self.mascota or not self.mascota.id:
            raise ValueError(f"{TurnoModel.PREFIX} Se requiere una mascota para registrar un turno.")
        
        if not self.veterinario or not self.veterinario.id:
            raise ValueError(f"{TurnoModel.PREFIX} Se requiere especificar el veterinario en un turno.")
        
        try:
            fecha_mysql = self.fecha_hora.replace('T', ' ')
            result = OperarBD.modifBD(
                "INSERT "
                "INTO TURNOS (fecha_hora, motivo, estado, mascota_id, veterinario_id) "
                "VALUES (%s, %s, %s, %s, %s)",
                (fecha_mysql, self.motivo, self.estado, self.mascota.id, self.veterinario.id)
            )
            if result > 0:
                self.id = result    # Se actualiza el atributo id.
                return True
            return False
        except DBErrorData as e:
            if "Dato duplicado" in str(e):
                raise ValueError(
                "El veterinario ya tiene un turno asignado en esa fecha y horario."
            )
            raise ValueError(f"No se pudo crear el turno. {e}")
        except DBException:
            print(f"DEBUG - {TurnoModel.PREFIX} (create):")
            raise ModelException('No se pudo crear el turno en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar un Turno.
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios).
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool:
        try:
            fecha_mysql = self.fecha_hora.replace('T', ' ')
            result = OperarBD.modifBD(
                "UPDATE TURNOS "
                "SET fecha_hora=%s, motivo=%s, estado=%s, mascota_id=%s, veterinario_id=%s "
                "WHERE id=%s",
                (fecha_mysql, self.motivo, self.estado, self.mascota.id, self.veterinario.id, self.id)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo actualizar el turno. {e}")
        except DBException:
            print(f"DEBUG - {TurnoModel.PREFIX} (update):")
            raise ModelException('No se pudo actualizar el turno en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar un Turno.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool:
        try:
            result = OperarBD.modifBD(
                "DELETE "
                "FROM TURNOS "
                "WHERE id=%s",
                (id,)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo eliminar el turno. {e}")
        except DBException:
            print(f"DEBUG - {TurnoModel.PREFIX} (delete):")
            raise ModelException('No se pudo eliminar el turno en la base de datos.')