<script setup lang="ts">
  import { toRefs, onMounted, ref, computed } from 'vue'
  import { Icon } from "@iconify/vue"
  import { recargarBD } from '@/router'

  import useTurnosStore from '@/stores/turnos_store'
  const { incluirHistorial, turno, turnos_proximos, turnos_historial } = toRefs(useTurnosStore())
  const { reset, getOne, update, getProximos, getHistorial, destroy } = useTurnosStore()

  const procesando = ref(false)         // Indica si se esta procesando una solicitud de eliminacion o cambio de estado

  const mostrarModal = ref(false)       // Determina si se muestra una ventana emergente (cambiar estado)
  const mostrarHistorial = ref(false)   // Determina si se muestra el listado de turnos anteriores

  const filtro = ref('')                // Filtro de búsqueda

  const mensajeAccion = ref('')         // Mensaje y estado ante una accion (eliminar/cambiar estado)
  const estadoAccion = ref('')                      

  const mensajeProx = ref('')           // Mensaje y estado al leer proximos turnos
  const estadoProx = ref('') 

  const mensajeHist = ref('')           // Mensaje y estado al leer turnos anteriores
  const estadoHist = ref('')

  const idEliminar = ref<number | null>(null)       // Id del turno a eliminar
  const idCambiarEstado = ref<number | null>(null)  // Id del turno que cambia de estado

  const nuevoEstado = ref('')

  //Carga de turnos futuros y pasados, con manejo de estados y mensajes para el usuario
  const loadTurnosProx = async () => {
    mensajeProx.value = ''
    estadoProx.value = 'cargandoProx'
    try{
        const respuesta = await getProximos()
        mensajeProx.value = 'Turnos Siguientes: ' + respuesta.mensaje
        estadoProx.value = 'cargaProxOk'
        setTimeout(() => {
            mensajeProx.value = '';
            estadoProx.value = '';
        }, 2000);
    } catch (error: any) {
        mensajeProx.value = error.mensaje || 'Error al cargar datos.'
        estadoProx.value = 'cargaError'
    }
  }
  const loadTurnosHist = async () => {
    mensajeHist.value = ''
    estadoHist.value = 'cargandoHist'
    try{
        const respuesta = await getHistorial()
        mensajeHist.value = 'Turnos Anteriores: ' + respuesta.mensaje
        estadoHist.value = 'cargaHistOk'
        setTimeout(() => {
            mensajeHist.value = '';
            estadoHist.value = '';
        }, 2000);
    } catch (error: any) {
        mensajeHist.value = error.mensaje || 'Error al cargar datos.'
        estadoHist.value = 'cargaError'
    }
  }
  // procesamientos de los listados de turnos (futuros y pasados), filtrado por el buscador y agrupacion por fecha
  const turnosProxFiltrados = computed(() => {
    const busqueda = filtro.value.toLowerCase().trim()
    if (!busqueda) 
      return turnos_proximos.value
    return turnos_proximos.value.filter(p => 
      p.fecha_hora.includes(busqueda) || 
      p.veterinario.apellido.toLowerCase().includes(busqueda) ||
      p.veterinario.nombre.toLowerCase().includes(busqueda) ||
      p.motivo.toLowerCase().includes(busqueda) ||
      p.estado.toLowerCase().includes(busqueda) ||
      p.mascota.nombre.toLowerCase().includes(busqueda) ||
      p.mascota.propietario.apellido.toLowerCase().includes(busqueda) ||
      p.mascota.propietario.nombre.toLowerCase().includes(busqueda)
    )
  })
  const turnosHistFiltrados = computed(() => {
    const busqueda = filtro.value.toLowerCase().trim()
    if (!busqueda) 
      return turnos_historial.value
    return turnos_historial.value.filter(p => 
      p.fecha_hora.includes(busqueda) || 
      p.veterinario.apellido.toLowerCase().includes(busqueda) ||
      p.veterinario.nombre.toLowerCase().includes(busqueda) ||
      p.motivo.toLowerCase().includes(busqueda) ||
      p.estado.toLowerCase().includes(busqueda) ||
      p.mascota.nombre.toLowerCase().includes(busqueda) ||
      p.mascota.propietario.apellido.toLowerCase().includes(busqueda) ||
      p.mascota.propietario.nombre.toLowerCase().includes(busqueda)
    )
  })
  const turnosProxPorDia = computed(() => {
    const dias : Record<string, any[]>= {};
    turnosProxFiltrados.value.forEach(unTurno => {
      const fechaDia = unTurno.fecha_hora.split('T')[0] || 'Sin fecha'
      if (!dias[fechaDia])
        dias[fechaDia] = []
      dias[fechaDia].push(unTurno)
      console.log(unTurno.fecha_hora)
    });
    return dias;
  })
  const turnosHistPorDia = computed(() => {
    const dias : Record<string, any[]>= {};
    turnosHistFiltrados.value.forEach(unTurno => {
      const fechaDia = unTurno.fecha_hora.split('T')[0] || 'Sin fecha'
      if (!dias[fechaDia])
        dias[fechaDia] = []
      dias[fechaDia].push(unTurno)

    });
    return dias;
  })

  // Inicializacion de la seccion, con lectura de la base de datos si es necesario
  const inicializar = async () => {
      await loadTurnosProx()
      if (mostrarHistorial.value)
        await loadTurnosHist()
    mostrarHistorial.value = incluirHistorial.value
    recargarBD.value = false
  }

  const onOffHistorial = async () => {
    mostrarHistorial.value = !mostrarHistorial.value
    if (mostrarHistorial.value && (recargarBD.value || turnos_historial.value.length === 0))
      await loadTurnosHist()
    incluirHistorial.value = mostrarHistorial.value 
  }

  onMounted(async () => {
    await inicializar()
  })

  const refrescar = async () => {
    recargarBD.value =true
    await inicializar()
  }

  function resetList() {
    procesando.value = false
    mostrarModal.value = false
    mensajeAccion.value = ''
    estadoAccion.value = ''
    idEliminar.value = null
    idCambiarEstado.value = null
  }
  
  //Acciones
  const ejecutarEliminar = async () => {
    if (!idEliminar.value)
      return
    procesando.value = true
    mensajeAccion.value = 'Intentando eliminar el turno.'
    mostrarModal.value = true
    try {  
        const respuesta = await destroy(idEliminar.value)
        mensajeAccion.value = respuesta.mensaje || '¡Éxito! Se ha eliminado el turno.'
        estadoAccion.value = 'exito'
    } catch (error: any) {
        mensajeAccion.value =  error.mensaje || 'No se pudo eliminar el turno.'
        estadoAccion.value = 'error'
    } finally {
          idEliminar.value = null
          procesando.value = false
      }
  }
  const ejecutarCambiarEstado = async () => {
    if (idCambiarEstado.value && ['Ausente', 'Atendido','Pendiente'].includes(nuevoEstado.value)) {
      procesando.value = true
      mensajeAccion.value = `Intentando cambiar de estado.`
      mostrarModal.value = true
      try {  
        await getOne(idCambiarEstado.value)
        turno.value.estado = nuevoEstado.value
        const respuesta = await update(turno.value)
        mensajeAccion.value = respuesta.mensaje || '¡Éxito! Se actualizó el estado del turno.'
        estadoAccion.value = 'exito'
      } catch (error: any) {
          mensajeAccion.value =  error.mensaje || 'No se pudo actualizar el estado del turno.'
          estadoAccion.value = 'error'
      } finally {
          idCambiarEstado.value = null
          procesando.value = false
      }
    }
  }
  
  const formatearFechaCabecera = (fechaString: string) => {
    const fecha = new Date(fechaString + "T00:00:00")
    return fecha.toLocaleDateString('es-ES', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }).replace(/^\w/, (c) => c.toUpperCase())
  };

  const getFechaHora = (fechaStr: string) => {
    return fechaStr.split('T')
  }
