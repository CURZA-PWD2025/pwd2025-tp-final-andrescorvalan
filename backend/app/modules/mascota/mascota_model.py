from ...database.accesoBD import OperarBD
from ...database.erroresBD import DBErrorData, DBException
from ..propietario.propietario_model import PropietarioModel
from ..especie.especie_model import EspecieModel
from datetime import date

class ModelException(Exception):
    # Errores ya procesados por el Model.
    # Se pueden enviar al frontend.
    pass

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Mascota.
#------------------------------------------------------------------------------------------------------------------------

class MascotaModel:
    PREFIX = 'Base de Datos (Mascota): '
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, nombre: str="", fecha_nac: str="", sexo:str="", propietario: PropietarioModel=None, 
                 especie: EspecieModel=None):
        self.id = id
        self.nombre = nombre
        self.fecha_nac = fecha_nac
        self.sexo = sexo
        self.propietario = propietario
        self.especie = especie
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        fecha_str = self.fecha_nac.isoformat() if isinstance(self.fecha_nac, date) else self.fecha_nac
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_nac": fecha_str,
            "sexo": self.sexo,
            "propietario": self.propietario.serializar() if self.propietario else None,
            "especie": self.especie.serializar() if self.especie else None,
        }
    @staticmethod
    def deserializar(data: dict) -> 'MascotaModel':
        propietario_data = data.get('propietario')
        especie_data = data.get('especie')
        return MascotaModel(
            id = data.get("id", 0),
            nombre = data.get("nombre", ""),
            fecha_nac = data.get("fecha_nac", ""),
            sexo = data.get("sexo", ""),
            propietario = PropietarioModel.deserializar(propietario_data) if propietario_data else None,
            especie = EspecieModel.deserializar(especie_data) if especie_data else None
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un dict completo, incluyendo el dict de propietario y de especie.
    #-------------------------------------------------------------------------------------------------------- 
    @staticmethod
    def get_data_completo(data: dict) -> dict:
        data_db = data.copy()

        if data_db.get('fecha_nac') and isinstance(data_db['fecha_nac'], date):
            data_db['fecha_nac'] = data_db['fecha_nac'].isoformat()

        data_db['propietario'] = PropietarioModel.get_one(data_db['propietario_id'])
        if data_db['propietario'] == {}:
            data_db['propietario'] = None
        
        data_db['especie'] = EspecieModel.get_one(data_db['especie_id'])
        if data_db['especie'] == {}:
            data_db['especie'] = None

        data_db.pop('propietario_id', None)
        data_db.pop('especie_id', None)

        return data_db
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas los Mascotas.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, nombre, fecha_nac, sexo, propietario_id, especie_id "
                "FROM MASCOTAS"
            )
            listado = []
            for mascota_data in registros:
                listado.append(
                    MascotaModel.get_data_completo(mascota_data)
                )
            return listado
        except DBException:
            print(f"DEBUG - {MascotaModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de mascotas. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )    
    #---------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Mascota por Id.
    # Retorna:  - Un diccionario con los datos si encontró el registro.
    #           - {} si no encontró el registro.
    # --------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, nombre, fecha_nac, sexo, propietario_id, especie_id "
                "FROM MASCOTAS "
                "WHERE id=%s", 
                (id,)
            )
            if registros:
                return MascotaModel.get_data_completo(registros[0])                
            return {}
        except DBException:
            print(f"DEBUG - {MascotaModel.PREFIX} (get_one):")
            raise ModelException(
                "No se pudo obtener la mascota. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )    #--------------------------------------------------------------------------------------------------------
    # Método para crear una Mascota.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool:
        if not self.propietario or not self.propietario.id:
            raise ValueError(f"{MascotaModel.PREFIX} Se requiere un propietario para registrar la mascota.")
        
        if not self.especie or not self.especie.id:
            raise ValueError(f"{MascotaModel.PREFIX} Se requiere especificar la especie de la mascota.")
        
        try:
            result = OperarBD.modifBD(
                "INSERT "
                "INTO MASCOTAS (nombre, fecha_nac, sexo, propietario_id, especie_id) " \
                "VALUES (%s, %s, %s, %s, %s)",
                (self.nombre, self.fecha_nac, self.sexo, self.propietario.id, self.especie.id)
            )
            if result > 0:
                self.id = result    # Se actualiza el atributo id.
                return True
            return False
        except DBErrorData as e:
            raise ValueError(f"No se pudo crear la mascota. {e}")
        except DBException:
            print(f"DEBUG - {MascotaModel.PREFIX} (create):")
            raise ModelException('No se pudo crear la mascota en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar un Mascota.
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios).
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool:
        try:
            result = OperarBD.modifBD(
                "UPDATE MASCOTAS "
                "SET nombre=%s, fecha_nac=%s, sexo=%s, propietario_id=%s, especie_id=%s "
                "WHERE id=%s",
                (self.nombre, self.fecha_nac, self.sexo, self.propietario.id, self.especie.id, self.id)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo actualizar la mascota. {e}")
        except DBException:
            print(f"DEBUG - {MascotaModel.PREFIX} (update):")
            raise ModelException('No se pudo actualizar la mascota en la base de datos.')
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar un Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool:
        try:
            result = OperarBD.modifBD(
                "DELETE "
                "FROM MASCOTAS "
                "WHERE id=%s",
                (id,)
            )
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo eliminar la mascota. {e}")
        except DBException:
            print(f"DEBUG - {MascotaModel.PREFIX} (delete):")
            raise ModelException('No se pudo eliminar la mascota en la base de datos.')