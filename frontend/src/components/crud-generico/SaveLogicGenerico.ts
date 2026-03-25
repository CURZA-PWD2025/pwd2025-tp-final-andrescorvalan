//Implementa la logica para los formularios Create y Update, para:
// -La configuracion de mensajes, estado, ventana emergente.
// -Metodo para grabar una entidad.
// -Metodo para buscar una entidad a editar.
// -Los metodos para crear/actualizar y buscar se reciben por parametros 
//  (metodos de un stre especifico).
import { ref } from 'vue'
import type { ApiRespuesta } from '@/interface/api_respuesta'

export function useSaveLogicGenerico() {
    const mensaje = ref('')
    const estado = ref('')          // 'exito', 'error', 'procesando'.
    const mostrarModal = ref(false) // Determina si se muestra una ventana emergente (eliminar).

    //Metodo generico para grabar la entidad.
    async function saveEntidad(
        saveMethod: () => Promise<ApiRespuesta>  // Metodo para grabar la entidades.
    ) {
        estado.value = 'procesando'
        mensaje.value = 'Procesando solicitud...'
        try {
            const respuesta = await saveMethod()
            mensaje.value = respuesta.mensaje
            if (respuesta.estado === 'not_found') {
                estado.value = 'error'
            } else {
                estado.value = 'exito'
            }
        } catch (error: any) {
            mensaje.value = error.mensaje || 'Ocurrió un error inesperado.'
            estado.value = 'error'
        } finally {
            mostrarModal.value = true
        }
    }
    //Metodo generico para buscar una entidad.
    async function findEntidad(
        id: number,                                       // Id de la entidad a buscar.
        findMethod: (id: number) => Promise<ApiRespuesta> // Metodo para buscar la entidad.
    ){
        if (isNaN(id) || id <= 0) {
            mensaje.value = 'ID no válido.'
            estado.value = 'error'
            return null
        }
        try {
            estado.value = 'procesando'
            mensaje.value = 'Cargando datos...'
            const entidad = await findMethod(id)
            estado.value = ''
            return entidad.objeto
        } catch (error) {
            mensaje.value = 'No se pudo cargar el registro.'
            estado.value = 'error'
            mostrarModal.value = true
            return null
        }
    }
    //Metodo para reset la logica de grabado (limpiar las variables y volver la ventana original).
    function resetSaveLogicGenerico() {
        mostrarModal.value = false
        mensaje.value = ''
        estado.value = ''
    }

    return { 
        mensaje, estado, mostrarModal, 
        saveEntidad, findEntidad, resetSaveLogicGenerico 
    }
}