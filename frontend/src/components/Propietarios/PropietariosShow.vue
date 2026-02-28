| <script setup lang="ts">
  import { toRefs, onMounted } from 'vue'
  import { Icon } from "@iconify/vue"
  import usePropietariosStore from '../../stores/propietarios_store'
  import { useRoute, useRouter } from 'vue-router'

  const router = useRouter()
  const route = useRoute()
  const { propietario } = toRefs(usePropietariosStore())
  const { buscar_propietario } = usePropietariosStore()

  function go_propietarios_list() {
      router.push({ name: 'propietarios_list' })
  }

  onMounted(async () => {
    const id = Number(route.params.id)
    if (isNaN(id)) {
      router.push({ name: 'propietarios_list' })
      return
    }
    propietario.value.id=0
    //setTimeout(async () => { await buscar_propietario(id) }, 2000)
    await buscar_propietario(id)
  })
</script>

<template>
  <section class="grud">
    <header class="grud-encabezado">
      <h2>Detalles del Propietario</h2>
      <button @click="go_propietarios_list" class="boton boton-back">
        <Icon class="icono" icon="mdi:arrow-left"/>
        Volver al Listado
      </button>
    </header>
    <article class="grud-frame" v-if="propietario.id !== 0">
      <dl class="grud-field-name">ID:
        <span class="grud-data"> {{ propietario.id }}</span>
      </dl>
      <dl class="grud-field-name">Nombre:
        <span class="grud-data">{{ propietario.nombre }}</span>
      </dl>
      <dl class="grud-field-name">Apellido:
        <span class="grud-data">{{ propietario.apellido }}</span>
      </dl>
      <dl class="grud-field-name">DNI:
        <span class="grud-data">{{ propietario.dni }}</span>
      </dl>
      <dl class="grud-field-name">Teléfono:
        <span class="grud-data">{{ propietario.telefono }}</span>
      </dl>
      <dl class="grud-field-name">Email:
        <span class="grud-data">{{ propietario.email }}</span>
      </dl>
    </article>
    <div v-else class="grud-mensaje">
      <transition name="mensaje-fade" mode="out-in">
        <div role="alert" class="mensaje-alerta mensaje-procesando">
          <Icon class="icono-carga" icon="line-md:loading-twotone-loop" />
          Buscando información del propietario...
        </div>
      </transition>
    </div>
  </section> 
</template>

<style scoped>
</style>
