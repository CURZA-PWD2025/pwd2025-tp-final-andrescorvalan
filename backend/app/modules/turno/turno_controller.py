import datetime
from .turno_model import TurnoModel, ModelException
from ..mascota.mascota_model import MascotaModel
from ..veterinario.veterinario_model import VeterinarioModel
#corrregir mensajes


#------------------------------------------------------------------------------------------------------------------------
# Clase TurnoController para la entidad Turno.
#------------------------------------------------------------------------------------------------------------------------
class TurnoController:
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos los Turnos.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            turnos = TurnoModel.get_all()
            cantidad = len(turnos)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} turnos con éxito."
            else:
                msg = "No se encontraron turnos registrados."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': turnos
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Turno.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            turno = TurnoModel.get_one(id)
            if turno:
                return {
                    'estado': 'ok',
                    'datos': turno
                }
            else:
                return {
                    'estado': 'not_found',
                    'mensaje': f"No se encontro el turno con ID {id} en la base de datos."
                }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener los turnos futuros.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def proximos_turnos() -> dict:
        try:
            # hoy = datetime.datetime.now()
            turnos = TurnoModel.get_proximos()
            cantidad = len(turnos)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} turnos con éxito."
            else:
                msg = "No se encontraron turnos futuros."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': turnos
            }
        except ModelException as e:
            return {
                'estado': 'exception', 
                'mensaje': f'{str(e)}'
            }
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener los turnos pasados.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def historial_turnos() -> dict:
        try:
            # hoy = datetime.datetime.now()
            turnos = TurnoModel.get_historial()
            cantidad = len(turnos)
            if cantidad > 0:
                msg = f"Se obtuvieron {cantidad} turnos con éxito."
            else:
                msg = "No se encontraron turnos pasados."
            return {
                'estado': 'ok',
                'mensaje': msg,
                'datos': turnos
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
    def verificar_data(data: dict, es_nuevo: bool = True) -> dict:

        # Verificar existencia de la fecha-hora y el motivo.
        for campo in ['fecha_hora', 'motivo']:
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
       
        fecha_original = data["fecha_hora"]
        fecha_validar = fecha_original.replace('T', ' ')
        try:
            formato = "%Y-%m-%d %H:%M:%S" if len(fecha_validar) > 16 else "%Y-%m-%d %H:%M"
            fecha_turno = datetime.datetime.strptime(fecha_validar, formato)
        except ValueError:
            return {'estado': 'error', 'mensaje': 'La fecha o su formato tiene algún error.'}

        if es_nuevo and fecha_turno < datetime.datetime.now():
            return {
                'estado': 'error',
                'mensaje': 'No se puede asignar un turno en una fecha pasada.'
        }
    
        if 'estado' not in data or not data['estado']:
            data['estado'] = 'Pendiente'
        return {}
    #--------------------------------------------------------------------------------------------------------
    # Método estático para crear un Turno.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def create(data: dict) -> dict:
        # Verficar data.
        error = TurnoController.verificar_data(data)
        if error:
            return error # Devuelve el error de validación.
        try:
            turno = TurnoModel(
                id = 0,
                fecha_hora = data['fecha_hora'],
                motivo = data['motivo'],
                estado = data['estado'],
                mascota = MascotaModel(id = int(data['mascota_id'])),
                veterinario = VeterinarioModel(id = int(data['veterinario_id']))
            )
            if turno.create():
                data_completo = turno.serializar()
                data_completo["mascota"] = MascotaModel.get_one(turno.mascota.id)
                data_completo["veterinario"] = VeterinarioModel.get_one(turno.veterinario.id)
                return {
                    'estado': 'ok',
                    'mensaje': 'Turno creado con éxito.',
                    'objeto': data_completo
                }
            #else
            return {
                'estado': 'error', 
                'mensaje': 'No se pudo crear el nuevo turno. Intente más tarde.'
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
    # Método estático para actualizar un Turno.
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def update(data: dict) -> dict:
        # Validar el id (obligatorio para actualizar).
        if data.get('id') is None or not isinstance(data.get('id'), int) or data.get('id') <= 0:
            return {
                'estado': 'error', 
                'mensaje': 'El ID del turno es inválido o no fue enviado.'
            }
        # Verficar data.
        error = TurnoController.verificar_data(data,False)
        if error:
            return error # Devuelve el error de validación.
        # Actualizar
        try:
            turno = TurnoModel(
                id = data['id'],
                fecha_hora = data['fecha_hora'],
                motivo = data['motivo'],
                estado = data['estado'],
                mascota = MascotaModel(id = int(data['mascota_id'])),
                veterinario = VeterinarioModel(id = int(data['veterinario_id']))
            )
            if turno.update():
                data_completo = turno.serializar()
                data_completo["mascota"] = MascotaModel.get_one(turno.mascota.id)
                data_completo["veterinario"] = VeterinarioModel.get_one(turno.veterinario.id)
                return {
                    'estado': 'ok', 
                    'mensaje': 'Turno actualizado con éxito.',
                    'objeto': data_completo
                }
            # Si la ejecucion llega aqui es porque:
            # a) no existe el registro.
            # b) no hubo cambios.
            existe = TurnoModel.get_one(turno.id)
            if not existe:
                return {
                    'estado': 'not_found',
                    'mensaje': 'El turno ya no existe en la base de datos.'
                }
            return {
                'estado': 'ok', # Se trata como éxito para el usuario
                'mensaje': 'No se detectaron cambios, los datos están actualizados.',
                'objeto': turno.serializar()
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
    # Método estático para eliminar un Turno.
    #--------------------------------------------------------------------------------------------------------  
    @staticmethod
    def delete(id: int) -> dict:
        try:
            if TurnoModel.delete(id):
                return {
                    'estado': 'ok',
                    'mensaje': f'El turno con ID {id} ha sido eliminado con éxito.'
                }
            #else           
            return {
                'estado': 'not_found',
                'mensaje': f'El turno con ID {id} ya no existe en la base de datos.'
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