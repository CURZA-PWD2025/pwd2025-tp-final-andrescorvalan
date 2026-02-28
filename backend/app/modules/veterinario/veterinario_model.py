from ...database.accesoBD import OperarBD
from ...database.accesoBD import TransaccionBD
from ..especialidad.especialidad_model import EspecialidadModel

#------------------------------------------------------------------------------------------------------------------------
# Clase Modelo para la entidad Veterinario
#------------------------------------------------------------------------------------------------------------------------

class VeterinarioModel:
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
    def get_all() -> list[dict] | None:
        veterinarios_bd = OperarBD.obtenerReg(
            "SELECT * "
            "FROM VETERINARIOS"
        )
        if veterinarios_bd is None:
            return None
        
        listado = []
        for veterinario_data in veterinarios_bd:
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
    #--------------------------------------------------------------------------------------------------------
    # Método estático para obtener un Veterinario por Id
    # Retorna:  - un diccionario con los datos si encontró el registro
    #           - {} si no encontró el registro
    #           - None si hubo una excepción
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_one(id: int) -> dict | None:
        registros = OperarBD.obtenerReg(
            "SELECT * "
            "FROM VETERINARIOS "
            "WHERE id=%s",
            (id,)
        )
        if registros is None:
            return None
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
    #--------------------------------------------------------------------------------------------------------
    # Método para crear un Veterinario
    # Retorna: - True si se inserto correctamente
    #          - False si no se pudo insertar
    #          - None si hubo una excepción
    #--------------------------------------------------------------------------------------------------------
    def create(self) -> bool | None:
        #se usa una transaccion porque se deben realizar varias escrituras (todas o ninguna)
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()
            #Insertar veterinario
            resultado_vet = transaccion.operacionBD(
                "INSERT "
                "INTO VETERINARIOS (nombre, apellido, matricula, telefono, email) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.nombre, self.apellido, self.matricula, self.telefono, self.email)
            )
            if resultado_vet is None or resultado_vet == 0:
                transaccion.revertir_transaccion()
                return False
            
            self.id = transaccion.get_nuevo_id()
            #Insertar las especialidades del veterinario
            for una_esp in self.especialidades:
                resultado_esp = transaccion.operacionBD(
                    "INSERT "
                    "INTO VETERINARIO_ESPECIALIDAD (veterinario_id, especialidad_id) "
                    "VALUES (%s, %s)",
                    (self.id, una_esp.id))
                if resultado_esp is None:
                    transaccion.revertir_transaccion()
                    return False
            
            #Se inserto correctamente
            transaccion.confirmar_transaccion()
            return True
        except Exception as err:
            if transaccion:
                transaccion.revertir_transaccion()
            #print(f"Error al crear el artículo: {err}")
            return None
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()
    #--------------------------------------------------------------------------------------------------------
    # Método para modificar un Veterinario
    # Retorna: - True si se modificó correctamente (puede ser 0 si no hubo cambios)
    #          - None si hubo una excepción
    #--------------------------------------------------------------------------------------------------------
    def update(self) -> bool | None:       
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()
            #actualizar el veterinario
            resultado_vet = transaccion.operacionBD(
                "UPDATE VETERINARIOS "
                "SET nombre=%s, apellido=%s, matricula=%s, telefono=%s, email=%s "
                "WHERE id=%s",
                (self.nombre, self.apellido, self.matricula, self.telefono, self.email, self.id,)
            )
            if resultado_vet is None:
                transaccion.revertir_transaccion()
                return False

            #Eliminar las especialidades anteriores
            resultado_del = transaccion.operacionBD(
                "DELETE "
                "FROM VETERINARIO_ESPECIALIDAD "
                "WHERE veterinario_id=%s",
                (self.id,)
            )
            if resultado_del is None:
                transaccion.revertir_transaccion()
                return False

            #Agregar las especialidades
            for una_esp in self.especialidades:
                resultado_ins = transaccion.operacionBD(
                    "INSERT "
                    "INTO VETERINARIO_ESPECIALIDAD (veterinario_id, especialidad_id) "
                    "VALUES (%s, %s)",
                    (self.id, una_esp.id)
                )
                if resultado_ins is None:
                    transaccion.revertir_transaccion()
                    return False 
           
            #Se actualizo
            transaccion.confirmar_transaccion()
            return True 
               
        except Exception as err:
            if transaccion:
                transaccion.revertir_transaccion()
            print(f"Error al actualizar el veterinario: {err}")
            return None
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()
    #--------------------------------------------------------------------------------------------------------
    # Método para eliminar un Veterinario
    #--------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete(id: int) -> bool | None:
        transaccion = None
        try:
            transaccion = TransaccionBD()
            transaccion.iniciar_transaccion()

            resultado_esp = transaccion.operacionBD(
                "DELETE "
                "FROM VETERINARIO_ESPECIALIDAD "
                "WHERE veterinario_id=%s",
                (id,)
            )
            if resultado_esp is None:
                #print(f"DEBUG: Fallo al borrar relacion VETERINARIO_ESPECIALIDAD. rowcount era 0 o menos.")
                transaccion.revertir_transaccion()
                return False 

            resultado_vet = transaccion.operacionBD(
                "DELETE "
                "FROM VETERINARIOS "
                "WHERE id=%s",
                (id,)
            )
            if not resultado_vet:
                #print(f"DEBUG: Fallo al borrar de VETERINARIOS. rowcount era 0 o menos.")
                transaccion.revertir_transaccion()
                return False 
            
            #Se borro
            transaccion.confirmar_transaccion()
            return True
        except Exception as err:
            if transaccion:
                transaccion.revertir_transaccion()
            #print(f"Error/Exception al eliminar veterinario: {err}")
            return None
        finally:
            if transaccion:
                transaccion.finalizar_transaccion()