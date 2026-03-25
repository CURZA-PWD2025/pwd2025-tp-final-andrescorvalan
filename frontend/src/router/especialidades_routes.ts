const especialidades_routes = [
  {
    path: '/especialidades',
    name: 'especialidades',
    component: () => import('@/views/EspecialidadesView.vue'),
    children: [
      {
        path: '',
        name: 'especialidades_list',
        component: () => import('@/components/entidades/especialidades/EspecialidadesList.vue'),
      },
      {
        path: ':id/show',
        name: 'especialidades_show',
        component: () => import('@/components/entidades/especialidades/EspecialidadesShow.vue'),
      },
      {
        path: 'create',
        name: 'especialidades_create',
        component: () => import('@/components/entidades/especialidades/EspecialidadesCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'especialidades_update',
        component: () => import('@/components/entidades/especialidades/EspecialidadesUpdate.vue'),
      },
    ],
  },
]
export default especialidades_routes
