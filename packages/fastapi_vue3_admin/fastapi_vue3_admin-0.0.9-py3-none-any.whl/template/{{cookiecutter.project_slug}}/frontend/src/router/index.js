import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../store/user';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { public: true },
  },
  {
    path: '/',
    component: () => import('../layouts/AdminLayout.vue'),
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
      },
      {
        path: 'staff/users',
        name: 'UserList',
        component: () => import('../views/staff/UserList.vue'),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const userStore = useUserStore();
  if (!to.meta?.public && !userStore.token) {
    return '/login';
  }
});

export default router; 