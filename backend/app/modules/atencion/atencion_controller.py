import datetime
from .atencion_model import AtencionModel, ModelException
from ..mascota.mascota_model import MascotaModel
from ..veterinario.veterinario_model import VeterinarioModel

#------------------------------------------------------------------------------------------------------------------------
# Clase AtencionController para la entidad Atención.
#------------------------------------------------------------------------------------------------------------------------
class AtencionController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todas las Atenciones.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            atenciones = AtencionModel.get_all()
            cantidad = len(atenciones)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} atenciones con éxito."
            else:
                msg = "No se encontraron atenciones registrados."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': atenciones
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener una Atención.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            atencion = AtencionModel.get_one(id)
            if atencion:
                return {
                    'estado': 'ok',
                    'datos': atencion
                }
            else:
                return {
                    'estado': 'not_found',
                    'mensaje': f"No se encontro la atención con ID {id} en la base de datos."
                }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener el historial clinico de una mascota especifica.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_by_mascota(mascota_id: int) -> dict:
        try:
            historial = AtencionModel.get_by_mascota(mascota_id)
            return {
                'estado': 'ok',
                'datos': historial
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'No se pudo obtener el historial: {str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Métodos estático para verificar la integridad y formato de los datos.
    # Retorna: - {} si los datos son correctos.
    #          - dict con el error si los datos son incorrectos o incompletos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def verificar_data(data: dict) -> dict:
        # Verificar existencia de la fecha de nacimiento.
        for campo in ['fecha', 'diagnostico', 'tratamiento']:
            if campo not in data or data[campo] is None or not str(data[campo]).strip():
                return {
                    'estado': 'error', 
                    'mensaje': f'Falta el campo obligatorio: {campo}.'
                }
        # Verificar mascota_id y veterinario_id.
        for campo in ['mascota_id', 'veterinario_id']:
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
            datetime.datetime.strptime(data["fecha"], "%Y-%m-%d")
        except ValueError:
            return {
                'estado': 'error',
                'mensaje': 'La fecha no es válida o tiene un formato incorrecto.'
            }
        return {}

    @staticmethod
    def create(data: dict) -> dict:
        # Verficar data.
        error = AtencionController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        try:
            atencion = AtencionModel(
                id = 0,
                fecha = data['fecha'],
                diagnostico = data['diagnostico'],
                tratamiento = data['tratamiento'],
                observaciones = str(data.get('observaciones', '')).strip(),
                mascota = MascotaModel(id = int(data['mascota_id'])),
                veterinario = VeterinarioModel(id = int(data['veterinario_id']))
            )
            if atencion.create():
                data_completo = atencion.serializar()
                data_completo["mascota"] = MascotaModel.get_one(atencion.mascota.id)
                data_completo["veterinario"] = VeterinarioModel.get_one(atencion.veterinario.id)
                return {
                    'estado': 'ok',
                    'mensaje': 'Atención creada con éxito.',
                    'objeto': data_completo
                }
            #else
            return {
                'estado': 'error', 
                'mensaje': 'No se pudo crear la nueva atención. Intente más tarde.'
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
                'mensaje': 'El ID de la atención es inválido o no fue enviado.'
            }
        # Verficar data.
        error = AtencionController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        # Actualizar
        try:
            atencion = AtencionModel(
                id = data['id'],
                fecha = data['fecha'],
                diagnostico = data['diagnostico'],
                tratamiento = data['tratamiento'],
                observaciones = str(data.get('observaciones', '')).strip(),
                mascota = MascotaModel(id = int(data['mascota_id'])),
                veterinario = VeterinarioModel(id = int(data['veterinario_id']))
            )
            if atencion.update():
                data_completo = atencion.serializar()
                data_completo["mascota"] = MascotaModel.get_one(atencion.mascota.id)
                data_completo["veterinario"] = VeterinarioModel.get_one(atencion.veterinario.id)
                return {
                    'estado': 'ok', 
                    'mensaje': 'Atención actualizada con éxito.',
                    'objeto': data_completo
                }
            # Si la ejecucion llega aqui es porque:
            # a) no existe el registro.
            # b) no hubo cambios.
            existe = AtencionModel.get_one(atencion.id)
            if not existe:
                return {
                    'estado': 'not_found',
                    'mensaje': 'La atención ya no existe en la base de datos.'
                }
            return {
                'estado': 'ok', # Se trata como éxito para el usuario
                'mensaje': 'No se detectaron cambios, los datos están actualizados.',
                'objeto': atencion.serializar()
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
            if AtencionModel.delete(id):
                return {
                    'estado': 'ok',
                    'mensaje': f'La atención con ID {id} ha sido eliminada con éxito.'
                }
            #else           
            return {
                'estado': 'not_found',
                'mensaje': f'La atención con ID {id} ya no existe en la base de datos.'
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