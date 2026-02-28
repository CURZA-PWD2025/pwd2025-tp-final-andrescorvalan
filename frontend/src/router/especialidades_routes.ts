const especialidades_routes = [
  {
    path: '/especialidades',
    name: 'especialidades',
    component: () => import('../views/EspecialidadesView.vue'),
    children: [
      {
        path: '',
        name: 'especialidades_list',
        component: () => import('../components/Especialidades/EspecialidadesList.vue'),
      },
      {
        path: ':id/show',
        name: 'especialidades_show',
        component: () => import('../components/Especialidades/EspecialidadesShow.vue'),
      },
      {
        path: 'create',
        name: 'especialidades_create',
        component: () => import('../components/Especialidades/EspecialidadesCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'especialidades_update',
        component: () => import('../components/Especialidades/EspecialidadesUpdate.vue'),
      },
    ],
  },
]
export default especialidades_routes
