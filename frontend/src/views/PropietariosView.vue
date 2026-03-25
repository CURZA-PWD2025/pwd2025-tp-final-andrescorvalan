<script setup lang="ts">
  import { useRouter, useRoute } from 'vue-router'
  import { onMounted } from 'vue'

  const router = useRouter()
  const route = useRoute()

  onMounted(() => {
    if (route.name === 'propietarios') {
      router.push({ name: 'propietarios_list' })
    } 
  })
</script>

<template>
  <router-view />
</template>


<style scoped></style>
