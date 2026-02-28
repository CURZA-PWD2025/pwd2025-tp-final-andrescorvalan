<script setup lang="ts">
  import { useRouter } from 'vue-router'
  import { onMounted } from 'vue'

  const router = useRouter()

  onMounted(() => {
    router.push({ name: 'especialidades_list' })
  })
</script>

<template>
  <h1>Administración de Especialidades</h1>
  <router-view/>
</template>

<style scoped></style>