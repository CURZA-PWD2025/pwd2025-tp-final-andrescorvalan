<script setup lang="ts">
  import { onMounted, ref, toRefs, computed } from 'vue'
  
  import { useRoute, useRouter } from 'vue-router'
  const router = useRouter()
  const route = useRoute()

  import SaveFormGenerico from '@/components/crud-generico/SaveViewGenerico.vue'
  import { useSaveLogicGenerico } from '@/components/crud-generico/SaveLogicGenerico'
  const { mensaje, estado, mostrarModal, saveEntidad, findEntidad, resetSaveLogicGenerico } = useSaveLogicGenerico()

  import useTurnosStore from '@/stores/turnos_store'
  const { turnos_proximos } = toRefs(useTurnosStore())
  const { buscar_turno, update, getProximos, defaultTurno } = useTurnosStore()
  const editTurno = ref({ ...defaultTurno })

  import useVeterinariosStore from '@/stores/veterinarios_store'
  const { veterinarios } = toRefs(useVeterinariosStore())
  const { getAll: getall_veterinarios } = useVeterinariosStore()

  import useMascotasStore from '@/stores/mascotas_store'
  const { mascotas } = toRefs(useMascotasStore())
  const { getAll: getall_mascotas } = useMascotasStore()

  // Variables auxiliares para los selects y la grilla
  const idVeterinario = ref<number>(0)
  const idMascota = ref<number>(0)
  const seleccionTmp = ref<{fecha: string, hora: string} | null>(null)

  const horariosDisponibles = ['08:30','09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', 
                              '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00']

  const proximosDias = computed(() => {
    const dias = []
    for (let i = 0; i < 14; i++) {
      const d = new Date()
      d.setDate(d.getDate() + i)
      if (d.getDay() !== 0) { 
        const fechaLocal = d.toLocaleDateString('sv-SE')
        dias.push({
          valor: fechaLocal,
          formateada: d.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit' })
        })
      }
    }
    return dias
  })

  async function cargar_datos () {
    const id = Number(route.params.id)
    await Promise.all([getall_mascotas(), getall_veterinarios(), getProximos()])
    
    const datos = await findEntidad(id, buscar_turno)
    console.log('id a buscar:', id)
    console.log('buscar en:', turnos_proximos.value)
    console.log('resultado:', datos)
    if (datos) {
        editTurno.value = { ...datos }
        idMascota.value = datos.mascota.id
        idVeterinario.value = datos.veterinario.id
        console.log(idMascota.value, idVeterinario.value )
        
        // Parsear fecha para la grilla: "YYYY-MM-DDTHH:mm:ss" -> {fecha, hora}
        if (datos.fecha_hora) {
          const [fecha, tiempo] = datos.fecha_hora.split('T')
          const hora = tiempo.substring(0, 5)
          seleccionTmp.value = { fecha, hora }
        }
    }
  }

  onMounted(() => {
    cargar_datos()
  })

  const esHorarioOcupado = (fecha: string, hora: string) => {
    if (idVeterinario.value === 0) return false
    const busqueda = `${fecha}T${hora}`
    return turnos_proximos.value.some(t => 
      t.fecha_hora.includes(busqueda) && 
      t.veterinario.id === idVeterinario.value &&
      t.id !== editTurno.value.id // No bloquear el horario actual del propio turno
    )
  }

  function seleccionarBloque(fecha: string, hora: string) {
    seleccionTmp.value = { fecha, hora }
    editTurno.value.fecha_hora = `${fecha}T${hora}:00`
  }

  async function modificar_turno() {
    if (!idMascota.value || !idVeterinario.value || !seleccionTmp.value) {
      mensaje.value = 'Debe seleccionar veterinario, mascota y un horario.'
      estado.value = 'error' 
      return
    }
    editTurno.value.mascota.id = idMascota.value
    editTurno.value.veterinario.id = idVeterinario.value
    await saveEntidad(() => update(editTurno.value))
  }
</script>

