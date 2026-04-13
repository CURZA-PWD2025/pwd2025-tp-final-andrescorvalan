const veterinarios_routes = [
  {
    path: '/veterinarios',
    component: () => import('@/views/VeterinariosView.vue'),
    redirect: { name: 'veterinarios_list' },
    children: [
      {
        path: '',
        name: 'veterinarios_list',
        component: () => import('@/components/entidades/veterinarios/VeterinariosList.vue'),
      },
      {
        path: ':id/show',
        name: 'veterinarios_show',
        component: () => import('@/components/entidades/veterinarios/VeterinariosShow.vue'),
      },
      {
        path: 'create',
        name: 'veterinarios_create',
        component: () => import('@/components/entidades/veterinarios/VeterinariosCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'veterinarios_update',
        component: () => import('@/components/entidades/veterinarios/VeterinariosUpdate.vue'),
      },
    ],
  },
]
export default veterinarios_routes
