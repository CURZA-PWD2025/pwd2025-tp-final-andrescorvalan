<script setup lang="ts">
  import { computed, ref } from 'vue'
  import { Icon } from '@iconify/vue'
  import ApiService from '@/services/api_service'

  import useEspecialidadesStore from '../stores/especialidades_store'
  import useEspeciesStore from '../stores/especies_store'
  import usePropietariosStore from '../stores/propietarios_store'
  import useVeterinariosStore from '../stores/veterinarios_store'
  import useMascotasStore from '../stores/mascotas_store'
  import useAtencionesStore from '../stores/atenciones_store'


  const especialidadStore = useEspecialidadesStore()
  const mascotaStore = useMascotasStore()
  const especieStore = useEspeciesStore()
  const propietarioStore = usePropietariosStore()
  const veterinarioStore = useVeterinariosStore()
  const atencionStore = useAtencionesStore()


  const mensaje = ref('')
  const estado = ref('')
  
  const mje_advertencia = ref('')
  const comando = ref('')
  
  const procesando = ref(false)
  const confirmar = ref(false)

  const tipoMensaje = computed(() => ({
    'mensaje-exito': estado.value === 'exito',
    'mensaje-error': estado.value === 'error',
    'mensaje-procesando': estado.value === 'procesando'
  }));

  const limpiarTodosLosStores = () => {
    especialidadStore.reset()
    mascotaStore.reset()
    especieStore.reset()
    propietarioStore.reset()
    veterinarioStore.reset()
    atencionStore.reset()
  }

  function confirmarAccion(accion: string) {
    confirmar.value = true
    comando.value = accion
    if (accion === 'clear')
      mje_advertencia.value = '¿Desesa BORRAR TODAS las tablas? Esta acción no se puede deshacer.'
    if (accion === 'setup')
      mje_advertencia.value = '¿Desea crear la estructura de tablas vacía?'
    if (accion === 'seed')
      mje_advertencia.value = '¿Desea crear la estructura de tablas y cargar datos de ejemplo?'
  }

  async function ejecutarAccion() {
    procesando.value = true
    estado.value = 'procesando'
    mensaje.value = ''
    try {
      const data = await ApiService.execute(`/db/${comando.value}`)
      limpiarTodosLosStores()
      mensaje.value = data.mensaje
      estado.value = 'exito'
    } catch (error: any) {
      mensaje.value = error.mensaje || 'Error crítico en la base de datos.'
      estado.value = 'error'
    } finally {
      procesando.value = false
      confirmar.value = false
      setTimeout(() => { if (mensaje.value) mensaje.value = ''; }, 5000)
    }
  }
</script>

<template>
  <div class="crud">
    <div class="crud-encabezado">
      <h2>Panel de Control de Base de Datos</h2>
    </div>
    <div class="crud-mensaje">
      <transition name="mensaje-fade" mode="out-in">
        <div v-if="mensaje" :key="mensaje" class="mensaje-alerta" :class="tipoMensaje">
          <Icon v-if="estado === 'procesando'" icon="line-md:loading-twotone-loop" />
          {{ mensaje }}
        </div>
      </transition>
    </div>
    <div class="crud-frame">
      <h3>Mantenimiento de la Base de Datos</h3>      
      <div class="crud-list">
        <div class="crud-list-item">
          <h4>Inicializar Estructura</h4>
          <p class="crud-data">Crea la base de datos "Veterinaria" y sus tablas (Propietarios, Mascotas, etc.) pero sin contenido.</p>
          <div class="crud-botones">
            <button @click="confirmarAccion('setup')" class="boton boton-add" :disabled="procesando">
              <Icon class="icono" icon="mdi:table-plus" /> Crear/Vaciar Tablas
            </button>
          </div>
        </div>
        <div class="crud-list-item">
          <h4>Crear la BD con Datos de Ejemplos</h4>
          <p class="crud-data">
            Crea la base de datos "Veterinaria" e inserta registros de prueba para demostrar el funcionamiento del sistema.</p>
          <div class="crud-botones">
            <button @click="confirmarAccion('seed')" class="boton boton-accept" :disabled="procesando">
              <Icon class="icono" icon="mdi:database-import" /> Crear BD y Cargar Datos
            </button>
          </div>
        </div>
        <div class="crud-list-item">
          <h4>Limpieza Total</h4>
          <p class="crud-data">Elimina toda la base de datos (tablas y datos).</p>
          <div class="crud-botones">
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
          <div class="crud-botones">
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