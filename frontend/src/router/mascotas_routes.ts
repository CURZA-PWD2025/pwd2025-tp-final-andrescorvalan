const mascotas_routes = [
  {
    path: '/mascotas',
    component: () => import('@/views/MascotasView.vue'),
    redirect: { name: 'mascotas_list' },
    children: [
      {
        path: '',
        name: 'mascotas_list',
        component: () => import('@/components/entidades/mascotas/MascotasList.vue'),
      },
      {
        path: ':id/show',
        name: 'mascotas_show',
        component: () => import('@/components/entidades/mascotas/MascotasShow.vue'),
      },
      {
        path: 'create',
        name: 'mascotas_create',
        component: () => import('@/components/entidades/mascotas/MascotasCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'mascotas_update',
        component: () => import('@/components/entidades/mascotas/MascotasUpdate.vue'),
      },
    ],
  },
]
export default mascotas_routes
