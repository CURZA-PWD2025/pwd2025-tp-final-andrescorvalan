const veterinarioes_routes = [
  {
    path: '/veterinarios',
    name: 'veterinarios',
    component: () => import('../views/VeterinariosView.vue'),
    children: [
      {
        path: '',
        name: 'veterinarios_list',
        component: () => import('../components/Veterinarios/VeterinariosList.vue'),
      },
      {
        path: ':id/show',
        name: 'veterinarios_show',
        component: () => import('../components/Veterinarios/VeterinariosShow.vue'),
      },
      {
        path: 'create',
        name: 'veterinarios_create',
        component: () => import('../components/Veterinarios/VeterinariosCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'veterinarios_update',
        component: () => import('../components/Veterinarios/VeterinariosUpdate.vue'),
      },
    ],
  },
]
export default veterinarioes_routes
