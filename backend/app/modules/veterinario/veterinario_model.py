from ...database.accesoBD import OperarBD
from ...database.erroresBD import DBErrorData, DBException

from ...database.accesoBD import TransaccionBD
from ..especialidad.especialidad_model import EspecialidadModel

class ModelException(Exception):
    # Errores ya procesados por el Model.
    # Se pueden enviar al frontend.
    pass

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Veterinario
#------------------------------------------------------------------------------------------------------------------------

class VeterinarioModel:
    PREFIX = 'Base de Datos (Veterinario): '
    #--------------------------------------------------------------------------------------------------------
    # Constructor
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, id: int=0, nombre: str="", apellido: str="", matricula: str="",
                 telefono: str="", email: str="", especialidades: list[EspecialidadModel] = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula
        self.telefono = telefono
        self.email = email
        self.especialidades = especialidades if especialidades is not None else []
    #--------------------------------------------------------------------------------------------------------
    # Métodos de serialización y deserialización
    #--------------------------------------------------------------------------------------------------------
    def serializar(self) -> dict:
        return {
            "id" : self.id,
            "nombre" : self.nombre,
            "apellido" : self.apellido,
            "matricula" : self.matricula,
            "telefono" : self.telefono,
            "email" : self.email,
            "especialidades" : [esp.serializar() for esp in self.especialidades]
        }
    @staticmethod
    def deserializar(data: dict) -> 'VeterinarioModel':        
        return VeterinarioModel(
            id = data.get('id', 0),
            nombre = data.get('nombre', ""),
            apellido= data.get('apellido', ""),
            matricula = data.get('matricula', ""),
            telefono = data.get('telefono', ""),
            email = data.get('email', ""),
            especialidades = [EspecialidadModel.deserializar(esp) for esp in data.get("especialidades", [])]
        )
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener todos los Veterinarios
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all() -> list[dict]:
        try:
            registros_vet = OperarBD.obtenerReg(
                "SELECT id, nombre, apellido, matricula, telefono, email "
                "FROM VETERINARIOS"
            )
            listado = []
            for veterinario_data in registros_vet:
                registros_esp = OperarBD.obtenerReg(
                    "SELECT especialidad_id "
                    "FROM VETERINARIO_ESPECIALIDAD "
                    "WHERE veterinario_id=%s",
                    (veterinario_data['id'],)
                ) or []
                especialidades = []
                for reg in registros_esp:
                    esp = EspecialidadModel.get_one(reg['especialidad_id'])
                    if esp:
                        especialidades.append(esp)
                veterinario_data['especialidades'] = especialidades
                listado.append(veterinario_data)
            return listado
        except DBException:
            print(f"DEBUG - {VeterinarioModel.PREFIX} (get_all):")
            raise ModelException(
                "No se pudo obtener el listado de veterinarios. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )   
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Veterinario por Id
    # Retorna:  - un diccionario con los datos si encontró el registro
    #           - {} si no encontró el registro
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict:
        try:
            registros = OperarBD.obtenerReg(
                "SELECT id, nombre, apellido, matricula, telefono, email "
                "FROM VETERINARIOS "
                "WHERE id=%s",
                (id,)
            )
            if not registros:
                return {}
            veterinario_data = registros[0]
            registros_esp = OperarBD.obtenerReg(
                "SELECT especialidad_id "
                "FROM VETERINARIO_ESPECIALIDAD "
                "WHERE veterinario_id=%s",
                (id,)
            ) or []
            especialidades = []
            for reg in registros_esp:
                esp = EspecialidadModel.get_one(reg['especialidad_id'])
                if esp:
                    especialidades.append(esp)
            veterinario_data['especialidades'] = especialidades

            return veterinario_data
        except DBException:
            print(f"DEBUG - {VeterinarioModel.PREFIX} (get_one):")
            raise ModelException(
                "No se pudo obtener el veterinario. El Sistema " \
                "Gestor de Base de Datos esta fuera de servicio o la BD/Tabla no existe."
            )    
    #--------------------------------------------------------------------------------------------------------
    # Método para crear un Veterinario
    # Retorna: - True si se inserto correctamente
    #          - False si no se pudo insertar
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool:
        #se usa una transaccion porque se deben realizar varias escrituras (todas o ninguna)
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()
            #Insertar veterinario
            result_vet = transaccion.operacionBD(
                "INSERT "
                "INTO VETERINARIOS (nombre, apellido, matricula, telefono, email) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.nombre, self.apellido, self.matricula, self.telefono, self.email)
            )
            if result_vet > 0:
                self.id = transaccion.get_nuevo_id()
            else:
                transaccion.revertir_transaccion()
                return False 
            #Insertar las especialidades del veterinario
            for una_esp in self.especialidades:
                transaccion.operacionBD(
                    "INSERT "
                    "INTO VETERINARIO_ESPECIALIDAD (veterinario_id, especialidad_id) "
                    "VALUES (%s, %s)",
                    (self.id, una_esp.id)
                )
            #Se inserto correctamente
            transaccion.confirmar_transaccion()
            return True
        except DBErrorData as e:
            raise ValueError(f"No se pudo crear el veterinario: {e}")
        except DBException:
            print(f"DEBUG - {VeterinarioModel.PREFIX} (create):")
            raise ModelException('No se pudo crear el veterinario en la base de datos.')
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar un Veterinario
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios)
    #          - None si hubo una excepción
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool:       
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()
            #actualizar el veterinario
            transaccion.operacionBD(
                "UPDATE VETERINARIOS "
                "SET nombre=%s, apellido=%s, matricula=%s, telefono=%s, email=%s "
                "WHERE id=%s",
                (self.nombre, self.apellido, self.matricula, self.telefono, self.email, self.id)
            )
            #Eliminar las especialidades anteriores
            transaccion.operacionBD(
                "DELETE "
                "FROM VETERINARIO_ESPECIALIDAD "
                "WHERE veterinario_id=%s",
                (self.id,)
            )
            #Agregar las especialidades
            for una_esp in self.especialidades:
                transaccion.operacionBD(
                    "INSERT "
                    "INTO VETERINARIO_ESPECIALIDAD (veterinario_id, especialidad_id) "
                    "VALUES (%s, %s)",
                    (self.id, una_esp.id)
                )
            #Se actualizo
            transaccion.confirmar_transaccion()
            return True
        except DBErrorData as e:
            raise ValueError(f"No se pudo actualizar el veterinario: {e}")
        except DBException:
            print(f"DEBUG - {VeterinarioModel.PREFIX} (update):")
            raise ModelException('No se pudo actualizar el veterinario en la base de datos.')
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar un Veterinario
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool:
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()
            transaccion.operacionBD(
                "DELETE FROM VETERINARIO_ESPECIALIDAD WHERE veterinario_id=%s", (id,)
            )
            result = transaccion.operacionBD(
                "DELETE FROM VETERINARIOS WHERE id=%s", (id,)
            )        
            #Se borro
            transaccion.confirmar_transaccion()
            return result > 0
        except DBErrorData as e:
            raise ValueError(f"No se pudo eliminar el veterinario: {e}")
        except DBException:
            print(f"DEBUG - {VeterinarioModel.PREFIX} (delete):")
            raise ModelException('No se pudo eliminar el veterinario en la base de datos.')
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()