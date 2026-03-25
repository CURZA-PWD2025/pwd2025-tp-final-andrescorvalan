//Implementa la logica para el listado de entidades:
// -Configuracion de mensajes y estados.
// -Metodo para leer los registros de una entidad a travez de un getAll (de un store) que recibe
//  como parametro.
// - Metodo para elminar una entidad a travez de un delete (de un store) que recibe
//  como parametro.
import { ref } from 'vue'
import type { ApiRespuesta } from '@/interface/api_respuesta'

export function useListLogicGenerico() {
    const borrando = ref(false)     
    const mensaje = ref('')
    const estado = ref('')                      // cargaOk, cargaError, procesando, exito, error.
    const mostrarModal = ref(false)             // Determina si se muestra una ventana
                                                // emergente (eliminar).
    const idEliminar = ref<number | null>(null) // Id de la entidad a borrar.
    const identEliminar = ref('')
    //Metodo generico para obtener el listado de entidades.
    async function loadEntidades(
        getEntidades: () =>  Promise<ApiRespuesta>   // Metodo para obtener el listado de entidades.
    ){
        mensaje.value = ''
        estado.value = 'cargando'
        try{
            const respuesta = await getEntidades()
            mensaje.value = respuesta.mensaje
            estado.value = 'cargaOk'
            setTimeout(() => {
                mensaje.value = '';
                estado.value = '';
            }, 2000);
        } catch (error: any) {
            mensaje.value = error.mensaje || 'Error al cargar datos.'
            estado.value = 'cargaError'
        }
    }
    const prepararEliminar = (id: number, identifEntidad: string) => {
        idEliminar.value = id
        mostrarModal.value = true;
        identEliminar.value = identifEntidad
    }
    //Metodo generico para borrar una entidad.
    async function delEntidad(
        id: number,                                      // Id de la entidad a eliminar.
        delMethod: (id: number) => Promise<ApiRespuesta> // Metodo para eliminar una entidad.
    ){
        borrando.value = true
        mensaje.value = `Intentando eliminar ${identEliminar.value}.`
        mostrarModal.value = true
        try {  
            const respuesta = await delMethod(id)
            mensaje.value = respuesta.mensaje || `¡Éxito! Se ha eliminado el registro (su ID es ${id}).`
            estado.value = 'exito'
        } catch (error: any) {
            mensaje.value =  error.mensaje || `No se pudo eliminar el registro (su ID es ${id}).`
            estado.value = 'error'
        } finally {
            borrando.value = false
            idEliminar.value = null
        }
    }
    //Metodo para reset la logica del listado,
    //al cerrar la ventana de eliminar se deben limpiar las variables.
    function resetListLogicGenerico() {
        mostrarModal.value = false
        mensaje.value = ''
        estado.value = ''
        idEliminar.value = null
        borrando.value = false
    }
    
    return { 
        mensaje, estado, mostrarModal, idEliminar, identEliminar, borrando,
        loadEntidades, prepararEliminar, delEntidad, resetListLogicGenerico 
    }
}