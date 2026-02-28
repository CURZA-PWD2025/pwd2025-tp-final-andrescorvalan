import datetime
from .mascota_model import MascotaModel
from ..propietario.propietario_model import PropietarioModel
from ..especie.especie_model import EspecieModel

#------------------------------------------------------------------------------------------------------------------------
# Clase MascotaController para la entidad Mascota.
#------------------------------------------------------------------------------------------------------------------------
class MascotaController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas los Mascotas.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict] | None:
        return MascotaModel.get_all()
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        return MascotaModel.get_one(id)
    #--------------------------------------------------------------------------------------------------------
    # Métodos estático para verificar la integridad y formato de los datos.
    # Retorna: - {} si los datos son correctos.
    #          - dict con el error si los datos son incorrectos o incompletos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def verificar_data_comun(data: dict) -> dict:
        # Verificar existencia de nombre y fecha de nacimiento.
        print(data)
        for campo in ['nombre', 'fecha_nac']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Mascota: Falta el campo obligatorio: {campo}.'
                }
        # Verificar propietario_id y especie_id.
        for campo in ['propietario_id', 'especie_id']:
            if campo not in data:
                return {
                    "estado": "error",
                    "mensaje": f"Mascota: Falta el campo obligatorio {campo}."
                }
            if not isinstance(data[campo], int) or data[campo] <= 0:
                return {
                    "estado": "error",
                    "mensaje": f"Mascota: {campo} debe ser entero positivo."
                }
       # Verificar la fecha.
        try:
            datetime.datetime.strptime(data["fecha_nac"], "%Y-%m-%d")
        except:
            return {
                'estado': 'error',
                'mensaje': 'Mascota: La fecha de nacimiento debe tener formato YYYY-MM-DD.'
            }
        # Chequear existencia del propietario y obtener su data.
        propietario_data = PropietarioModel.get_one(data["propietario_id"])
        if propietario_data == {}:
            return {
                'estado': 'error',
                'mensaje': 'Mascota: El propietario especificado no existe.'
            }
        # Chequear existencia de la especie y obtener su data.
        especie_data = EspecieModel.get_one(data['especie_id'])
        if especie_data == {}:
            return {
                'estado': 'error',
                'mensaje': 'Mascota: La especie especificada no existe.'
            }
        
        # Si se llega aca, todo en orden.
        # Crear data completo.
        data_completo = data.copy()
        data_completo["propietario"] = propietario_data
        data_completo["especie"] = especie_data
        del data_completo["propietario_id"]
        del data_completo["especie_id"]
        return {
            'estado': 'ok',
            'data_completo': data_completo
        }

    @staticmethod  
    def verificar_data_create(data: dict) -> dict:
        return MascotaController.verificar_data_comun(data)
    
    @staticmethod  
    def verificar_data_update(data: dict) -> dict:
        print("Verificando data update:", data)
        # Verificar ID obligatorio.
        if not isinstance(data.get("id"), int) or data.get("id") <= 0:
            return {
                'estado': 'error',
                'mensaje': 'Mascota: El ID es obligatorio para actualizar y debe ser un entero positivo.'
            }
        # Chequear existencia de la mascota.
        if MascotaModel.get_one(data["id"]) == {}:
            return {
                'estado': 'not_found',
                'mensaje': 'Mascota: La mascota a actualizar no existe.'
            }
        return MascotaController.verificar_data_comun(data)
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear un Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict | None:
        # Verficar data.
        estado = MascotaController.verificar_data_create(data)
        if estado['estado'] != 'ok':
            return estado # Devuelve el error de validación.
        # Obtener el data completo, setear id=0, y un objeto de MascotaModel (completo, con Propietario y Especie).
        data_create = estado['data_completo']
        data_create['id'] = 0
        mascota = MascotaModel.deserializar(data_create)
        # Crear en la BD.
        result = mascota.create()
        if result is True: 
            return {
                'estado': 'ok', 
                'mensaje': 'Mascota: Creación exitosa',
                'objeto': mascota.serializar()
            }
        if result is False:
            return {
                'estado': 'error', 
                'mensaje': 'Mascota: Error al intentar crear.'
            }
        return None # Excepción al intentar insertar en la BD.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para actualizar un Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict | None:
        # Verificar data.
        estado = MascotaController.verificar_data_update(data)
        if estado['estado'] != 'ok':
            return estado # Devuelve el error de validación.
        # Obtener el data completo y un objeto de MascotaModel (completo, con Propietario y Especie).
        data_update = estado['data_completo']
        mascota = MascotaModel.deserializar(data_update)
        print(mascota)
        # Actualizar en la BD.
        result = mascota.update()
        if result is None:
            return None # Excepción al intentar actualizar en la BD.
        if result is True:
            return {
                'estado': 'ok', 
                'mensaje': 'Mascota: Actualización exitosa.',
                'objeto': mascota.serializar()
            }
        # Si la ejecucion llega aqui es porque result == False: UPDATE no afectó filas por:
        # a) no existe el registro.
        # b) no hubo cambios.
        reg = MascotaModel.get_one(data['id'])
        if reg == {}:   # no existe.
            return {
                'estado': 'not_found',
                'mensaje': 'Mascota: No existe la mascota que se quiere actualizar.'
            }
        #else: no se cambio nada.
        return {
            'estado': 'ok',
            'mensaje': 'Mascota: No hubo cambios (los datos enviados son iguales a los existentes).'
        }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para eliminar un Mascota.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict | None:
        result = MascotaModel.delete(id)
        if result is True:
            return {
                'estado': 'ok',
                'mensaje': 'Mascota: Eliminación exitosa.'
            }
        if result is False:
            return {
                'estado': 'not_found',
                'mensaje': 'Mascota: No existe el registro.'
            }
        return None # Excepción al intentar eliminar en la BD.