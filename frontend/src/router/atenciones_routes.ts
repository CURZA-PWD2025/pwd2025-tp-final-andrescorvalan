const atenciones_routes = [
  {
    path: '/atenciones',
    component: () => import('@/views/AtencionesView.vue'),
    redirect: { name: 'atenciones_list' },
    children: [
      {
        path: '',
        name: 'atenciones_list',
        component: () => import('@/components/entidades/atenciones/AtencionesList.vue'),
      },
      {
        path: ':id/show',
        name: 'atenciones_show',
        component: () => import('@/components/entidades/atenciones/AtencionesShow.vue'),
      },
      {
        path: 'create',
        name: 'atenciones_create',
        component: () => import('@/components/entidades/atenciones/AtencionesCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'atenciones_update',
        component: () => import('@/components/entidades/atenciones/AtencionesUpdate.vue'),
      },
    ],
  },
]
export default atenciones_routes
