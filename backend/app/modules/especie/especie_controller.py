from .especie_model import EspecieModel, ModelException

#------------------------------------------------------------------------------------------------------------------------
# Clase EspecieController para la entidad Especie.
#------------------------------------------------------------------------------------------------------------------------
class EspecieController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas las Especies.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            especies = EspecieModel.get_all()
            cantidad = len(especies)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} especies con éxito."
            else:
                msg = "No se encontraron especies registradas."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': especies
            }
        except ModelException as e:
            return {
                'estado': 'exception',
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        try:
            especie = EspecieModel.get_one(id)
            if especie:
                return {
                    'estado': 'ok',
                    'datos': especie
                }
            else:
                return {
                    'estado': 'not_found',
                    'mensaje': f"No se encontro la especie con ID {id} en la base de datos."
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
        for campo in ['nombre', 'nombre_cientifico', 'clase']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Falta el campo obligatorio: {campo}.'
                }        
        for campo in ['esperanza_vida', 'exotica']:
            if campo not in data or data[campo] is None:
                return {
                    'estado': 'error', 
                    'mensaje': f'Falta el campo obligatorio: {campo}.'
                }
            # Verificar que son numeros
            try:
                int(data[campo])
            except (ValueError, TypeError):
                return {
                    'estado': 'error', 
                    'mensaje': f'El campo {campo} debe ser un valor numérico.'
                }
        return {} # Datos correctos.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear una Especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict:
        # Verficar data.
        error = EspecieController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        try:
            especie = EspecieModel.deserializar(data)
            especie.id = 0
            if especie.create(): 
                return {
                    'estado': 'ok', 
                    'mensaje': 'Especie creada con éxito.',
                    'objeto': especie.serializar()
                }
            #else
            return {
                'estado': 'error', 
                'mensaje': 'No se pudo crear la nueva especie en la base de datos. Intente más tarde.'
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
    # Método estático para actualizar una Especie.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'El ID de la especie es inválido o no fue enviado.'
            }
        # Verificar data
        error = EspecieController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.

        especie = EspecieModel.deserializar(data)
        try:
            if especie.update():
                return { 
                    'estado': 'ok', 
                    'mensaje': 'Especie actualizada con éxito.',
                    'objeto': especie.serializar()
                }
            # Si la ejecucion llega aqui es porque:
            # a) no existe el registro.
            # b) no hubo cambios.
            existe = EspecieModel.get_one(especie.id)
            if not existe:
                return {
                    'estado': 'not_found',
                    'mensaje': 'La especie ya no existe en la base de datos.'
                }
            return {
                'estado': 'ok', # Se trata como éxito para el usuario
                'mensaje': 'No se detectaron cambios, los datos están actualizados.',
                'objeto': especie.serializar()
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
    # Método estático para eliminar una Especie.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict:
        try:
            if EspecieModel.delete(id):
                return {
                    'estado': 'ok',
                    'mensaje': f'La especie con ID {id} ha sido eliminada con éxito.'
                }
            #else           
            return {
                'estado': 'not_found',
                'mensaje': f'La especie con ID {id} ya no existe en la base de datos.'
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