const propietarios_routes = [
  {
    path: '/propietarios',
    name: 'propietarios',
    component: () => import('../views/PropietariosView.vue'),
    children: [
      {
        path: '',
        name: 'propietarios_list',
        component: () => import('../components/Propietarios/PropietariosList.vue'),
      },
      {
        path: ':id/show',
        name: 'propietarios_show',
        component: () => import('../components/Propietarios/PropietariosShow.vue'),
      },
      {
        path: 'create',
        name: 'propietarios_create',
        component: () => import('../components/Propietarios/PropietariosCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'propietarios_update',
        component: () => import('../components/Propietarios/PropietariosUpdate.vue'),
      },
    ],
  },
]
export default propietarios_routes