</script>

<template>
  <section class="crud">
    <!-- Ventana para confirmar -->
    <div v-if="mostrarModal" class="deshabilitar-interaccion">
      <div v-if="idEliminar || idCambiarEstado">
        <div class="ventana-emergente">
          <div v-if="procesando === true">  
             <!-- Ya se esta procesando la solicitud -->
            <div class="icono-procesando"></div>
            {{ mensajeAccion }}
          </div>
          <div v-else>                      
            <!-- Aun no se esta procesando, ventana de confirmacion -->  
            {{ mensajeAccion }}
          </div>
          <!-- Botones Cambiar y Cancelar-->
          <div class="crud-botones">
            <button v-if="idEliminar" @click="ejecutarEliminar" :disabled="procesando" class="boton boton-accept">
              <span v-if="procesando">Procesando...</span>
              <span v-else>Sí, proceder</span>
            </button>
            <button v-if="idCambiarEstado" @click="ejecutarCambiarEstado" :disabled="procesando" class="boton boton-accept">
              <span v-if="procesando">Procesando...</span>
              <span v-else>Sí, proceder</span>
            </button>
            <button @click="resetList" :disabled="procesando" class="boton boton-cancel">
              <span>Cancelar</span>
            </button>
          </div>
        </div>
      </div>
      <div v-else>
        <!-- Se cambio el estado con exito -->
        <div v-if="estadoAccion === 'exito'" class="ventana-emergente ventana-emergente-exito">
          <icon-mdi-check-circle class="ventana-emergente-icono ventana-emergente-icono-exito"/>
          <h3>¡Excelente!</h3>
          <p>La solicitud fue procesada con exito.</p>
          <p class="mje-db">{{ mensajeAccion }}</p>
          <button @click="resetList" class="boton boton-accept" style="width: 100%;" type="button">
            Entendido
          </button>
        </div>
        <!-- No se cambio el estado por algun error -->
        <div v-else-if="estadoAccion ==='error'" class="ventana-emergente ventana-emergente-error">
          <icon-mdi-close-circle class="ventana-emergente-icono ventana-emergente-icono-error"/>
          <h3>Hubo un problema</h3>
          <p>La solicitud no fue procesada con exito.</p>
          <p class="mje-db">{{ mensajeAccion }}</p>
          <button @click="resetList" class="boton boton-accept" style="width: 100%;" type="button">
            Entendido
          </button>
        </div>
      </div>
    </div>

    <header class="crud-encabezado">
      <h2>Proximos Turnos</h2>
      <div class="crud-controles">
        <!-- Buscador -->
        <div class="buscador-wrapper">
          <Icon icon="mdi:magnify" class="icono-busqueda" />
          <input 
            v-model="filtro" class="input-busqueda"
            type="text" placeholder="Buscar por nombre, propietario ..." 
            title="Buscar por fecha, nombre de mascota, nombre o apellido del propietario, nombre o apellido del veterinario"/>
        </div>
        <!-- Botones -->
        <div class="crud-botones">
          <button @click="refrescar" class="boton boton-refresh" :disabled="estadoProx === 'leyendo' || estadoHist === 'leyendo'">
            <icon-mdi-refresh class="icono"/>Actualizar
          </button>
          <router-link class="boton boton-add" :to="{ name: 'turnos_create' }">
            <icon-mdi-add class="icono"/>Nuevo Turno
          </router-link>
        </div>
      </div>
    </header>
    <!-- Mensajes de la seccion Proximos Turnos -->
    <div class="crud-mensaje">
      <div v-if="estadoProx==='cargandoProx'" class="mensaje-alerta icono-procesando"></div>
      <transition  name="mensaje-fade" mode="out-in">
        <div v-if="estadoProx==='cargaError'" :key="mensajeProx" role="alert" class="mensaje-alerta mensaje-error">
          {{ mensajeProx }}
        </div>
      </transition>  
       <transition  name="mensaje-fade" mode="out-in">
        <div v-if="estadoProx==='cargaProxOk'" :key="mensajeProx" role="alert" class="mensaje-alerta mensaje-exito">
          {{ mensajeProx }}
        </div>
      </transition>  
    </div>
    <!-- Listado de turnos siguientes, ordenados por dia -->
    <div v-for="(turnosDelDia, fecha) in turnosProxPorDia" :key="fecha" class="crud-list-item">
      <!-- Listado del dia -->
      <h3>{{formatearFechaCabecera(fecha)}}</h3>
      <!-- Lista de elementos de ese día -->
      <article class="fila-grid" v-for="unTurno in turnosDelDia" :key="unTurno.id">
        <!-- Datos -->
        <span class="crud-data">{{ getFechaHora(unTurno.fecha_hora)[1]}}</span>
        <div>
          <dt class="crud-field-name">Propietario (Mascota)</dt>
          <dd class="crud-data">{{ unTurno.mascota.propietario.nombre }} {{ unTurno.mascota.propietario.apellido }}
            ({{ unTurno.mascota.nombre }})
          </dd>
        </div>
        <div>
          <dt class="crud-field-name">Veterinario</dt>
          <dd class="crud-data">{{ unTurno.veterinario.nombre }} {{ unTurno.veterinario.apellido }}</dd>
        </div>
        <div>
          <dt class="crud-field-name">Estado</dt>
          <dd :class="unTurno.estado.toLowerCase()">{{ unTurno.estado }}</dd>
        </div>
        <div>  <!-- Cambio de estado -->
          <button v-if="unTurno.estado !== 'Atendido'" title="Confirmar la Atención" class="boton_estado boton-atendido"
            @click="idCambiarEstado = unTurno.id; nuevoEstado = 'Atendido'; 
            mensajeAccion='¿Seguro que quieres cambiar el estado del turno a Atendido?';
            mostrarModal = true;">
            Atendido
          </button>
          <button v-if="unTurno.estado !== 'Ausente'" title="Marcar como Ausente" class="boton_estado boton-ausente"
            @click="idCambiarEstado = unTurno.id; nuevoEstado = 'Ausente';
            mensajeAccion='¿Seguro que quieres cambiar el estado del turno a Ausente?';
            mostrarModal = true;">
            Ausente
          </button>
          <button v-if="unTurno.estado !== 'Pendiente'" title="Marcar como Pendiente" class="boton_estado boton-pendiente"
            @click="idCambiarEstado = unTurno.id; nuevoEstado = 'Pendiente';
            mensajeAccion='¿Seguro que quieres cambiar el estado del turno a Pendiente?';
            mostrarModal = true;">
            Pendiente
          </button>
        </div>
        <!-- Botones -->
        <div class="crud-botones">
          <router-link title="Mostrar Detalles" class="boton boton-show" :to="{ name: 'turnos_show', params: { id: unTurno.id } }">
            <icon-mdi-eye class="icono" />
          </router-link>
          <router-link title="Editar Turno" class="boton boton-edit" :to="{ name: 'turnos_update', params: { id: unTurno.id } }">
            <icon-mdi-edit class="icono"/>
          </router-link>
          <button class="boton boton-delete" 
            @click="idEliminar = unTurno.id;
            mostrarModal = true;
            mensajeAccion='¿Seguro que quiere eliminar el turno?'">
            <icon-mdi-delete class="icono"/>
          </button>
        </div>
      </article> 
    </div>

    <!-- Ver/Ocultar Historial de turnos -->
    <div class="crud-botones">
      <button @click="onOffHistorial" class="boton boton-refresh" :disabled="estadoProx === 'leyendo' || estadoHist === 'leyendo'">
          <icon-mdi-plus-box v-if="!mostrarHistorial" class="icono"/>
          <icon-mdi-minus-box v-if="mostrarHistorial" class="icono"/>
          Ver/Ocultar Historial de turnos
        </button>
    </div>

    <!-- Mensajes de la seccion Historial-->
    <div v-if="mostrarHistorial">
      <div class="crud-mensaje">
        <div v-if="estadoHist==='cargandoHist'" class="mensaje-alerta icono-procesando"></div>
        <transition  name="mensaje-fade" mode="out-in">
          <div v-if="estadoHist==='cargaError'" :key="mensajeHist" role="alert" class="mensaje-alerta mensaje-error">
            {{ mensajeHist }}
          </div>
        </transition>  
        <transition  name="mensaje-fade" mode="out-in">
          <div v-if="estadoHist==='cargaHistOk'" :key="mensajeHist" role="alert" class="mensaje-alerta mensaje-exito">
            {{ mensajeHist }}
          </div>
        </transition>  
      </div>

      <!-- Listado de turnos anteriores, ordenados por dia -->
      <div v-for="(turnosDelDia, fecha) in turnosHistPorDia" :key="fecha" class="crud-list-item">
        <!-- Listado del dia -->
        <h3>{{formatearFechaCabecera(fecha)}}</h3>
        <!-- Lista de elementos de ese día -->
      <article class="fila-grid" v-for="unTurno in turnosDelDia" :key="unTurno.id">
          <!-- Datos -->
          <span class="crud-data">{{ getFechaHora(unTurno.fecha_hora)[1]}}</span>
          <div>
            <dt class="crud-field-name">Propietario (Mascota)</dt>
            <dd class="crud-data">{{ unTurno.mascota.propietario.nombre }} {{ unTurno.mascota.propietario.apellido }}
            ({{ unTurno.mascota.nombre }})

            </dd>
          </div>
          <div>
            <dt class="crud-field-name">Veterinario</dt>
            <dd class="crud-data">{{ unTurno.veterinario.nombre }} {{ unTurno.veterinario.apellido }}</dd>
          </div>
          <div>
            <dt class="crud-field-name">Estado</dt>
            <dd :class="unTurno.estado.toLowerCase()">{{ unTurno.estado }}</dd>
          </div>
          <div>  <!-- Cambio de estado -->
            <button v-if="unTurno.estado !== 'Atendido'" title="Confirmar la Atención" class="boton_estado boton-atendido"
              @click="idCambiarEstado = unTurno.id; nuevoEstado = 'Atendido'; 
              mensajeAccion='¿Seguro que quieres cambiar el estado del turno a Atendido?';
              mostrarModal = true;">
              Atendido
            </button>
            <button v-if="unTurno.estado !== 'Ausente'" title="Marcar como Ausente" class="boton_estado boton-ausente"
              @click="idCambiarEstado = unTurno.id; nuevoEstado = 'Ausente';
              mensajeAccion='¿Seguro que quieres cambiar el estado del turno a Ausente?';
              mostrarModal = true;">
              Ausente
            </button>
 
          </div>
          <!-- Botones -->
          <div class="crud-botones">
            <router-link title="Mostrar Detalles" class="boton boton-show" :to="{ name: 'turnos_show', params: { id: unTurno.id } }">
              <icon-mdi-eye class="icono" />
            </router-link>
          </div>
        </article> 
      </div>
    </div>
  </section> 
