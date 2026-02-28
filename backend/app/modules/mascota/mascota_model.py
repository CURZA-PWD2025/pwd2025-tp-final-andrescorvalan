from ...database.accesoBD import OperarBD
from ..propietario.propietario_model import PropietarioModel
from ..especie.especie_model import EspecieModel

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Mascota.
#------------------------------------------------------------------------------------------------------------------------

class MascotaModel:
    #--------------------------------------------------------------------------------------------------------
    # Constructor.
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, nombre: str="", fecha_nac: str="", propietario: PropietarioModel=None, 
                 especie: EspecieModel=None):
        self.id = id
        self.nombre = nombre
        self.fecha_nac = fecha_nac
        self.propietario = propietario
        self.especie = especie
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización.
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_nac": self.fecha_nac,
            "propietario": self.propietario.serializar() if self.propietario else None,
            "especie": self.especie.serializar() if self.especie else None,
        }
    @staticmethod
    def deserializar(data: dict) -> 'MascotaModel':
        return MascotaModel(
            id = data["id"],
            nombre = data["nombre"],
            fecha_nac = data["fecha_nac"],
            propietario = PropietarioModel.deserializar(data['propietario']),
            especie = EspecieModel.deserializar(data['especie'])
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un dict completo, incluyendo el dict de propietario y de especie.
    #-------------------------------------------------------------------------------------------------------- 
    @staticmethod
    def get_data_completo(data: dict) -> dict:
        data_db = data.copy()
        if data_db['fecha_nac']:
            data_db['fecha_nac'] = data_db['fecha_nac'].isoformat()
        
        data_db['propietario'] = PropietarioModel.get_one(data_db['propietario_id'])
        if data_db['propietario'] == {}:
            data_db['propietario'] = None
        
        data_db['especie'] = EspecieModel.get_one(data_db['especie_id'])
        if data_db['especie'] == {}:
            data_db['especie'] = None

        del data_db['propietario_id']
        del data_db['especie_id']

        return data_db
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos los Mascotas.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict] | None:
        mascotas_bd = OperarBD.obtenerReg("SELECT * FROM MASCOTAS")
        if mascotas_bd is None:
            return None
        listado = []
        for mascota_data in mascotas_bd:
            listado.append(
                MascotaModel.get_data_completo(mascota_data)
            )
           
        return listado
    #---------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Mascota por Id.
    # Retorna:  - un diccionario con los datos si encontró el registro.
    #           - {} si no encontró el registro.
    #           - None si hubo una excepción.
    # --------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        mascotas_bd = OperarBD.obtenerReg("SELECT * FROM MASCOTAS WHERE id=%s", (id,))
        if mascotas_bd is None:
            return None
        if mascotas_bd:
            return MascotaModel.get_data_completo(mascotas_bd[0])
        else:
            return {}
    #--------------------------------------------------------------------------------------------------------
    # Método para crear una Mascota.
    # Retorna: - True si se inserto correctamente.
    #          - False si no se pudo insertar.
    #          - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool | None:
        result = OperarBD.modifBD(
            "INSERT INTO MASCOTAS (nombre, fecha_nac, propietario_id, especie_id) " \
            "VALUES (%s, %s, %s, %s)",
            (self.nombre, self.fecha_nac, self.propietario.id, self.especie.id)
        )
        if result == None:
            return None         # Alguna excepción.
        if result > 0:
            self.id = result    # Se actualiza el atributo id (el nuevo id para este registro).
            return True         # Se insertó correctamente.
        else:
            return False        # No se pudo insertar el nuevo mascota.
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar un Mascota.
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios).
    #          - None si hubo una excepción.
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool | None:
        result = OperarBD.modifBD(
            "UPDATE MASCOTAS SET nombre=%s, fecha_nac=%s, propietario_id=%s, especie_id=%s WHERE id=%s",
            (self.nombre, self.fecha_nac, self.propietario.id, self.especie.id, self.id)
        )
        if result == None:
            return None     # Alguna excepción.
        return result == 1  # True si se actualizó correctamente, False si no se cambio la BD. 
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar un Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool | None:
        result = OperarBD.modifBD("DELETE FROM MASCOTAS WHERE id=%s", (id,))
        if result == None:
            return None     # Alguna excepción.
        return result == 1  # True si se elimino, sino False.