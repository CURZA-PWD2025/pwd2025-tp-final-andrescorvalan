const propietarios_routes = [
  {
    path: '/propietarios',
    component: () => import('@/views/PropietariosView.vue'),
    redirect: { name: 'propietarios_list' },
    children: [
      {
        path: '',
        name: 'propietarios_list',
        component: () => import('@/components/entidades/propietarios/PropietariosList.vue'),
      },
      {
        path: ':id/show',
        name: 'propietarios_show',
        component: () => import('@/components/entidades/propietarios/PropietariosShow.vue'),
      },
      {
        path: 'create',
        name: 'propietarios_create',
        component: () => import('@/components/entidades/propietarios/PropietariosCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'propietarios_update',
        component: () => import('@/components/entidades/propietarios/PropietariosUpdate.vue'),
      },
    ],
  },
]
export default propietarios_routes
