<script setup>
  import { onMounted, toRefs } from 'vue'
  import { useRouter } from 'vue-router'
  const router = useRouter()

  import useTurnosStore from '@/stores/turnos_store'
  const { turnos_proximos } = toRefs(useTurnosStore())
  const { getProximos } = useTurnosStore()

  import useMascotasStore from '@/stores/mascotas_store'
  const { mascotas } = toRefs(useMascotasStore())
  const { getAll: getMascotas } = useMascotasStore()

  onMounted(async () => {
    await Promise.all([getProximos(), getMascotas()])
  })
</script>

<template>
  <div class="home-container">
    <!-- Banner -->
    <section class="banner">
      <div class="banner-overlay"></div>
      <div class="banner-content">
        <div class="banner-text">
          <h1>Happy Animals</h1>
          <p>Cuidado profesional para quienes más quieres.</p>
        </div>
      </div>
    </section>
    <!-- Metricas -->
    <div class="metricas">
      <div class="metrica-tarjeta">
        <icon-mdi-paw class="metrica-icon" />
        <div class="metrica-text">
          <span class="metrica-number">{{ turnos_proximos.length }}</span>
          <span class="metrica-label">Turnos hoy</span>
        </div>
      </div>
      <div class="metrica-tarjeta">
        <icon-mdi-calendar-clock class="metrica-icon" />
        <div class="metrica-text">
          <span class="metrica-number">{{ mascotas.length }}</span>
          <span class="metrica-label">Mascotas activas</span>
        </div>
      </div>

      <div class="metrica-tarjeta highlight">
        <span class="metrica-label">Atención rápida</span>
        <button @click="router.push({name: 'turnos_create'})" class="boton-rapido">
          Nueva Cita
        </button>
        <button @click="router.push({name: 'atenciones_create'})" class="boton-rapido">
          Registrar Atención
        </button>
      </div>
    </div>
    <!-- Accesos rapidos -->
    <h2 class="section-title">Accesos Rápidos</h2>
    <div class="accesos-rapidos">
      <!-- Turnos -->
      <div class="accesorapido-tarjeta" @click="router.push({ name: 'turnos_list' })">
        <div class="accesorapido-icon"> 
          <icon-mdi-calendar-clock/>
        </div>
        <div class="accesorapido-texto">
          <h3>Turnos</h3>
          <p>Agenda y Horarios</p>
        </div>
        <icon-mdi-chevron-right class="icon-flecha" />
      </div>
      <!-- Atenciones -->
      <div class="accesorapido-tarjeta" @click="router.push({ name: 'atenciones_list' })">
        <div class="accesorapido-icon">
          <icon-mdi-medical-bag/>
        </div>
        <div class="accesorapido-texto">
          <h3>Atenciones</h3>
          <p>Administrar Atenciones</p>
        </div>
        <icon-mdi-chevron-right class="icon-flecha" />
      </div>
      <!-- Propiedades -->
      <div class="accesorapido-tarjeta" @click="router.push({ name: 'propietarios_list' })">
        <div class="accesorapido-icon">
          <icon-mdi-account-group/>
        </div>
        <div class="accesorapido-texto">
          <h3>Propietarios</h3>
          <p>Administrar Propietarios</p>
        </div>
        <icon-mdi-chevron-right class="icon-flecha" />
      </div>
      <!-- Mascotas -->
      <div class="accesorapido-tarjeta" @click="router.push({ name: 'mascotas_list' })">
        <div class="accesorapido-icon">
          <icon-mdi-dog />
        </div>
        <div class="accesorapido-texto">
          <h3>Mascotas</h3>
          <p>Administrar Mascotas</p>
        </div>
        <icon-mdi-chevron-right class="icon-flecha" />
      </div>
      <!-- Mascotas -->
      <div class="accesorapido-tarjeta" @click="router.push({ name: 'veterinarios_list' })">
        <div class="accesorapido-icon">
          <icon-mdi-doctor/>
        </div>
        <div class="accesorapido-texto">
          <h3>Veterinarios</h3>
          <p>Administrar Veterinarios</p>
        </div>
        <icon-mdi-chevron-right class="icon-flecha" />
      </div>
      <!-- Especies -->
      <div class="accesorapido-tarjeta" @click="router.push({ name: 'especies_list' })">
        <div class="accesorapido-icon">
          <icon-mdi-panda/>
        </div>
        <div class="accesorapido-texto">
          <h3>Especies</h3>
          <p>Administrar Especies</p>
        </div>
        <icon-mdi-chevron-right class="icon-flecha" />
      </div>
      <!-- Especialidades -->
      <div class="accesorapido-tarjeta" @click="router.push({ name: 'especialidades_list' })">
        <div class="accesorapido-icon">
          <icon-mdi-certificate/>
        </div>
        <div class="accesorapido-texto">
          <h3>Especialidades</h3>
          <p>Administrar Especialidades</p>
        </div>
        <icon-mdi-chevron-right class="icon-flecha" />
      </div>
    </div>
  </div>
