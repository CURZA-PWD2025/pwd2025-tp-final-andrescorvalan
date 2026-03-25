import re
from .propietario_model import PropietarioModel, ModelException

#------------------------------------------------------------------------------------------------------------------------
# Clase PropietarioController para la entidad Propietario.
#------------------------------------------------------------------------------------------------------------------------
class PropietarioController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos los Propietarios.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            propietarios = PropietarioModel.get_all()
            cantidad = len(propietarios)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} propietarios con éxito."
            else:
                msg = "No se encontraron propietarios registrados."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': propietarios
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }     
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            propietario = PropietarioModel.get_one(id)
            if propietario:
                return {
                    'estado': 'ok',
                    'datos': propietario
                }
            else:
                return {
                    'estado': 'not_found',
                    'mensaje': f"No se encontro el propietario con ID {id} en la base de datos."
                }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }  
    #--------------------------------------------------------------------------------------------------------
    # Método estático para verificar la integridad y formato de los datos.
    # Retorna: - {} si los datos son correctos.
    #          - dict con el error si los datos son incorrectos o incompletos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def verificar_data(data: dict) -> dict:
        # Verificar existencia y que el valor no sea None ni "".
        for campo in ['nombre', 'apellido', 'dni']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Error en los datos, falta el campo obligatorio: {campo}.'
                }      
        # Validar el dni (todos números y longitud entre 7 y 10).
        if not re.match(r'^[0-9]+$', data['dni']) or len(data['dni'])<7 or len(data['dni'])>10:
            return {
                'estado': 'error', 
                'mensaje': 'Error en los datos, el DNI debe contener entre 7 y 10 dígitos.'
            }
        # Validar el teléfono (todos números).
        if data['telefono'] and not re.match(r'^[0-9]+$', data['telefono']):
            return {
                'estado': 'error', 
                'mensaje': 'Error en los datos: el teléfono debe contener solo dígitos.'
            }
        # Validar básicamente el Email: string@string.string.
        if data['email'] and not re.match(r'^.+@.+\..+$', data['email']):
             return {
                 'estado': 'error', 
                 'mensaje': 'Error en los datos: el formato del email es inválido (debe ser: usuario@dominio.com).'
            }
        return {} # Datos correctos.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear un Propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict:
        # Verficar data.
        error = PropietarioController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        try:
            propietario = PropietarioModel.deserializar(data)
            propietario.id = 0
            if propietario.create(): 
                return {
                    'estado': 'ok', 
                    'mensaje': 'Propietario creado con exito.',
                    'objeto': propietario.serializar()
                }
            #else
            return {
                'estado': 'error', 
                'mensaje': 'No se pudo crear el nuevo propietario en la base de datos. Intente más tarde.'
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
    # Método estático para actualizar un Propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'El ID del propietario es inválido o no fue enviado.'
            }
        # Verificar data
        error = PropietarioController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.

        propietario = PropietarioModel.deserializar(data)
        try:
            if propietario.update():
                return { 
                    'estado': 'ok', 
                    'mensaje': 'Propietario actualizado con exito.',
                    'objeto': propietario.serializar()
                }
            # Si la ejecucion llega aqui es porque:
            # a) no existe el registro.
            # b) no hubo cambios.
            existe = PropietarioModel.get_one(propietario.id)
            
            if not existe:
                return {
                    'estado': 'not_found',
                    'mensaje': 'El propietario ya no existe en la base de datos.'
                }
            return {
                'estado': 'ok', # Se trata como éxito para el usuario
                'mensaje': 'No se detectaron cambios, los datos están actualizados.',
                'objeto': propietario.serializar()
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
    # Método estático para eliminar un Propietario.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict:
        try:
            if PropietarioModel.delete(id):
                return {
                    'estado': 'ok',
                    'mensaje': f'El propietario con ID {id} ha sido eliminado con éxito.'
                }
            #else           
            return {
                'estado': 'not_found',
                'mensaje': f'El propietario con ID {id} ya no existe en la base de datos.'
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