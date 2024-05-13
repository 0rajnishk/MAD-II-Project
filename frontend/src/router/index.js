import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/admin',
      name: 'adminDashboard',
      component: () => import('../views/AdminDashboard.vue')
    },
    {
      path: '/adminlogin',
      name: 'adminlogin',
      component: () => import('../components/admin/AdminLogin.vue')
    },
    {
      path:'/register',
      name:'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path:'/dashboard',
      name:'dashboard',
      component: () => import('../views/DashboardView.vue')
    },
    {
      path:'/checkout',
      name:'checkout',
      component: () => import('../views/CheckoutView.vue')
    },
    {
      path: '/play',
      name: 'audio',
      component: () => import('../components/AudioPlayer.vue')
    },
    {
      path: '/playlist/:id',
      name: 'playlist',
      component: () => import('../views/PlaylistView.vue')
    },
    {
      path: '/search/:query',
      name: 'search',
      component: () => import('../views/SearchView.vue')
    },
    {
      path: '/admin/search/:query',
      name: 'adminsearch',
      component: () => import('../views/SearchAdminView.vue')
    },
    {
      path: '/album/:id',
      name: 'album',
      component: () => import('../views/AlbumView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
    },

  ]
})

export default router