</template>

<style scoped>
  .crud-controles {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  :deep(.input-busqueda) {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    width: 25ch;
  }
 .mje-db {
    border: 1px solid gray;
    font-size: 0.7;
    color: gray;
    padding: 0.5rem;
  }
  .fila-grid {
    display: grid;
    grid-template-columns: 80px 1fr 1fr 10ch 1fr auto; 
    align-items: center;
    gap: 15px;
    padding: 12px;
    border-bottom: 1px solid #eee;
  }
  /* Colores por estado */
  .pendiente {
    color: #0369a1;
  }
  .atendido {
    color: #15803d;
  }
  .ausente {
    color: magenta;
  }
  /* Botones */
  .boton_estado {
    display:inline-flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: 0 0.3rem;
    margin:0.2rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: white;
    cursor: pointer;
    min-height: 30px;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 0.5rem;
    background: #555;
    box-shadow: 0 1px 0 rgba(255,255,255,0.2) inset;
    transition: all 0.2s ease;
    font-family: inherit;
    text-decoration: none;
    user-select: none;
    white-space: nowrap;
  }
  .boton_estado:active {
    transform: scale(0.98);
  }
  @media (hover: hover) and (pointer: fine) {
    .boton_estado:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      filter: brightness(1.5);
    }
  }
  .boton-ausente {
    background-color: #4e4e4e;
  }
  .boton-pendiente {
    background-color: #495da5;
  }
  .boton-atendido {
    background-color: #257738;
  }
</style>