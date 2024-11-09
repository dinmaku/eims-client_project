<template>
  <div class="h-screen flex items-center justify-center bg-gray-500 ">
    <div class="w-full h-full overflow-y-auto">
      <div class="mt-32 ml-5">
        <h1 class="md:text-3xl font-raleway font-semibold text-gray-50">Gowns and Tuxedo</h1>
        <div class="flex items-center space-x-10 m-10">
          <button class="flex items-center hover:bg-gray-400 p-1 rounded-lg">
            <img src="/img/filter.png" class="h-6" />
            <span class="ml-2 text-md font-medium text-gray-200 font-amaticRegular">Filters</span>
          </button>

          <select class="h-9 bg-gray-100 text-sm border border-gray-300 text-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-28">
            <option value="" disabled selected>Sort</option>
            <option value="trending">Recommended</option>
            <option value="newest">Newest</option>
            <option value="popular">Most Popular</option>
          </select>

          <p class="text-gray-50 italic">46 <span>results</span></p>
        </div>

        <!-- Outfit grid container -->
        <div class="outfit-container grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-4 w-full">
          <div v-for="outfit in outfits" :key="outfit.outfit_id" class="outfit-card bg-white border rounded-lg shadow-lg p-4 flex flex-col h-full">
            <!-- Outfit Image -->
            <img :src="outfit.outfit_img" alt="Outfit Image" class="w-full h-60 object-cover rounded-lg mb-4" />

            <!-- Outfit Name and Description -->
            <h3 class="text-xl font-semibold mb-2">{{ outfit.outfit_name }}</h3>
            <p class="text-gray-700 mb-2">{{ outfit.outfit_desc }}</p>

            <!-- Price and Status -->
            <div class="flex flex-col flex-grow justify-between">
              <p class="text-gray-900 font-bold">Price: {{ outfit.rent_price }}</p>
              <p :class="{'text-green-600': outfit.status === 'available', 'text-red-600': outfit.status !== 'available'}" class="mt-2">
                {{ outfit.status }}
              </p>
            </div>
          </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AttireCatalog', 
  data() {
    return {
      outfits: []  // Array to hold outfit data
    };
  },
  mounted() {
    this.fetchOutfits();
  },
  methods: {
    async fetchOutfits() {
          try {
            const token = localStorage.getItem('access_token');  // Assuming the JWT token is stored in localStorage
            const response = await axios.get('http://127.0.0.1:5000/outfits', {
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  // Send the JWT token
              },
              withCredentials: true  // Send cookies with the request if needed
            });
            this.outfits = response.data;  // Populate outfits array with data from API
          } catch (error) {
            console.error('Error fetching outfits:', error);
          }
        },
  }
};
</script>

<style scoped>
.outfit-card {
  transition: transform 0.3s ease;
}

.outfit-card:hover {
  transform: scale(1.05);
}

.outfit-container {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* Responsive grid layout */
}
</style>
