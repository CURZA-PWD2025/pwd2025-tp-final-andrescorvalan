<script setup lang="ts">
import { onMounted, ref, toRefs } from 'vue'

const props = defineProps<{ mascotaId: number }>()
import useAtencionesStore from '@/stores/atenciones_store'

const { atenciones } = toRefs(useAtencionesStore())
const { getByMascota } = useAtencionesStore()
const estado=ref('')
const mensaje=ref('')

onMounted(async () => {
  mensaje.value = 'Obteniendo el listado ...'
  estado.value = 'cargando'
  try {
    await getByMascota(props.mascotaId)
    mensaje.value = 'Consulta exitosa ...'
    estado.value = 'exito'

    setTimeout(() => {
        mensaje.value = '';
        estado.value = '';
     }, 3000);
  } catch (error: any) {
    mensaje.value = error.mensaje || 'Error al cargar datos.'
    estado.value = 'errorCargando'
  }
})


const formatearFecha = (fechaStr: string) => {
  const date = new Date(fechaStr + 'T00:00:00')
  return date.toLocaleDateString('es-AR', {day: '2-digit', month: '2-digit', year: 'numeric'});
};
</script>

<template>
  <div>    
    <div v-if="estado==='cargando'">Cargando historial...</div>
  
    <div  v-else-if="atenciones.length > 0">        
      <article class="crud-list-item" v-for="atencion in atenciones" :key="atencion.id">
        <dl class="crud-field-name">Fecha:
          <span class="crud-data"> {{ formatearFecha(atencion.fecha) }}</span>
        </dl>
        <dl class="crud-field-name">Veterinario:
          <span class="crud-data">{{ atencion.veterinario.apellido }}, {{ atencion.veterinario.nombre }}</span>
        </dl>
        <dl class="crud-field-name">Diagnóstico:
          <span class="crud-data">{{ atencion.diagnostico }}</span>
        </dl>
        <dl class="crud-field-name">Tratamiento:
          <span class="crud-data">{{ atencion.tratamiento }}</span>
        </dl>
        <dl class="crud-field-name">Observaciones:
          <span class="crud-data">{{ atencion.observaciones }}</span>
        </dl>
      </article>
    </div>

    <p v-else>
      No hay atenciones registradas para esta mascota.</p> 
  </div>
</template>