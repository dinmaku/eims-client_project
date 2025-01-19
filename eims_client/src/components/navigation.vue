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
                <a href="/suppliers-profile" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200">Suppliers Profile</a>
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
                  <a href="#" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1">Customer Support</a>
                  <a href="/booked-services" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1">My Bookings</a>
                  <a href="/vendor-schedule" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1">Booked Schedules</a>
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

  <section class="w-full h-[500px] bg-gray-50">
    <div class="w-full h-[500px] bg-gray-700">
      <div class = "flex justify-between m-5">
         <div class = "flex flex-col my-5 space-y-2">
            <p class ="text-md font-medium font-poppins text-gray-300">Contact Us</p>
            <span class = "text-md md:text-2xl font-semibold text-white font-poppins indent-5">09123456781</span>
            <span class = "text-md md:text-2xl font-semibold text-white font-poppins indent-5">225-0665</span>
         </div>
        <div class = "flex flex-col text-center my-5 space-y-2">
          <p class ="text-md font-medium font-poppins text-gray-300">Email us for support</p>
          <span class ="text-md md:text-2xl font-medium font-raleway text-yellow-300 ml-3">redcarpet.events@gmail.com</span>
      </div>
         <div class = "flex flex-col text-center my-5 space-y-2 mx-7">
        <p class ="text-md font-medium font-poppins text-gray-300">Follow us on</p>
        <div class = "flex items-center space-x-2">
            <a href="#" class = "text-xl font-semibold text-white font-poppins"><img src="/img/facebook.png" alt="facebook-logo" class="h-6 w-6 md:h-8 md:w-8 transition-transform duration-300 transform hover:scale-110"></a>
            <a href="#" class = "text-xl font-semibold text-white font-poppins"><img src="/img/instagram-black.png" alt="instagram-logo" class="h-6 w-6 md:h-8 md:w-8 transition-transform duration-300 transform hover:scale-110"></a>
            <a href="#" class = "text-xl font-semibold text-white font-poppins"><img src="/img/twitter.png" alt="twitter-logo" class="h-6 w-6 md:h-8 md:w-8 transition-transform duration-300 transform hover:scale-110"></a>
            <a href="#" class = "text-xl font-semibold text-white font-poppins"><img src="/img/linkedin.png" alt="twitter-logo" class="h-6 w-6 md:h-8 md:w-8 transition-transform duration-300 transform hover:scale-110"></a>
          </div>  
        </div>
       
        
      </div>
      <hr class="border-t border-gray-300 my-8 w-[90%] mx-auto" />

      <div class="flex justify-between m-5 mx-7">
    <div class="flex flex-col my-5">
        <h1 class="text-5xl font-semibold text-gray-50 font-dancing mb-5">RedCarpet</h1>
        <p class="text-start text-sm md:text-md font-medium text-gray-200 font-raleway">
            "From all of us, we believe every occasion deserves to be extraordinary. 
           <p class ="text-start text-sm md:text-md font-medium text-gray-200 font-raleway"> We appreciate your trust in us to make your events remarkable and </p>
           <p class ="text-start text-sm md:text-md font-medium text-gray-200 font-raleway"> look forward to bringing even more brilliance to your future celebrations."</p>
        </p>
    </div>
    <div class="flex flex-col text-center space-y-5 ml-5">
      <p class = "text-md font-medium font-poppins text-gray-300 ml">Explore</p>
      <ul class ="font-semibold text-lg text-center text-gray-50 space-y-1">
        <li class="transition-transform duration-300 transform hover:scale-105 hover:underline" ><a href="">About Us</a></li>
        <li class="transition-transform duration-300 transform hover:scale-105 hover:underline" ><a href="">OurTeam</a></li>
        <li class="transition-transform duration-300 transform hover:scale-105 hover:underline" ><a href="">Gallery</a></li>
      </ul>
    </div>

    <div class="flex flex-col items-end space-y-3 mt-10 mx-4 md:mt-20 md:mx-7">
      <p class="font-semibold font-poppins text-gray-200 text-center md:text-right">
        &copy; 2024 Red Carpet Services. All rights reserved.
      </p>
      <p class="font-semibold font-poppins text-gray-200 text-center md:text-right">
        @MSU, Naawan
      </p>
    </div>

</div>

    </div>
    
  </section>

  
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
      const isAttireCatalog = route === '/attire-catalog';
      const isBookedServices = route === '/booked-services';  // Check for /booked-services route
      const isVendorSchedule = route === '/vendor-schedule';  // Check for /vendor-schedule route
      const isScrolled = this.isScrolled || (isAttireCatalog && window.scrollY > 0);

      // Apply bg-black if on /booked-services, /vendor-schedule, or if scrolled or on /add-wishlist
      return isBookedServices || isVendorSchedule || isScrolled || route === '/add-wishlist'
        ? 'bg-black bg-opacity-60'
        : 'bg-transparent';
    }
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