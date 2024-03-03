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
      // component: () => import('../components/Login-Signup/LoginMobile.vue')
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
      path:'/adopt',
      name:'adopt',
      component: () => import('../views/AdoptView.vue')
    },
    {
      path:'/checkout',
      name:'checkout',
      component: () => import('../views/CheckoutView.vue')
    }
  ]
})

export default router