</template>

<style scoped>
  .home-container {
    padding: 1.5rem;
    text-align: left;
  }
  /* Banner */
  .banner {
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
  .banner-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, rgba(63, 81, 181, 0.9) 0%, rgba(63, 81, 181, 0.4) 100%);
    z-index: 1;
  }
  .banner-content {
    position: relative;
    z-index: 2;
  }
  .banner-text h1 {
    font-size: 3rem;
    margin: 0;
    font-weight: 800;
  }
  .banner-text p {
    font-size: 1.2rem;
    opacity: 0.9;
    margin-top: 0.5rem;
  }
  /* Metricas */
  .metricas {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2.5rem;
  }
  .metrica-tarjeta {
    background-color: white;
    border-radius: 0.8rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: row; 
    align-items: center;
    justify-content: flex-start;
    gap: 20px;  
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border-bottom: 4px solid #3f51b5;
  }
  .metrica-tarjeta.highlight {
    background-color: #3f51b5;
    border-bottom: none;
  }
  .metrica-tarjeta.highlight .metrica-label {
    color: white;
    margin-bottom: 10px;
  }
  .metrica-icon {
    font-size: 3.5rem;
    color: #3f51b5;
    opacity: 0.8;
  }
  .metrica-text {
    display: flex;
    flex-direction: column;
    text-align: left;
  }
  .metrica-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: #333;
    line-height: 1;
  }
  .metrica-label {
    font-size: 0.85rem;
    color: #6c757d;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 4px;
  }
  /* Botones para un rapido acceso */
  .boton-rapido {
    background-color: #ffcc00;
    color: #333;
    border: none;
    padding: 8px 15px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.2s;
    margin:0.2rem
  }
  .boton-rapido:hover {
    transform: scale(1.05);
    background-color: #fff;
  }
  /* Accesos rapidos */
  .accesos-rapidos {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }
  .accesorapido-tarjeta {
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
  .accesorapido-tarjeta:hover {
    transform: translateY(-5px);
    background-color: #ffffff;
    border-color: #3f51b5;
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  }
  .accesorapido-icon {
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
  .accesorapido-texto h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #2c3e50;
  }
  .accesorapido-texto p {
    margin: 0;
    font-size: 0.85rem;
    color: #6c757d;
  }
  .icon-flecha {
    position: absolute;
    right: 1.2rem;
    color: #3f51b5;
    opacity: 0;
    transition: opacity 0.2s;
  }
  .accesorapido-tarjeta:hover .icon-flecha {
    opacity: 1;
  }
  @media (max-width: 600px) {
    .banner {
      padding: 2rem;
      flex-direction: column;
      text-align: center;
    }
    .banner-text h1 { font-size: 2rem; }
  }
</style>