import { createRouter, createWebHistory } from 'vue-router'
import { ref } from 'vue';
import HomeView from '@/views/HomeView.vue'
import AdminDBView from '@/views/AdminDBView.vue'

import propietarios_routes from './propietarios_routes'
import especies_routes from './especies_routes'
import mascotas_routes from './mascotas_routes'
import especialidades_routes from './especialidades_routes'
import veternarios_routes from './veterinarios_routes'
import atenciones_routes from './atenciones_routes'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  ...propietarios_routes,
  ...especies_routes,
  ...mascotas_routes,
  ...especialidades_routes,
  ...veternarios_routes,
  ...atenciones_routes,
  {
    path: '/admin_db',
    name: 'admin_db',
    component: AdminDBView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export const recargarBD = ref(true)

router.beforeEach((to, from) => {
  // Analizar la ruta anterior y la actual para ver si se cambia de seccion.
  // Si se cambia de seccion: recargarBD.value = true (se lee de la BD)
  // Si se continua en la misma seccion no se hace nada (depende de los 
  // componentes de esa seccion setearlo a true (forzar lectura de la BD), o a false (usar store)
  const entidadActual = to.name?.toString().split('_')[0];
  const entidadAnterior = from.name?.toString().split('_')[0];

  if (entidadActual !== entidadAnterior || to.name === from.name) {
    recargarBD.value = true; 
  } else {
    //para intentar detectar falla de q recargarBD pasaba misteriosamente a false
    console.log(`Navegación interna en ${entidadActual}`)

    // recargarBD.value = false; <- posible culpable de la falla de no leer BD cdo debia
  }
  console.log(`Navegando aRecargar BD: ${recargarBD.value}`);
});

export default router