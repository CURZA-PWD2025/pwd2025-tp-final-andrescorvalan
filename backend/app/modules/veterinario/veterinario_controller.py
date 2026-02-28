import re
from .veterinario_model import VeterinarioModel
from ..especialidad.especialidad_model import EspecialidadModel

#------------------------------------------------------------------------------------------------------------------------
# Clase VeterinarioController para la entidad Veterinario (Dueño de la mascota)
#------------------------------------------------------------------------------------------------------------------------
class VeterinarioController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos los Veterinarios
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict] | None:
        return VeterinarioModel.get_all()
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Veterinario
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        return VeterinarioModel.get_one(id)
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
                    'mensaje': f'Veterinario: Falta el campo obligatorio: {campo}.'
                }      
        # Validar el teléfono (todos números).
        if data['telefono'] and not re.match(r'^[0-9]+$', data['telefono']):
            return {
                'estado': 'error', 
                'mensaje': 'Veterinario: El teléfono debe contener solo dígitos.'
            }
        # Validar básicamente el Email: string@string.string.
        if data['email'] and not re.match(r'^.+@.+\..+$', data['email']):
             return {
                 'estado': 'error', 
                 'mensaje': 'Veterinario: El formato del email es inválido (debe ser: usuario@dominio.com).'
            }
        return {}  # Datos correctos.
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear un Veterinario
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict | None:
        # Verficar data
        error = VeterinarioController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación
                
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
        print(veterinario.serializar())   
        result = veterinario.create()
        if result == True: 
            return {
                'estado': 'ok', 
                'mensaje': 'Veterinario: Creación exitosa',
                'objeto': veterinario.serializar()
            }
        if result == False:
            return {
                'estado': 'error', 
                'mensaje': 'Veterinario: Error al intentar crear (verifique unicidad).'
            }
        return None # Excepción al intentar insertar en la BD
    #--------------------------------------------------------------------------------------------------------
    # Método estático para actualizar un Veterinario
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict | None:
        # Validar el id (obligatorio para actualizar)
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'Veterinario: El ID es inválido o no fue enviado.'
            }
        # Verificar data
        error = VeterinarioController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación

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

        result = veterinario.update()
        if result == None:
            return None # Excepción al intentar actualizar en la BD
        
        if result == True:
            return {
                'estado': 'ok', 
                'mensaje': 'Veterinario: Actualización exitosa.',
                'objeto': veterinario.serializar()
            }
        
        # Si la ejecucion llega aqui es porque result == False: UPDATE no afectó filas por:
        # a) no existe el registro.
        # b) no hubo cambios.
        reg = VeterinarioModel.get_one(data['id'])
        if reg == {}:   # no existe
            return {
                'estado': 'not_found',
                'mensaje': 'Veterinario: No existe el registro que se quiere actualizar.'
            }
        #else: no se cambio nada
        return {
            'estado': 'ok',
            'mensaje': 'Veterinario: No hubo cambios (los datos enviados son iguales a los existentes).'
        }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para eliminar un Veterinario
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict | None:
        result = VeterinarioModel.delete(id)
        if result == True:
            return {
                'estado': 'ok',
                'mensaje': 'Veterinario: Eliminación exitosa.'
            }
        if result==False:
            return {
                'estado': 'not_found',
                'mensaje': 'Veterinario: No existe el registro.'
            }
        return None # Excepción al intentar eliminar en la BD