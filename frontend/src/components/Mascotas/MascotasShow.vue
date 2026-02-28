<script setup lang="ts">
  import { toRefs, onMounted } from 'vue'
  import { Icon } from "@iconify/vue"
  import useMascotasStore from '../../stores/mascotas_store'
  import { useRoute, useRouter } from 'vue-router'
  

  const router = useRouter()
  const route = useRoute()
  const { mascota } = toRefs(useMascotasStore())
  const { buscar_mascota } = useMascotasStore()

  function go_mascotas_list() {
      router.push({ name: 'mascotas_list' })
  }

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'mascotas_list' })
      return
    }
    mascota.value.id=0
    //setTimeout(async () => { await buscar_mascota(id) }, 2000)
    await buscar_mascota(id)
  })
</script>

<template>
  <section class="grud">
    <header class="grud-encabezado">
      <h2>Detalles del Mascota</h2>
      <button @click="go_mascotas_list" class="boton boton-back">
        <Icon class="icono" icon="mdi:arrow-left"/>
        Volver al Listado
      </button>
    </header>
    <article class="grud-frame" v-if="mascota.id !== 0">
      <dl class="grud-field-name">ID:
        <span class="grud-data"> {{ mascota.id }}</span>
      </dl>
      <dl class="grud-field-name">Nombre:
        <span class="grud-data">{{ mascota.nombre }}</span>
      </dl>
      <dl class="grud-field-name">Fecha de Nacimiento:
        <span class="grud-data">{{ mascota.fecha_nac }}</span>
      </dl>
      <fieldset class="grud-fieldset">
        <legend class="grud-legend">Propietario</legend>
        <dl class="grud-field-name">Nombre:
          <span class="grud-data">{{ mascota.propietario.nombre }}</span>
        </dl>
        <dl class="grud-field-name">Apellido:
          <span class="grud-data">{{ mascota.propietario.apellido }}</span>
        </dl>
        <dl class="grud-field-name">DNI:
          <span class="grud-data">{{ mascota.propietario.dni }}</span>
        </dl>
        <dl class="grud-field-name">Teléfono:
          <span class="grud-data">{{ mascota.propietario.telefono }}</span>
        </dl>
        <dl class="grud-field-name">Email:
          <span class="grud-data">{{ mascota.propietario.email }}</span>
        </dl>
      </fieldset>
      <fieldset class="grud-fieldset">
        <legend class="grud-legend">Especie</legend>
        <dl class="grud-field-name">Nombre:
          <span class="grud-data">{{ mascota.especie.nombre }}</span>
        </dl>
        <dl class="grud-field-name">Nombre Científico:
          <span class="grud-data">{{ mascota.especie.nombre_cientifico }}</span>
        </dl>
        <dl class="grud-field-name">Clase:
          <span class="grud-data">{{ mascota.especie.clase }}</span>
        </dl>
      </fieldset>
    </article>
    <div v-else class="grud-mensaje">
      <transition name="mensaje-fade" mode="out-in">
        <div role="alert" class="mensaje-alerta mensaje-procesando">
          <Icon class="icono-carga" icon="line-md:loading-twotone-loop" />
          Buscando información del mascota...
        </div>
      </transition>
    </div>
  </section> 
</template>

<style scoped>
</style>
