<template>
  <div class="home-container">
    <section class="hero-banner">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="hero-text">
          <h1>Happy Animals</h1>
          <p>Cuidado profesional para quienes más quieres.</p>
        </div>
      </div>
    </section>

    <h2 class="section-title">Accesos Rápidos</h2>

    <div class="grid-shortcuts">
      <div 
        v-for="item in accesos" 
        :key="item.route" 
        class="card-shortcut"
        @click="router.push({ name: item.route })"
      >
        <div class="card-icon-wrapper">
          <Icon :icon="item.icon" />
        </div>
        <div class="card-content">
          <h3>{{ item.label }}</h3>
          <p>Administrar {{ item.label.toLowerCase() }}</p>
        </div>
        <Icon icon="mdi:chevron-right" class="arrow-icon" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useRouter } from 'vue-router'
  import { Icon } from '@iconify/vue'

  const router = useRouter()

  const accesos = [
    { label: 'Propietarios', route: 'propietarios_list', icon: 'mdi:account-group' },
    { label: 'Veterinarios', route: 'veterinarios_list', icon: 'mdi:doctor' },
    { label: 'Mascotas', route: 'mascotas_list', icon: 'mdi:dog' },
    { label: 'Atenciones', route: 'atenciones_list', icon: 'mdi:medical-bag' },
    { label: 'Especies', route: 'especies_list', icon: 'mdi:panda' },
    { label: 'Especialidades', route: 'especialidades_list', icon: 'mdi:certificate' },
  ]
</script>
<style scoped>

.home-container {
  padding: 1.5rem;
  text-align: left;
}

.hero-banner {
  position: relative;
  background-image: url('../assets/cats-dogs.jpg');
  background-position: center;
  color: white;
  border-radius: 0.8rem;
  padding: 4rem 3rem;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  margin-bottom: 2.5rem;
  min-height: 350px;
  display: flex;
  align-items: center;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, rgba(63, 81, 181, 0.9) 0%, rgba(63, 81, 181, 0.4) 100%);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-text h1 {
  font-size: 3rem;
  margin: 0;
  font-weight: 800;
}

.hero-text p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-top: 0.5rem;
}

.hero-icon-large {
  font-size: 6rem;
  opacity: 0.2;
}

.section-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
  padding-left: 0.5rem;
  border-left: 5px solid #3f51b5;
}

.grid-shortcuts {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.card-shortcut {
  background-color: #f0f2f5;
  border: 1px solid #dee2e6;
  border-radius: 0.6rem;
  padding: 1.2rem;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.card-shortcut:hover {
  transform: translateY(-5px);
  background-color: #ffffff;
  border-color: #3f51b5;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.card-icon-wrapper {
  background-color: #3f51b5;
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-right: 1.2rem;
}

.card-content h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.card-content p {
  margin: 0;
  font-size: 0.85rem;
  color: #6c757d;
}

.arrow-icon {
  position: absolute;
  right: 1.2rem;
  color: #3f51b5;
  opacity: 0;
  transition: opacity 0.2s;
}

.card-shortcut:hover .arrow-icon {
  opacity: 1;
}

@media (max-width: 600px) {
  .hero-banner {
    padding: 2rem;
    flex-direction: column;
    text-align: center;
  }
  .hero-text h1 { font-size: 2rem; }
}
</style>

