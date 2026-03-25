<script setup lang="ts">
  import { useRouter, useRoute } from 'vue-router'
  import { onMounted } from 'vue'

  const router = useRouter()
  const route = useRoute()

  onMounted(() => {
    if (route.name === 'especies') {
      router.push({ name: 'especies_list' })
    } 
  })
</script>

<template>
  <router-view />
</template>


<style scoped></style>
