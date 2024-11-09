<template>
  <nav :class="navClass" class="fixed w-full z-20 transition-colors duration-300">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-2">
      <img src="/img/logo.png" class="h-24" alt="RedCarpet Logo" />
      <button
        @click="toggleNavbar"
        type="button"
        class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-100 rounded-lg md:hidden hover:bg-gray-00 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
        aria-controls="navbar-default"
        :aria-expanded="isNavbarOpen.toString()"
      >
        <span class="sr-only">Open main menu</span>
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="#cccccc" viewBox="0 0 17 14">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
        </svg>
      </button>
      <div :class="{'hidden': !isNavbarOpen, 'w-full': true, 'md:block': true, 'md:w-auto': true}" id="navbar-default">
        <ul class="font-medium flex flex-col items-center p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg- md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
          <li>
            <a href="/" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-yellow-400 md:p-0 dark:text-white md:dark:text-blue-500" aria-current="page">Home</a>
          </li>
          <li class="relative">
            <a href="#" @click.prevent="toggleServices" class="block py-2 px-3 text-gray-100 rounded hover:text-gray-200 md:border-0 md:p-0 dark:text-gray-600 dark:hover:text-gray-200">Services</a>
              <!-- Dropdown Menu -->
              <div v-if="isDropdownVisible" class="absolute right-[-90px] z-10 mt-5 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <div class="py-1 text-left" role="none">
    
                <a href="/package-deal" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200">Package Deals</a>

                <a href="/attire-catalog" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200">Attire Rentals</a>
              </div>
              </div>
            </li>

          <li>
            <a href="#" class="block py-2 px-3 text-gray-100 rounded hover:text-gray-300 md:border-0 md:p-0 dark:text-white dark:hover:text-gray-200">About</a>
          </li>
          <li>
            <a href="#" class="block py-2 px-3 text-gray-100 rounded hover:text-gray-300 md:border-0 md:p-0 dark:text-white dark:hover:text-gray-200">Contact</a>
          </li>

          <!-- Conditionally render based on login status -->
          <li v-if="!loggedIn">
            <button @click="showLoginForm" class="block py-2 px-3 text-gray-100 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-black md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">
              Login
            </button>
            <LoginRegister 
            :loginForm="loginModalForm" 
            @close="hideModal" 
            @update:loginForm="val => loginModalForm = val"
            @loginSuccess="handleLoginSuccess"
          />
          </li>
          
          <!-- Profile Dropdown when logged in -->
          <li v-else>
            <div class="relative">
              <div class="flex items-center justify-start space-x-4" @click="toggleDrop">
                <img class="w-9 h-9 rounded-full border-2 border-gray-50 bg-white cursor-pointer" src="/img/ID.jpg" alt="">
                <div class="font-semibold text-gray-100 dark:text-white text-left">
                  <div>Dean Mark</div>
                </div>
              </div>
              
              <!-- Drop down -->
              <div v-show="showDropDown" class="absolute right-[-50px] z-10 mt-3 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
                <div class="py-1 text-left" role="none">
                  <a href="#" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1">Account settings</a>
                  <a href="#" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1">Support</a>
                  <a href="#" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1">License</a>
                  <router-link to="/">
                    <button 
                      @click="handleLogout" 
                      class="text-gray-700 block w-full px-4 py-2 text-left text-sm hover:bg-gray-200" 
                      role="menuitem" 
                      tabindex="-1">
                      Sign out
                    </button>
                  </router-link>
                </div>
              </div>
            </div>
          </li>
        </ul>

      </div>
    </div>
  </nav>

  <router-view></router-view>
</template>

<script>
import LoginRegister from '../pages/login-register.vue';

export default {
  name: 'ClientNavigation',
  components: { LoginRegister },
  data() {
    return {
      isMenuOpen: false,
      isScrolled: false,
      loginModalForm: false,
      isNavbarOpen: false,
      loggedIn:localStorage.getItem('loggedIn') === 'true',
      showDropDown: false,
      isDropdownVisible: false,
    };
  },
  computed: {
    navClass() {
      const route = this.$route.path;
      return this.isScrolled || route === '/add-wishlist' ? 'bg-black bg-opacity-50' : 'bg-transparent' || route === '/package-deal' ? 'bg-black bg-opacity-20' : 'bg-transparent';
    },
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
    this.loggedIn = localStorage.getItem('loggedIn') === 'true';
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen; 
    },
    handleScroll() {
      this.isScrolled = window.scrollY > 0;
    },
    showLoginForm() {
      this.loginModalForm = true;
    },
    hideModal() {
      this.loginModalForm = false; // Ensure this is reset as well
    },
    handleLoginSuccess() {
      this.loggedIn = true;  // Set logged in state to true
      localStorage.setItem('loggedIn', 'true'); 
      this.showDropDown = false;  // Ensure dropdown is hidden after login
      this.loginModalForm = false;  // Close login modal
    },
    toggleDrop() {
      this.showDropDown = !this.showDropDown;
    },
    handleLogout() {
      this.loggedIn = false; // Update Vue component state
      localStorage.removeItem('loggedIn'); // Remove login status from localStorage
      this.showDropDown = false; // Close dropdown
      this.$router.push('/'); // Optionally redirect to home or login page
      },
      toggleServices() {
      this.isDropdownVisible = !this.isDropdownVisible;
    },
  },
};
</script>

<style scoped>
/* Add your styles here if needed */
</style>