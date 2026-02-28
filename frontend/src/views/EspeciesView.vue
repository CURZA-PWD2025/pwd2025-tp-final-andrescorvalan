<script setup lang="ts">
  import { useRouter } from 'vue-router'
  import { onMounted } from 'vue'

  const router = useRouter()

  onMounted(() => {
    router.push({ name: 'especies_list' })
  })
</script>

<template>
  <h1>Administración de Especies</h1>
  <router-view/>
</template>

<style scoped></style>