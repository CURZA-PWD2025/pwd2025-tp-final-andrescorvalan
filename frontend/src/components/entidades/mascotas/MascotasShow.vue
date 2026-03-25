| <script setup lang="ts">
  import { ref, toRefs, onMounted } from 'vue'
  import { Icon } from "@iconify/vue"
  
  import { useRoute, useRouter } from 'vue-router'
  const router = useRouter()
  const route = useRoute()

  import useMascotasStore from '@/stores/mascotas_store'
  const { mascota } = toRefs(useMascotasStore())
  const { buscar_mascota, defaultMascota } = useMascotasStore()

  import ShowViewGenerico from '@/components//crud-generico/ShowViewGenerico.vue'

  const mensajeError = ref('')

  onMounted(async () => {

    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'mascotas_list' })
      return
    }

    mascota.value = { ...defaultMascota }
    try {    
      await buscar_mascota(id)
    } catch (error: any) {
      mensajeError.value = error.mensaje || 'No se encontró la mascota.'
    }
  })

  const formatearFecha = (fechaStr: string) => {
    const date = new Date(fechaStr + 'T00:00:00')
    return date.toLocaleDateString('es-AR', {day: '2-digit', month: '2-digit', year: 'numeric'});
  };
</script>

<template>
  <ShowViewGenerico
    titulo="Detalles de la mascota"
    :mensaje="mensajeError" 
    @volver="router.push({ name: 'mascotas_list' })">
    <template #detalles v-if="mascota.id !== 0">
      <header class="ficha-encabezado">
        <Icon icon="mdi:paw" class="ficha-logo" />
        <div>
          <h2>{{ mascota.nombre }}</h2>
          <p>ID: {{ mascota.id }}</p>
          <p>Fecha de nacimiento: {{ formatearFecha(mascota.fecha_nac) }}</p>
          <p>Sexo: {{ mascota.sexo }}</p>
        </div>
      </header>
      <div class="ficha-detalles">
        <section class="ficha-tarjeta">  
          <div class="ficha-tarjeta-titulo">
            <Icon icon="mdi:account" /> Datos del Propietario
          </div>
          <div class="card-body">
            <div class="ficha-tarjeta-fila">
              <span>Nombre:</span>
              <strong>{{ mascota.propietario.nombre }} {{ mascota.propietario.apellido }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>DNI:</span>
              <strong>{{ mascota.propietario.dni }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Teléfono:</span>
              <strong>{{ mascota.propietario.telefono }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Email:</span>
              <strong>{{ mascota.propietario.email }}</strong>
            </div>
          </div>
        </section>
        <section class="ficha-tarjeta">
          <div class="ficha-tarjeta-titulo">
            <Icon icon="mdi:cat" /> Información de Especie
          </div>
          <div class="card-body">
            <div class="ficha-tarjeta-fila">
              <span>Especie:</span>
              <strong>{{ mascota.especie.nombre }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Nombre Científico:</span>
              <strong>{{ mascota.especie.nombre_cientifico }}</strong>
            </div>
            <div class="ficha-tarjeta-fila">
              <span>Clase:</span> 
              <strong>{{ mascota.especie.clase }}</strong>
            </div>
          </div>
        </section>
      </div>
    </template>
  </ShowViewGenerico>
</template>

<style scoped>
</style>