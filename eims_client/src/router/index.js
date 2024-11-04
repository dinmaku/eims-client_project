import { createRouter, createWebHistory } from 'vue-router';
import ClientNavigation from '../components/navigation.vue';
import Home from '../pages/home.vue'
import Wishlist from  '../pages/add-wishlist.vue';
import LoginRegister from '../pages/login-register.vue';

const routes = [
  {
    path: '/',
    component: ClientNavigation, // Assuming you want the navigation for the root
    children: [
      {
        path: '',
        component: Home, // This will be displayed at '/'
      },
      {
        path: 'add-wishlist',
        name: 'Wishlist',
        component: Wishlist,
        meta: {
          title: 'Wishlist',
        },
      },
      {
        path: 'login-register',
        name: 'LoginRegister',
        component: LoginRegister,
        meta: {
          title: 'Login',
        },
      },
    ],
  },
];
  



const router = Router();
export default router;
function Router() {
  const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  return router;
}

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'RedCarpet';
  next();
});