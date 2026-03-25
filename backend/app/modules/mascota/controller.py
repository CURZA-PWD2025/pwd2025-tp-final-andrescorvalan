import datetime
from .mascota_model import MascotaModel, ModelException
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
    def get_all() -> list[dict]:
        try:
            mascotas = MascotaModel.get_all()
            return {
                'estado': 'ok',
                'datos': mascotas
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)} Intente más tarde.'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            mascota = MascotaModel.get_one(id)
            if mascota:
                return {
                    'estado': 'ok',
                    'datos': mascota
                }
            else:
                return {
                    'estado': 'not_found',
                    'mensaje': f"No se encontro la mascota con Id={id}. Intente más tarde."
                }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)} Intente más tarde.'
            }
    #--------------------------------------------------------------------------------------------------------
    # Métodos estático para verificar la integridad y formato de los datos.
    # Retorna: - {} si los datos son correctos.
    #          - dict con el error si los datos son incorrectos o incompletos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def verificar_data_comun(data: dict) -> dict:
        # Verificar existencia de nombre y fecha de nacimiento.
        for campo in ['nombre', 'fecha_nac', 'sexo']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Falta el campo obligatorio: {campo}.'
                }
        # Verificar propietario_id y especie_id.
        for campo in ['propietario_id', 'especie_id']:
            if campo not in data:
                return {
                    "estado": "error",
                    "mensaje": f"Falta el campo obligatorio {campo}."
                }
            if not isinstance(data[campo], int) or data[campo] <= 0:
                return {
                    "estado": "error",
                    "mensaje": f"El {campo} debe ser un entero positivo."
                }
       # Verificar la fecha.
        try:
            datetime.datetime.strptime(data["fecha_nac"], "%Y-%m-%d")
        except ValueError:
            return {
                'estado': 'error',
                'mensaje': 'La fecha de nacimiento debe tener formato YYYY-MM-DD.'
            }
        # Chequear existencia del propietario y obtener su data.
        propietario_data = PropietarioModel.get_one(data["propietario_id"])
        if propietario_data == {}:
            return {
                'estado': 'error',
                'mensaje': 'El propietario especificado no existe.'
            }
        # Chequear existencia de la especie y obtener su data.
        especie_data = EspecieModel.get_one(data['especie_id'])
        if especie_data == {}:
            return {
                'estado': 'error',
                'mensaje': 'La especie especificada no existe.'
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
        # Verificar ID obligatorio.
        if not isinstance(data.get("id"), int) or data.get("id") <= 0:
            return {
                'estado': 'error',
                'mensaje': 'El ID de la mascota es obligatorio para actualizar y debe ser un entero positivo.'
            }
        # Chequear existencia de la mascota.
        if MascotaModel.get_one(data["id"]) == {}:
            return {
                'estado': 'not_found',
                'mensaje': 'El ID de la mascota es inválido o no fue enviado.'
            }
        return MascotaController.verificar_data_comun(data)

    @staticmethod
    def create(data: dict) -> dict:
        # Verficar data.
        validacion = MascotaController.verificar_data(data)
        if validacion['estado'] != 'ok':
               return validacion
        # Crear
        try:
            mascota = MascotaModel.deserializar(validacion['data_completo'])
            mascota.id = 0
            if mascota.create(): 
                return {
                    'estado': 'ok', 
                    'mensaje': 'Mascota creada con éxito',
                    'objeto': mascota.serializar()
                }
            #else
            return {
                'estado': 'error', 
                'mensaje': 'No se pudo crear la nueva mascota. Intente más tarde.'
            }
        except ValueError as e: 
            return {
                'estado': 'error',
                'mensaje': f'{str(e)} Intente más tarde.'
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)} Intente más tarde.'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para actualizar un Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict:
        # Verficar data.
        result_valid = MascotaController.verificar_data(data)
        if result_valid['estado'] != 'ok':
               return result_valid
        # Actualizar
        try:
            data_update = result_valid['data_completo']
            mascota = MascotaModel.deserializar(data_update)
            # Actualizar en la BD.
            if mascota.update():
                return { 
                    'estado': 'ok', 
                    'mensaje': 'Mascota actualizada con éxito.',
                    'objeto': mascota.serializar()
                }
            # Si la ejecucion llega aqui es porque:
            # a) no existe el registro.
            # b) no hubo cambios.
            existe = MascotaModel.get_one(mascota.id)
            if not existe:
                return {
                    'estado': 'not_found',
                    'mensaje': 'La mascota ya no existe en la base de datos.'
                }
            return {
                'estado': 'ok', # Se trata como éxito para el usuario
                'mensaje': 'No se detectaron cambios, los datos están actualizados.',
                'objeto': mascota.serializar()
            }
        except ValueError as e: 
            return {
                'estado': 'error',
                'mensaje': f'{str(e)} Intente más tarde.'
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)} Intente más tarde.'
            } 
    #--------------------------------------------------------------------------------------------------------
    # Método estático para eliminar un Mascota.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict:
        try:
            if MascotaModel.delete(id):
                return {
                    'estado': 'ok',
                    'mensaje': 'Mascota eliminada con éxito.'
                }
            #else           
            return {
                'estado': 'not_found',
                'mensaje': 'La mascota ya no existe en la base de datos.'
            }
        except ValueError as e: 
            return {
                'estado': 'error',
                'mensaje': f'{str(e)} Intente más tarde.'
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)} Intente más tarde.'
            }