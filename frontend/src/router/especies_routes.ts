const especies_routes = [
  {
    path: '/especies',
    component: () => import('@/views/EspeciesView.vue'),
    redirect: { name: 'especies_list' },
    children: [
      {
        path: '',
        name: 'especies_list',
        component: () => import('@/components/entidades/especies/EspeciesList.vue'),
      },
      {
        path: ':id/show',
        name: 'especies_show',
        component: () => import('@/components/entidades/especies/EspeciesShow.vue'),
      },
      {
        path: 'create',
        name: 'especies_create',
        component: () => import('@/components/entidades/especies/EspeciesCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'especies_update',
        component: () => import('@/components/entidades/especies/EspeciesUpdate.vue'),
      },
    ],
  },
]
export default especies_routes
