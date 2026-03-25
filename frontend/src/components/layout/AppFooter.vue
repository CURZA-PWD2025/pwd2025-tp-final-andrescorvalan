<script setup lang="ts">
</script>

<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-section">
        <p>Estudiante: <strong>Andrés Leandro Corvalan</strong></p>
      </div>
      <div class="footer-section">
        <p>Materia: <strong>Programación Web Dinámica</strong></p>
      </div>
      <div class="footer-section">
        <p>Trabajo Práctico Final: <strong>Sistema de Gestión Veterinaria</strong></p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
  .app-footer {
    background-color: #2c3e50;
    color: white;
    padding: 1.5rem 0;
    margin-top: auto;
    width: 100%;
    border-top: 4px solid #ffcc00;
  }
  .footer-content {
    display: flex;
    justify-content: space-around;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    flex-wrap: wrap;
    gap: 1rem;
  }
  .footer-section {
    display: flex;
    align-items: center;
    font-size: 0.9rem;
  }
  strong {
    color: #ffcc00;
  }
  @media (max-width: 768px) {
    .footer-content {
      flex-direction: column;
      text-align: center;
    }
  }
</style>