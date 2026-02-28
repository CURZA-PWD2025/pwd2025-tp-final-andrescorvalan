const mascotas_routes = [
  {
    path: '/mascotas',
    name: 'mascotas',
    component: () => import('../views/MascotasView.vue'),
    children: [
      {
        path: '',
        name: 'mascotas_list',
        component: () => import('../components/Mascotas/MascotasList.vue'),
      },
      {
        path: ':id/show',
        name: 'mascotas_show',
        component: () => import('../components/Mascotas/MascotasShow.vue'),
      },
      {
        path: 'create',
        name: 'mascotas_create',
        component: () => import('../components/Mascotas/MascotasCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'mascotas_update',
        component: () => import('../components/Mascotas/MascotasUpdate.vue'),
      },
    ],
  },
]
export default mascotas_routes
