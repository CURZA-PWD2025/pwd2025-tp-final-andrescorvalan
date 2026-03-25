<script setup lang="ts">
  import { RouterLink, RouterView } from 'vue-router'
  import { Icon } from "@iconify/vue"
</script>

<template>
  <nav>
    <div class="menu-items">
      <RouterLink to="/" class="opcion_menu">
        <Icon icon="mdi:home"/>
        <span>Home</span>
      </RouterLink>
      <RouterLink to="/propietarios" class="opcion_menu">
        <Icon icon="mdi:account-group"/>
        <span>Propietarios</span>
      </RouterLink>
      <RouterLink to="/veterinarios" class="opcion_menu">
        <Icon icon="mdi:doctor"/>
        <span>Veterinarios</span>
      </RouterLink>
      
      <RouterLink to="/mascotas" class="opcion_menu">
        <Icon icon="mdi:paw"/> 
        <span>Mascotas</span>
      </RouterLink>
      <RouterLink to="/atenciones" class="opcion_menu">
        <Icon icon="mdi:medical-bag"/>
        <span>Atenciones</span>
      </RouterLink>
      
      <RouterLink to="/especies" class="opcion_menu">
        <Icon icon="mdi:cat" />
        <span>Especies</span>
      </RouterLink>
      <RouterLink to="/especialidades" class="opcion_menu">
        <Icon icon="mdi:certificate" />
        <span>Especialidades</span>
      </RouterLink>
      <RouterLink to="/admin_db" class="opcion_menu">
        <Icon icon="mdi:database-cog" />
        <span>Base de Datos</span>
      </RouterLink>
    </div>
    <img class="logo-nav" src="../../assets/marca.png" alt="">
  </nav>
</template>

<style scoped>
  nav {
    background-color: #436ad3;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 0 1rem;
    box-sizing: border-box;
    min-height: 80px;
  }
  .menu-items {
    display: flex;
    flex-direction: row;
    align-items: stretch;
    gap: 4px;
  }
  .opcion_menu {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 0.5rem;
    margin: 0.25rem;
    min-width: 85px; 
    text-decoration: none;
    background-color: #E0E0E0;
    color: #333;
    border-radius: 8px;
    transition: all 0.3s ease;
    cursor: pointer;
    border: none;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .opcion_menu span {
    font-size: 0.8rem;
    font-weight: bold;
    margin-top: 4px;
  }
  .opcion_menu .iconify {
    font-size: 1.6rem;
    color: #064388;
  }
  .opcion_menu:hover {
    background-color: #f0f0f0;
    transform: translateY(-2px);
  }
  nav .menu-items .opcion_menu.router-link-active {
    background-color: #2c3e50;
    color: #ffffff;
  }
  nav .menu-items .router-link-active .iconify {
    color: #ffcc00;
  }
  .logo-nav {
    border: 0.1rem solid #CC7A00;
    border-radius: 0.5rem;
    height: 60px;
    flex-shrink: 0;
    margin-left: 1rem;
  }
  @media (max-width: 768px) {
    nav {
        flex-direction: row;
        justify-content: space-between;
        min-height: 60px;
      }
    .opcion_menu {
      min-width: 45px;
      height: 45px;
      padding: 0;
      border-radius: 50%;
    }
    .opcion_menu span {
      display: none;
    }
    .opcion_menu .iconify {
      font-size: 1.8rem;
      margin: 0;
    }
    .logo-nav {
      height: 45px;
      margin-left: 0.5rem;
    }
  }
</style>