<template>
  <SaveFormGenerico
    titulo="Modificar un Turno"
    :estado="estado" 
    :mensaje="mensaje" 
    :mostrarModal="mostrarModal"
    @volver="router.push({name: 'turnos_proximos'})"
    @submit="modificar_turno"
    @reset="cargar_datos"
    @cerrarModal="resetSaveLogicGenerico"
  >
    <div class="crud-field-group">
      <div class="crud-field">
        <label class="crud-field-name">Veterinario: <abbr>*</abbr></label>
        <select class="crud-input crud-data" v-model="idVeterinario" style="width: 30ch;">
          <option value="0" disabled>Seleccione profesional</option>
          <option v-for="v in veterinarios" :key="v.id" :value="v.id">
            {{ v.apellido }}, {{ v.nombre }}
          </option>
        </select>
      </div>
      <div class="crud-field">
        <label class="crud-field-name">Mascota: <abbr>*</abbr></label>
        <select class="crud-input crud-data" v-model="idMascota" style="width: 30ch;">
          <option value="0" disabled>Seleccione mascota</option>
          <option v-for="m in mascotas" :key="m.id" :value="m.id">
            {{ m.nombre }} ({{ m.propietario.apellido }})
          </option>
        </select>
      </div>
    </div>

    <div class="crud-field" style="width: 100%;">
      <label class="crud-field-name">Seleccione un horario disponible: <abbr>*</abbr></label>
      
      <div class="agenda-wrapper">
        <div v-for="dia in proximosDias" :key="dia.valor" class="agenda-columna">
          <div class="agenda-header">{{ dia.formateada }}</div>
          
          <div class="agenda-slots">
            <button 
              v-for="hora in horariosDisponibles" 
              :key="hora"
              type="button"
              class="boton-dia"
              :class="{ 
                'boton-dia-selected': seleccionTmp?.fecha === dia.valor && seleccionTmp?.hora === hora,
                'boton-dia-ocupado': esHorarioOcupado(dia.valor, hora) 
              }"
              :disabled="esHorarioOcupado(dia.valor, hora) || idVeterinario === 0"
              @click="seleccionarBloque(dia.valor, hora)"
            >
              {{ hora }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="crud-field">
      <label class="crud-field-name">Motivo de la consulta:</label>
      <textarea class="crud-input crud-data" v-model="editTurno.motivo" 
        rows="3" style="width: 100%; resize: none;" placeholder="Ej: Vacunación anual..."></textarea>
    </div>
  </SaveFormGenerico>
</template>

<style scoped>
  .agenda-wrapper {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 10px 0;
    border: 1px solid #ccc;
    border-radius: 4px;
    background: #f9f9f9;
  }

  .agenda-columna {
    display: flex;
    flex-direction: column;
    min-width: 90px;
    align-items: center;
  }

  .agenda-header {
    font-size: 0.85rem;
    font-weight: bold;
    margin-bottom: 8px;
    color: #555;
  }

  .agenda-slots {
    display: flex;
    flex-direction: column;
    gap: 4px;
    width: 100%;
    padding: 0 5px;
  }
  .boton-dia {
    padding: 8px 4px;
    font-size: 0.85rem;
    border: 1px solid #ddd;
    background: white;
    border-radius: 4px;
    cursor: pointer; /* La manito por defecto */
    transition: all 0.2s ease;
    width: 100%;
  }
  .boton-dia:hover:not(:disabled) {
    background-color: #e3f2fd;
    border-color: #2196f3;
    color: #1976d2;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .boton-dia-selected {
    background-color: #2196f3 !important;
    color: white !important;
    border-color: #1976d2 !important;
    font-weight: bold;
  }

  /* BOTÓN DESHABILITADO (OCUPADO) */
  .boton-dia:disabled {
    background-color: #fdeaea; /* Fondo rojizo muy tenue */
    color: #d32f2f;            /* Texto en rojo oscuro */
    border: 1.5px solid #ffcdd2; /* Borde rojo suave */
    cursor: not-allowed;       /* EL PUNTERO CAMBIA AL CÍRCULO TACHADO */
    opacity: 0.8;
    box-shadow: none;          /* Quitamos sombras */
  }

  /* Si el botón está deshabilitado porque NO elegiste veterinario (pero no está ocupado) */
  /* Esto es opcional, por si querés diferenciar "ocupado" de "faltan datos" */
  .boton-dia:disabled:not(.slot-ocupado) {
    background-color: #f5f5f5;
    color: #999;
    border-color: #eee;
    border-style: solid;
  }

  /* Refuerzo para el estado ocupado específico */
  .boton-dia-ocupado {
    border-color: #e57373 !important; /* Rojo más intenso */
    position: relative;
  }

  /* Opcional: una sutil x o marca visual */
  .boton-dia-ocupado::after {
    content: '×';
    position: absolute;
    top: -2px;
    right: 2px;
    font-size: 10px;
    color: #ef5350;
  }
  abbr {
    color: red;
    text-decoration: none;
  }
</style>