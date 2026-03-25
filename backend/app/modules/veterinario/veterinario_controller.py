import re
from .veterinario_model  import VeterinarioModel, ModelException
from ..especialidad.especialidad_model import EspecialidadModel

#------------------------------------------------------------------------------------------------------------------------
# Clase VeterinarioController para la entidad Veterinario (Dueño de la mascota)
#------------------------------------------------------------------------------------------------------------------------
class VeterinarioController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos los Veterinarios
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            veterinarios = VeterinarioModel.get_all()
            cantidad = len(veterinarios)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} veterinarios con éxito."
            else:
                msg = "No se encontraron veterinarios registrados."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': veterinarios
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Veterinario
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            veterinario = VeterinarioModel.get_one(id)
            if veterinario:
                return {
                    'estado': 'ok',
                    'datos': veterinario
                }
            else:
                return {
                    'estado': 'not_found',
                    'mensaje': f"No se encontro el veterinario con ID {id} en la base de datos."
                }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            } 
    #--------------------------------------------------------------------------------------------------------
    # Método estático para verificar la integridad y formato de los datos de entrada
    # Retorna: - {} si los datos son correctos
    #          - dict con el error si los datos son incorrectos o incompletos
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def verificar_data(data: dict) -> dict:
        # Verificar existencia y que el valor no sea None ni ""
        for campo in ['nombre', 'apellido', 'matricula']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Falta el campo obligatorio: {campo}.'
                }      
        # Validar el teléfono (todos números).
        if data['telefono'] and not re.match(r'^[0-9]+$', data['telefono']):
            return {
                'estado': 'error', 
                'mensaje': 'El teléfono debe contener solo dígitos.'
            }
        # Validar básicamente el Email: string@string.string.
        if data['email'] and not re.match(r'^.+@.+\..+$', data['email']):
             return {
                 'estado': 'error', 
                 'mensaje': 'El formato del email es inválido (debe ser: usuario@dominio.com).'
            }
        return {}  # Datos correctos.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear un Veterinario
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict:
        # Verficar data.
        error = VeterinarioController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        try:
            lista_esp = []
            ids_recibidos = data.get('especialidades', [])
            
            for esp_id in ids_recibidos:
                esp_dict = EspecialidadModel.get_one(esp_id)
                if esp_dict: 
                    objeto_esp = EspecialidadModel.deserializar(esp_dict)
                    lista_esp.append(objeto_esp)

            veterinario = VeterinarioModel(
                nombre=data['nombre'],
                apellido=data['apellido'],
                matricula=data['matricula'],
                telefono=data['telefono'],
                email=data['email'],
                especialidades=lista_esp
            )
            if veterinario.create(): 
                return {
                    'estado': 'ok', 
                    'mensaje': 'Veterinario creado con exito.',
                    'objeto': veterinario.serializar()
                }
            #else
            return {
                'estado': 'error', 
                'mensaje': 'No se puedo crear el nuevo veterinario. Intente mas tarde.'
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
    # Método estático para actualizar un Veterinario
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'El ID del veterinario es inválido o no fue enviado.'
            }
        # Verificar data
        error = VeterinarioController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        
        try:
            lista_esp = []
            ids_recibidos = data.get('especialidades', [])
            
            for esp_id in ids_recibidos:
                esp_dict = EspecialidadModel.get_one(esp_id)
                if esp_dict: 
                    objeto_esp = EspecialidadModel.deserializar(esp_dict)
                    lista_esp.append(objeto_esp)

            veterinario = VeterinarioModel(
                id=data['id'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                matricula=data['matricula'],
                telefono=data['telefono'],
                email=data['email'],
                especialidades=lista_esp
            )
            if veterinario.update():
                return { 
                    'estado': 'ok', 
                    'mensaje': 'Veterinario actualizado con exito.',
                    'objeto': veterinario.serializar()
                }
            # Si la ejecucion llega aqui es porque:
            # a) no existe el registro.
            # b) no hubo cambios.
            existe = VeterinarioModel.get_one(veterinario.id)
            if not existe:
                return {
                    'estado': 'not_found',
                    'mensaje': 'El veterinario ya no existe en la base de datos.'
                }
            return {
                'estado': 'ok', # Se trata como éxito para el usuario
                'mensaje': 'No se detectaron cambios, los datos están actualizados.',
                'objeto': veterinario.serializar()
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
    # Método estático para eliminar un Veterinario
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict:
        try:
            if VeterinarioModel.delete(id):
                return {
                    'estado': 'ok',
                    'mensaje': f'El veterinario con ID {id} ha sido eliminado con exito.'
                }
            #else           
            return {
                'estado': 'not_found',
                'mensaje': f'El veterinario con ID {id} ya no existe en la base de datos.'
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