from .especialidad_model import EspecialidadModel, ModelException

#------------------------------------------------------------------------------------------------------------------------
# Clase EspecialidadController para la entidad Especialidad.
#------------------------------------------------------------------------------------------------------------------------
class EspecialidadController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas las Especialidades.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            especialidades = EspecialidadModel.get_all()
            cantidad = len(especialidades)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} especialidades con éxito."
            else:
                msg = "No se encontraron especialidades registradas."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': especialidades
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }  
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            especialidad = EspecialidadModel.get_one(id)
            if especialidad:
                return {
                    'estado': 'ok',
                    'datos': especialidad
                }
            else:
                return {
                    'estado': 'not_found',
                    'mensaje': f"No se encontro la especialidad con ID {id} en la base de datos."
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
        for campo in ['nombre', 'descripcion']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Falta el campo obligatorio: {campo}.'
                }
        for campo in ['activa']:
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
    # Método estático para crear una Especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict:
        # Verficar data.
        error = EspecialidadController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        try:
            especialidad = EspecialidadModel.deserializar(data)
            especialidad.id = 0
            if especialidad.create(): 
                return {
                    'estado': 'ok', 
                    'mensaje': 'Especialidad creada con éxito.',
                    'objeto': especialidad.serializar()
                }
            #else
            return {
                'estado': 'error', 
                'mensaje': 'No se pudo crear la nueva especialidad en la base de datos. Intente más tarde.'
            }
        except ValueError as e: 
            return {
                'estado': 'error',
                'mensaje': f'{str(e)} Verifique los datos e intente más tarde.'
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}.'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para actualizar una Especialidad.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'El ID de la especialidad es inválido o no fue enviado.'
            }
        # Verificar data
        error = EspecialidadController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.

        especialidad = EspecialidadModel.deserializar(data)
        try:
            if especialidad.update():
                return { 
                    'estado': 'ok', 
                    'mensaje': 'Especialidad actualizada con éxito.',
                    'objeto': especialidad.serializar()
                }
            # Si la ejecucion llega aqui es porque:
            # a) no existe el registro.
            # b) no hubo cambios.
            existe = EspecialidadModel.get_one(especialidad.id)
            if not existe:
                return {
                    'estado': 'not_found',
                    'mensaje': 'La especialidad ya no existe en la base de datos.'
                }
            return {
                'estado': 'ok', # Se trata como éxito para el usuario
                'mensaje': 'No se detectaron cambios, los datos están actualizados.',
                'objeto': especialidad.serializar()
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
    # Método estático para eliminar una Especialidad.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict:
        try:
            if EspecialidadModel.delete(id):
                return {
                    'estado': 'ok',
                    'mensaje': f'La especialidad con ID {id} ha sido eliminada con éxito.'
                }
            #else           
            return {
                'estado': 'not_found',
                'mensaje': f'La especialidad con ID {id} ya no existe en la base de datos.'
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