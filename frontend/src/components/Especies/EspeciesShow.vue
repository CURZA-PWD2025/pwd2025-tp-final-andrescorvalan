<script setup lang="ts">
  import { toRefs, onMounted } from 'vue'
  import { Icon } from "@iconify/vue"
  import useEspeciesStore from '../../stores/especies_store'
  import { useRoute, useRouter } from 'vue-router'

  const router = useRouter()
  const route = useRoute()
  const { especie } = toRefs(useEspeciesStore())
  const { buscar_especie } = useEspeciesStore()

  function go_especies_list() {
      router.push({ name: 'especies_list' })
  }

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'especie_list' })
      return
    }
    especie.value.id=0
    //setTimeout(async () => { await buscar_especie(id) }, 2000)
    await buscar_especie(id)
  })
</script>

<template>
  <section class="grud">
    <header class="grud-encabezado">
      <h2>Detalles de la Especie</h2>
      <button @click="go_especies_list" class="boton boton-back">
        <Icon class="icono" icon="mdi:arrow-left"/>
        Volver al Listado
      </button>
    </header>
    <article class="grud-frame" v-if="especie.id !== 0">
      <dl class="grud-field-name">ID:
        <span class="grud-data"> {{ especie.id }}</span>
      </dl>
      <dl class="grud-field-name">Nombre:
        <span class="grud-data">{{ especie.nombre }}</span>
      </dl>
      <dl class="grud-field-name">Nombre Científico:
        <span class="grud-data">{{ especie.nombre_cientifico }}</span>
      </dl>
      <dl class="grud-field-name">Clase:
        <span class="grud-data">{{ especie.clase }}</span>
      </dl>
    </article>
    <div v-else class="grud-mensaje">
      <transition name="mensaje-fade" mode="out-in">
        <div role="alert" class="mensaje-alerta mensaje-procesando">
          <Icon class="icono-carga" icon="line-md:loading-twotone-loop" />
          Buscando información de la especie...
        </div>
      </transition>
    </div>
  </section> 
</template>

<style scoped>
</style>
