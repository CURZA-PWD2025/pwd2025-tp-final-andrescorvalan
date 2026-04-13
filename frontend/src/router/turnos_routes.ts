const turnos_routes = [
  {
    path: '/turnos',
    component: () => import('@/views/TurnosView.vue'),
    redirect: { name: 'turnos_proximos' },
    children: [
      {
        path: '',
        name: 'turnos_proximos',
        component: () => import('@/components/entidades/turnos/TurnosList.vue'),
      },
      {
        path: ':id/show',
        name: 'turnos_show',
        component: () => import('@/components/entidades/turnos/TurnosShow.vue'),
      },
      {
        path: 'create',
        name: 'turnos_create',
        component: () => import('@/components/entidades/turnos/TurnosCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'turnos_update',
        component: () => import('@/components/entidades/turnos/TurnosUpdate.vue'),
      },
    ],
  },
]
export default turnos_routes