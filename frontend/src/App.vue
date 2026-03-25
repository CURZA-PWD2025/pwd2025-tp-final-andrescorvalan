<script setup lang="ts">
  import { RouterView } from 'vue-router'
  import Navbar from '@/components/layout/NavBar.vue'
  import AppFooter from './components/layout/AppFooter.vue'
</script>

<template>
  <div class="app-wrapper">   
    <Navbar />
    <main class="main-content">
      <router-view> </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<style scoped>
  .app-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  .main-content{
    flex: 1;
    padding: 2rem;
  }
  @media (max-width: 768px) {
    .main-content {
      padding: 0.5rem;
    }
  }
</style>