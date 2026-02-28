import re
from .propietario_model import PropietarioModel

#------------------------------------------------------------------------------------------------------------------------
# Clase PropietarioController para la entidad Propietario.
#------------------------------------------------------------------------------------------------------------------------
class PropietarioController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos los Propietarios.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict] | None:
        return PropietarioModel.get_all()
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        return PropietarioModel.get_one(id)
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
                    'mensaje': f'Propietario: Falta el campo obligatorio: {campo}.'
                }      
        # Validar el dni (todos números y longitud 7 u 8).
        if not re.match(r'^[0-9]+$', data['dni']) or len(data['dni'])<7 or len(data['dni'])>8:
            return {
                'estado': 'error', 
                'mensaje': 'Propietario: El DNI debe contener solo 7 u 8 dígitos.'
            }
        # Validar el teléfono (todos números).
        if data['telefono'] and not re.match(r'^[0-9]+$', data['telefono']):
            return {
                'estado': 'error', 
                'mensaje': 'Propietario: El teléfono debe contener solo dígitos.'
            }
        # Validar básicamente el Email: string@string.string.
        if data['email'] and not re.match(r'^.+@.+\..+$', data['email']):
             return {
                 'estado': 'error', 
                 'mensaje': 'Propietario: El formato del email es inválido (debe ser: usuario@dominio.com).'
            }
        return {} # Datos correctos.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear un Propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict | None:
        # Verficar data.
        error = PropietarioController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        
        data_create = data.copy()
        data_create['id'] = 0
        
        propietario = PropietarioModel.deserializar(data_create)
        
        result = propietario.create()
        if result is True: 
            return {
                'estado': 'ok', 
                'mensaje': 'Propietario: Creación exitosa',
                'objeto': propietario.serializar()
            }
        if result is False:
            return {
                'estado': 'error', 
                'mensaje': 'Propietario: Error al intentar crear (verifique unicidad).'
            }
        return None # Excepción al intentar insertar en la BD.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para actualizar un Propietario.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict | None:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'Propietario: El ID es inválido o no fue enviado.'
            }
        # Verificar data
        error = PropietarioController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.

        propietario = PropietarioModel.deserializar(data)

        result = propietario.update()
        if result is None:
            return None # Excepción al intentar actualizar en la BD.
        
        if result is True:
            return {
                'estado': 'ok', 
                'mensaje': 'Propietario: Actualización exitosa.',
                'objeto': propietario.serializar()
            }
        
        # Si la ejecucion llega aqui es porque result == False: UPDATE no afectó filas por:
        # a) no existe el registro.
        # b) no hubo cambios.
        reg = PropietarioModel.get_one(data['id'])
        if reg == {}:   # no existe.
            return {
                'estado': 'not_found',
                'mensaje': 'Propietario: No existe el propietario que se quiere actualizar.'
            }
        #else: no se cambio nada.
        return {
            'estado': 'ok',
            'mensaje': 'Propietario: No hubo cambios (los datos enviados son iguales a los existentes).'
        }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para eliminar un Propietario.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict | None:
        result = PropietarioModel.delete(id)
        if result is True:
            return {
                'estado': 'ok',
                'mensaje': 'Propietario: Eliminación exitosa.'
            }
        if result is False:
            return {
                'estado': 'not_found',
                'mensaje': 'Propietario: No existe el registro.'
            }
        return None # Excepción al intentar eliminar en la BD.