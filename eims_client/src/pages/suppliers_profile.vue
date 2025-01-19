<template>
  <div class="min-h-screen bg-gray-500 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto mt-20">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Our Suppliers</h1>
      
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

      <div v-if="suppliers.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Supplier Card -->
        <div v-for="supplier in suppliers" :key="supplier.supplier_id" 
             class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 w-full h-[600px] flex flex-col">
          <!-- Image Container - Fixed Height -->
          <div class="h-48 overflow-hidden">
            <img 
              :src="supplier.user_img || '/default-profile.jpg'" 
              :alt="supplier.firstname + ' ' + supplier.lastname"
              class="w-full h-full object-cover"
              @error="handleImageError"
            />
          </div>
          <!-- Content Container - Scrollable if content overflows -->
          <div class="p-6 flex-1 flex flex-col overflow-auto">
            <h2 class="text-xl font-semibold text-gray-800 mb-2">
              {{ supplier.firstname || 'Unknown' }} {{ supplier.lastname || '' }}
            </h2>
            <div class="space-y-2 flex-1 overflow-auto">
              <p v-if="supplier.service" class="text-gray-600">
                <span class="font-medium">Service:</span> {{ supplier.service }}
              </p>
              <p v-if="supplier.price" class="text-gray-600">
                <span class="font-medium">Price:</span> ₱{{ supplier.price.toLocaleString() }}
              </p>
              <p v-if="supplier.contactnumber" class="text-gray-600">
                <span class="font-medium">Contact:</span> {{ supplier.contactnumber }}
              </p>
              <p v-if="supplier.email" class="text-gray-600">
                <span class="font-medium">Email:</span> {{ supplier.email }}
              </p>
              <p v-if="supplier.address" class="text-gray-600">
                <span class="font-medium">Address:</span> {{ supplier.address }}
              </p>
              <p v-if="supplier.status" class="text-gray-600">
                <span class="font-medium">Status:</span> 
                <span :class="{
                  'text-green-600': supplier.status.toLowerCase() === 'active',
                  'text-red-600': supplier.status.toLowerCase() === 'inactive'
                }">
                  {{ supplier.status }}
                </span>
              </p>
            </div>
            
            <!-- Social Media Links - Fixed at Bottom -->
            <div v-if="supplier.social_media && supplier.social_media.length > 0" class="mt-4">
              <p class="font-medium text-gray-700 mb-2">Social Media:</p>
              <div class="flex space-x-3">
                <a v-for="social in supplier.social_media" 
                   :key="social.platform + social.handle"
                   :href="social.url || getSocialUrl(social.platform, social.handle)"
                   target="_blank"
                   class="text-gray-600 hover:opacity-80 transition-opacity"
                   :title="social.platform">
                  <img 
                    :src="getSocialIcon(social.platform)" 
                    :alt="social.platform"
                    class="w-6 h-6 object-contain"
                  />
                </a>
              </div>
            </div>

            <!-- Buttons - Fixed at Bottom -->
            <div class="mt-4 space-y-2">
              <button 
                v-if="supplier.status?.toLowerCase() === 'active'"
                class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors duration-300">
                Contact Supplier
              </button>
              <button class="w-full border border-blue-600 text-blue-600 py-2 px-4 rounded-md hover:bg-blue-50 transition-colors duration-300">
                View Details
              </button>
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
      error: null
    };
  },
  methods: {
    getSocialIcon(platform) {
      const icons = {
        'facebook': '/img/facebook.png',
        'instagram': '/img/instagram-black.png',
        'twitter': '/img/twitter.png',
        'linkedin': '/img/linkedin.png',
        'youtube': '/img/youtube.png',
        'pinterest': '/img/pinterest.png'
      };
      return icons[platform.toLowerCase()] || '/img/link.png';
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
          this.suppliers = response.data.data;
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
</style>