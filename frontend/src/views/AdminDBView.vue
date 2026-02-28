<script setup lang="ts">
  import { ref } from 'vue'
  import { Icon } from '@iconify/vue'
  import ApiService from '@/services/ApiService'

  import useEspecialidadesStore from '../stores/especialidades_store'
  import useEspeciesStore from '../stores/especies_store'
  import usePropietariosStore from '../stores/propietarios_store'
  import useVeterinariosStore from '../stores/veterinarios_store'
  import useMascotasStore from '../stores/mascotas_store'
 
  const especialidadStore = useEspecialidadesStore()
  const mascotaStore = useMascotasStore()
  const especieStore = useEspeciesStore()
  const propietarioStore = usePropietariosStore()
  const veterinarioStore = useVeterinariosStore()

  const mensaje = ref('')
  const tipoMensaje = ref('')
  
  const mje_advertencia = ref('')
  const comando = ref('')
  
  const procesando = ref(false)
  const confirmar = ref(false)

  const limpiarTodosLosStores = () => {
    especialidadStore.reset()
    mascotaStore.reset()
    especieStore.reset()
    propietarioStore.reset()
    veterinarioStore.reset()
  }

  function confirmarAccion(accion: string) {
    confirmar.value = true
    comando.value = accion
    if (accion === 'clear')
      mje_advertencia.value = '¿Desesa BORRAR TODAS las tablas? Esta acción no se puede deshacer.'
    if (accion === 'setup')
      mje_advertencia.value = '¿Desea crear la estructura de tablas vacía?'
    if (accion === 'seed')
      mje_advertencia.value = '¿Desea cargar los datos de ejemplo predefinidos?'
  }
  async function ejecutarAccion() {
    procesando.value = true
    mensaje.value = ''
    try {
      const data = await ApiService.execute(`/db/${comando.value}`)
      limpiarTodosLosStores()
      mensaje.value = data.message
      tipoMensaje.value = 'mensaje-exito'
    } catch (error: any) {
      mensaje.value = error.response?.data?.error || error.message
      tipoMensaje.value = 'mensaje-error'
    } finally {
      procesando.value = false
      confirmar.value = false
      setTimeout(() => { if (mensaje.value) mensaje.value = ''; }, 5000)
    }
  }
</script>

<template>
  <div class="grud">
    <div class="grud-encabezado">
      <h1>Panel de Control de Base de Datos</h1>
    </div>
    <div class="grud-mensaje">
      <transition name="mensaje-fade">
        <div v-if="mensaje" class="mensaje-alerta" :class="tipoMensaje">
          {{ mensaje }}
        </div>
      </transition>
    </div>
    <div class="grud-frame">
      <h3>Mantenimiento de la Base de Datos</h3>      
      <div class="grud-list">
        <div class="grud-list-item">
          <h4>Inicializar Estructura</h4>
          <p class="grud-data">Crea la base de datos "Veterinaria" y sus tablas (Propietarios, Mascotas, etc.) pero sin contenido.</p>
          <div class="grud-botones">
            <button @click="confirmarAccion('setup')" class="boton boton-add" :disabled="procesando">
              <Icon class="icono" icon="mdi:table-plus" /> Crear/Vaciar Tablas
            </button>
          </div>
        </div>
        <div class="grud-list-item">
          <h4>Cargar Datos de Ejemplo</h4>
          <p class="grud-data">Inserta registros de prueba para demostrar el funcionamiento del sistema.</p>
          <div class="grud-botones">
            <button @click="confirmarAccion('seed')" class="boton boton-accept" :disabled="procesando">
              <Icon class="icono" icon="mdi:database-import" /> Cargar Datos
            </button>
          </div>
        </div>
        <div class="grud-list-item">
          <h4>Limpieza Total</h4>
          <p class="grud-data">Elimina toda la base de datos (tablas y datos) . Útil para un reinicio completo.</p>
          <div class="grud-botones">
            <button @click="confirmarAccion('clear')" class="boton boton-delete" :disabled="procesando">
              <Icon class="icono" icon="mdi:trash-can-outline" /> Borrar la Base de Datos
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="confirmar" class="deshabilitar-interaccion">
      <div class="ventana-emergente">
        <!-- Mensaje de Procesamiento -->
        <div v-if="procesando">
          <div class="icono-procesando"></div>
          <p>Procesando solicitud en el servidor...</p>
        </div>
        <!-- Mensaje de Confirmación -->
        <div v-else>
          <p>{{ mje_advertencia }}</p>
          <div class="grud-botones">
              <button @click="ejecutarAccion" class="boton boton-delete">
                Confirmar
              </button>
              <button @click="confirmar = false; procesando=false " class="boton boton-cancel">
                Cancelar
              </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>