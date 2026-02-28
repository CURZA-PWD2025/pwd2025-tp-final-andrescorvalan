import re
from .especie_model import EspecieModel

#------------------------------------------------------------------------------------------------------------------------
# Clase EspecieController para la entidad Especie.
#------------------------------------------------------------------------------------------------------------------------
class EspecieController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas las Especies.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict] | None:
        return EspecieModel.get_all()
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        return EspecieModel.get_one(id)
    #--------------------------------------------------------------------------------------------------------
    # Método estático para verificar la integridad y formato de los datos.
    # Retorna: - {} si los datos son correctos.
    #          - dict con el error si los datos son incorrectos o incompletos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def verificar_data(data: dict) -> dict:
        # Verificar existencia y que el valor no sea None ni "".
        for campo in ['nombre', 'nombre_cientifico', 'clase']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Especie: Falta el campo obligatorio: {campo}.'
                }    
        return {} # Datos correctos.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear una Especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict | None:
        # Verficar data.
        error = EspecieController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        
        data_create = data.copy()
        data_create['id'] = 0
        
        especie = EspecieModel.deserializar(data_create)
        
        result = especie.create()
        if result is True: 
            return {
                'estado': 'ok', 
                'mensaje': 'Especie: Creación exitosa',
                'objeto': especie.serializar()
            }
        if result is False:
            return {
                'estado': 'error', 
                'mensaje': 'Especie: Error al intentar crear (verifique unicidad).'
            }
        return None # Excepción al intentar insertar en la BD.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para actualizar una Especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict | None:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'Especie: El ID es inválido o no fue enviado.'
            }
        # Verificar data.
        error = EspecieController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.

        especie = EspecieModel.deserializar(data)

        result = especie.update()
        if result is None:
            return None # Excepción al intentar actualizar en la BD.
        
        if result is True:
            return {
                'estado': 'ok', 
                'mensaje': 'Especie: Actualización exitosa.',
                'objeto': especie.serializar()
            }
        
        # Si la ejecucion llega aqui es porque result == False: UPDATE no afectó filas por:
        # a) no existe el registro.
        # b) no hubo cambios.
        reg = EspecieModel.get_one(data['id'])
        if reg == {}:   # no existe.
            return {
                'estado': 'not_found',
                'mensaje': 'Especie: No existe el registro que se quiere actualizar.'
            }
        #else: no se cambio nada.
        return {
            'estado': 'ok',
            'mensaje': 'Especie: No hubo cambios (los datos enviados son iguales a los existentes).'
        }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para eliminar una Especie.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict | None:
        result = EspecieModel.delete(id)
        if result is True:
            return {
                'estado': 'ok',
                'mensaje': 'Especie: Eliminación exitosa.'
            }
        if result is False:
            return {
                'estado': 'not_found',
                'mensaje': 'Especie: No existe el registro.'
            }
        return None # Excepción al intentar eliminar en la BD.