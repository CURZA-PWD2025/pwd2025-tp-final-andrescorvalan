import re
from .especialidad_model import EspecialidadModel

#------------------------------------------------------------------------------------------------------------------------
# Clase EspecialidadController para la entidad Especialidad.
#------------------------------------------------------------------------------------------------------------------------
class EspecialidadController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas las Especialidades.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict] | None:
        return EspecialidadModel.get_all()
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        return EspecialidadModel.get_one(id)
    #--------------------------------------------------------------------------------------------------------
    # Método estático para verificar la integridad y formato de los datos.
    # Retorna: - {} si los datos son correctos.
    #          - dict con el error si los datos son incorrectos o incompletos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def verificar_data(data: dict) -> dict:
        # Verificar existencia y que el valor no sea None ni "".
        for campo in ['nombre', 'descripcion']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Especialidad: Falta el campo obligatorio: {campo}.'
                }    
        return {} # Datos correctos.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear una Especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict | None:
        # Verficar data.
        error = EspecialidadController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        
        data_create = data.copy()
        data_create['id'] = 0
        
        especialidad = EspecialidadModel.deserializar(data_create)
        
        result = especialidad.create()
        if result is True: 
            return {
                'estado': 'ok', 
                'mensaje': 'Especialidad: Creación exitosa',
                'objeto': especialidad.serializar()
            }
        if result is False:
            return {
                'estado': 'error', 
                'mensaje': 'Especialidad: Error al intentar crear (verifique unicidad).'
            }
        return None # Excepción al intentar insertar en la BD.

    #--------------------------------------------------------------------------------------------------------
    # Método estático para actualizar una Especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict | None:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'Especialidad: El ID es inválido o no fue enviado.'
            }
        # Verificar data.
        error = EspecialidadController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.

        especialidad = EspecialidadModel.deserializar(data)

        result = especialidad.update()
        if result is None:
            return None # Excepción al intentar actualizar en la BD.
        
        if result is True:
            return {
                'estado': 'ok', 
                'mensaje': 'Especialidad: Actualización exitosa.',
                'objeto': especialidad.serializar()
            }
        
        # Si la ejecucion llega aqui es porque result == False: UPDATE no afectó filas por:
        # a) no existe el registro.
        # b) no hubo cambios.
        reg = EspecialidadModel.get_one(data['id'])
        if reg == {}:   # no existe.
            return {
                'estado': 'not_found',
                'mensaje': 'Especialidad: No existe el registro que se quiere actualizar.'
            }
        #else: no se cambio nada.
        return {
            'estado': 'ok',
            'mensaje': 'Especialidad: No hubo cambios (los datos enviados son iguales a los existentes).'
        }
    
    #--------------------------------------------------------------------------------------------------------
    # Método estático para eliminar una Especialidad.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict | None:
        result = EspecialidadModel.delete(id)
        if result is True:
            return {
                'estado': 'ok',
                'mensaje': 'Especialidad: Eliminación exitosa.'
            }
        if result is False:
            return {
                'estado': 'not_found',
                'mensaje': 'Especialidad: No existe el registro.'
            }
        return None # Excepción al intentar eliminar en la BD.