const especies_routes = [
  {
    path: '/especies',
    name: 'especies',
    component: () => import('../views/EspeciesView.vue'),
    children: [
      {
        path: '',
        name: 'especies_list',
        component: () => import('../components/Especies/EspeciesList.vue'),
      },
      {
        path: ':id/show',
        name: 'especies_show',
        component: () => import('../components/Especies/EspeciesShow.vue'),
      },
      {
        path: 'create',
        name: 'especies_create',
        component: () => import('../components/Especies/EspeciesCreate.vue'),
      },
      {
        path: 'update/:id/edit',
        name: 'especies_update',
        component: () => import('../components/Especies/EspeciesUpdate.vue'),
      },
    ],
  },
]
export default especies_routes
