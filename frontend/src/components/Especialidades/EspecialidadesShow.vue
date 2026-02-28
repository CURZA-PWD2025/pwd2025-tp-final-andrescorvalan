<script setup lang="ts">
  import { toRefs, onMounted } from 'vue'
  import { Icon } from "@iconify/vue"
  import useEspecialidadesStore from '../../stores/especialidades_store'
  import { useRoute, useRouter } from 'vue-router'

  const router = useRouter()
  const route = useRoute()
  const { especialidad } = toRefs(useEspecialidadesStore())
  const { buscar_especialidad } = useEspecialidadesStore()

  function go_especialidades_list() {
    router.push({ name: 'especialidades_list' })
  }

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'especialidades_list' })
      return
    }
    especialidad.value.id=0
    //setTimeout(async () => { await buscar_especialidad(id) }, 2000)
    await buscar_especialidad(id)
  })
</script>

<template>
  <section class="grud">
    <header class="grud-encabezado">
      <h2>Detalles de la Especialidad</h2>
      <button @click="go_especialidades_list" class="boton boton-back">
        <Icon class="icono" icon="mdi:arrow-left"/>
        Volver al Listado
      </button>
    </header>
    <article class="grud-frame" v-if="especialidad.id !== 0">
      <dl class="grud-field-name">ID:
        <span class="grud-data"> {{ especialidad.id }}</span>
      </dl>
      <dl class="grud-field-name">Nombre:
        <span class="grud-data">{{ especialidad.nombre }}</span>
      </dl>
      <dl class="grud-field-name">Nombre Científico:
        <span class="grud-data">{{ especialidad.descripcion }}</span>
      </dl>
    </article>
    <div v-else class="grud-mensaje">
      <transition name="mensaje-fade" mode="out-in">
        <div role="alert" class="mensaje-alerta mensaje-procesando">
          <Icon class="icono-carga" icon="line-md:loading-twotone-loop" />
          Buscando información de la especialidad...
        </div>
      </transition>
    </div>
  </section> 
</template>

<style scoped>
</style>