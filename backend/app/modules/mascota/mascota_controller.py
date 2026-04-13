from datetime import datetime
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
            cantidad = len(mascotas)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} mascotas con éxito."
            else:
                msg = "No se encontraron mascotas registradas."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': mascotas
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
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
                    'mensaje': f"No se encontro la mascota con ID {id} en la base de datos."
                }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Métodos estático para verificar la integridad y formato de los datos.
    # Retorna: - {} si los datos son correctos.
    #          - dict con el error si los datos son incorrectos o incompletos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def verificar_data(data: dict) -> dict:
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
            fecha_nac = datetime.strptime(data['fecha_nac'], "%Y-%m-%d")
            ahora = datetime.now()
            if fecha_nac > ahora: 
                return {
                    'estado': 'error', 
                    'mensaje': 'La fecha de nacimiento no puede ser futura.'
                }
        except ValueError:
            return {
                'estado': 'error',
                'mensaje': 'La fecha de nacimiento no es válida o tiene un formato incorrecto.'
            }
        return {}
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear una Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict:
        # Verficar data.
        error = MascotaController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        try:
            mascota = MascotaModel(
                id = 0,
                nombre = data['nombre'],
                fecha_nac = data['fecha_nac'],
                sexo = data['sexo'],
                propietario = PropietarioModel(id = int(data['propietario_id'])),
                especie = EspecieModel(id = int(data['especie_id']))
            )
            if mascota.create():
                data_completo = mascota.serializar()
                data_completo["propietario"] = PropietarioModel.get_one(mascota.propietario.id)
                data_completo["especie"] = EspecieModel.get_one(mascota.especie.id)
                return {
                    'estado': 'ok',
                    'mensaje': 'Mascota creada con éxito.',
                    'objeto': data_completo
                }
            #else
            return {
                'estado': 'error', 
                'mensaje': 'No se pudo crear la nueva mascota en la base de datos. Intente más tarde.'
            }
        except ValueError as e: 
            return {
                'estado': 'error',
                'mensaje': f'{str(e)} Verifique los datos e intente más tarde.'
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para actualizar un Mascota.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'El ID de la mascota es inválido o no fue enviado.'
            }
        # Verficar data.
        error = MascotaController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        # Actualizar
        try:
            mascota = MascotaModel(
                id = data['id'],
                nombre = data['nombre'],
                fecha_nac = data['fecha_nac'],
                sexo = data['sexo'],
                propietario = PropietarioModel(id = int(data['propietario_id'])),
                especie = EspecieModel(id = int(data['especie_id']))
            )
            if mascota.update():
                data_completo = mascota.serializar()
                data_completo["propietario"] = PropietarioModel.get_one(mascota.propietario.id)
                data_completo["especie"] = EspecieModel.get_one(mascota.especie.id)
                return {
                    
                    'estado': 'ok', 
                    'mensaje': 'Mascota actualizada con éxito.',
                    'objeto': data_completo
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
                'mensaje': f'{str(e)} Verifique los datos e intente más tarde.'
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
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
                    'mensaje': f'La mascota con ID {id} ha sido eliminada con éxito.'
                }
            #else           
            return {
                'estado': 'not_found',
                'mensaje': f'La mascota con ID {id} ya no existe en la base de datos.'
            }
        except ValueError as e: 
            return {
                'estado': 'error',
                'mensaje': f'{str(e)}'
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }