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

              <div class="text-center my-3">
                <a 
                  class="text-xs text-indigo-500 italic hover:underline hover:text-indigo-600 font-medium" 
                  href="#"
                  @click.prevent="viewSupplierDetails(supplier)"
                >
                  View Profile
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