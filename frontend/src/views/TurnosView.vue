<!-- <script setup lang="ts">
  import { useRouter, useRoute } from 'vue-router'
  import { onMounted } from 'vue'
  import TurnosProximos from '@/components/entidades/turnos/TurnosProximos.vue'
  import TurnosHistorial from '@/components/entidades/turnos/TurnosHistorial.vue'

  const router = useRouter()
  const route = useRoute()

  onMounted(() => {
    if (route.name === 'turnos') {
      console.log("antes turnos proximos")
      router.push({ name: 'turnos_proximos' })
      console.log("despues turnos proximos")

      // router.push({ name: 'turnos_historial' })
    } 
  })
</script> -->

<template>
  <h1>Agenda de turnos</h1>
  <!-- 
  <turnos-proximos></turnos-proximos>
  <turnos-historial></turnos-historial> 
  -->
  <router-view />
</template>

<style scoped></style>
