<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto mt-20">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Our Suppliers</h1>
      
      <!-- Filter Button and Dropdown -->
      <div class="filter-container flex items-center mb-6 relative">
        <button 
          @click.stop="toggleFilter" 
          class="flex items-center hover:bg-gray-400 p-2 rounded-lg bg-gray-600 text-white"
        >
          <i class="fas fa-filter h-5 w-5"></i>
          <span class="ml-2 text-md font-medium">Filters</span>
        </button>
        
        <!-- Filter Dropdown -->
        <div 
          v-if="showFilter" 
          @click.stop
          class="absolute top-12 left-0 bg-white shadow-lg rounded-lg p-4 z-[1] min-w-[200px]"
        >
          <div class="space-y-2">
            <button 
              @click="filterByService('all')"
              :class="['w-full text-left px-4 py-2 rounded-lg', 
                selectedService === 'all' ? 'bg-indigo-100 text-indigo-700' : 'hover:bg-gray-100']"
            >
              All Services
            </button>
            <button 
              v-for="service in uniqueServices" 
              :key="service"
              @click="filterByService(service)"
              :class="['w-full text-left px-4 py-2 rounded-lg', 
                selectedService === service ? 'bg-indigo-100 text-indigo-700' : 'hover:bg-gray-100']"
            >
              {{ service || 'Uncategorized' }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Loading Message -->
      <div v-if="!suppliers.length && !error" class="text-center text-gray-600 py-8">
        Loading suppliers...
      </div>

      <!-- No Suppliers Message -->
      <div v-if="suppliers.length === 0 && !error" class="text-center text-gray-600 py-8">
        No suppliers available at the moment.
      </div>

      <div v-if="suppliers.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Supplier Card -->
        <div v-for="supplier in suppliers" :key="supplier.supplier_id" class="max-w-xs">
          <div class="bg-white shadow-xl rounded-lg py-3">
            <div class="photo-wrapper p-2">
              <img 
                class="w-32 h-32 rounded-full mx-auto object-cover" 
                :src="supplier.user_img || '/default-profile.jpg'" 
                :alt="supplier.firstname + ' ' + supplier.lastname"
                @error="handleImageError"
              />
            </div>
            <div class="p-2">
              <h3 class="text-center text-xl text-gray-900 font-medium leading-8">
                {{ supplier.firstname || 'Unknown' }} {{ supplier.lastname || '' }}
              </h3>
              <div class="text-center text-gray-400 text-xs font-semibold">
                <p>{{ supplier.service || 'Service Provider' }}</p>
              </div>
              <table class="text-xs my-3">
                <tbody>
                  <tr v-if="supplier.address">
                    <td class="px-2 py-2 text-gray-500 font-semibold">Address</td>
                    <td class="px-2 py-2">{{ supplier.address }}</td>
                  </tr>
                  <tr v-if="supplier.contactnumber">
                    <td class="px-2 py-2 text-gray-500 font-semibold">Phone</td>
                    <td class="px-2 py-2">{{ supplier.contactnumber }}</td>
                  </tr>
                  <tr v-if="supplier.email">
                    <td class="px-2 py-2 text-gray-500 font-semibold">Email</td>
                    <td class="px-2 py-2">{{ supplier.email }}</td>
                  </tr>
                  <tr v-if="supplier.price">
                    <td class="px-2 py-2 text-gray-500 font-semibold">Price</td>
                    <td class="px-2 py-2">₱{{ supplier.price.toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>

              <!-- Social Media Icons -->
              <div class="text-center my-3 flex justify-center space-x-4">
                <a 
                  v-for="social in supplier.social_media" 
                  :key="social.platform"
                  :href="getSocialUrl(social.platform, social.handle)"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-gray-600 hover:text-indigo-600 transition-colors duration-200"
                >
                  <i :class="getSocialIcon(social.platform)" class="text-xl"></i>
                </a>
              </div>

              <!-- Status Badge -->
              <div v-if="supplier.status" class="text-center">
                <span :class="{
                  'text-green-600': supplier.status.toLowerCase() === 'active',
                  'text-red-600': supplier.status.toLowerCase() === 'inactive'
                }" class="text-xs font-semibold">
                  {{ supplier.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// Configure axios defaults
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true;

export default {
  name: 'Suppliers Profile',
  data() {
    return {
      suppliers: [],
      allSuppliers: [], // Store all suppliers
      error: null,
      showFilter: false,
      selectedService: 'all'
    };
  },
  computed: {
    uniqueServices() {
      // Include null/undefined services as 'Uncategorized'
      const services = this.allSuppliers.map(supplier => supplier.service || 'Uncategorized');
      return [...new Set(services)].sort();
    }
  },
  methods: {
    toggleFilter() {
      this.showFilter = !this.showFilter;
    },
    filterByService(service) {
      this.selectedService = service;
      if (service === 'all') {
        this.suppliers = [...this.allSuppliers];
      } else if (service === 'Uncategorized') {
        this.suppliers = this.allSuppliers.filter(supplier => !supplier.service);
      } else {
        this.suppliers = this.allSuppliers.filter(supplier => supplier.service === service);
      }
      this.showFilter = false;
    },
    getSocialIcon(platform) {
      const icons = {
        'facebook': 'fab fa-facebook',
        'instagram': 'fab fa-instagram',
        'twitter': 'fab fa-twitter',
        'linkedin': 'fab fa-linkedin',
        'youtube': 'fab fa-youtube',
        'tiktok': 'fab fa-tiktok',
        'pinterest': 'fab fa-pinterest'
      };
      return icons[platform.toLowerCase()] || 'fas fa-link';
    },
    getSocialUrl(platform, handle) {
      const baseUrls = {
        'facebook': 'https://facebook.com/',
        'instagram': 'https://instagram.com/',
        'twitter': 'https://twitter.com/',
        'linkedin': 'https://linkedin.com/in/',
        'youtube': 'https://youtube.com/@',
        'tiktok': 'https://tiktok.com/@',
        'pinterest': 'https://pinterest.com/'
      };
      return baseUrls[platform.toLowerCase()] ? baseUrls[platform.toLowerCase()] + handle : '#';
    },
    handleImageError(e) {
      e.target.src = '/default-profile.jpg';
    },
    async fetchSuppliers() {
      try {
        const response = await axios.get('/api/suppliers');
        console.log('API Response:', response.data);
        if (response.data && response.data.status === 'success') {
          this.allSuppliers = response.data.data;
          this.suppliers = [...this.allSuppliers];
          this.error = null;
        } else {
          this.error = response.data?.message || 'Failed to fetch suppliers';
          console.error('Error:', this.error);
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message;
        console.error('Error fetching suppliers:', error);
      }
    }
  },
  async created() {
    await this.fetchSuppliers();
  },
  mounted() {
    // Close filter dropdown when clicking outside
    document.addEventListener('click', () => {
      this.showFilter = false;
    });
  },
  beforeUnmount() {
    // Clean up event listener
    document.removeEventListener('click', () => {
      this.showFilter = false;
    });
  }
};
</script>

<style scoped>
/* Hide scrollbar for Chrome, Safari and Opera */
.overflow-auto::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.overflow-auto {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.card-image {
  transition: transform 0.3s ease;
}

.card:hover .card-image {
  transform: scale(1.05);
}

/* Add these new styles */
.filter-container {
  position: relative;
  display: inline-block;
  z-index: 1;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>