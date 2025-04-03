<template>
  <div class="pt-32 px-5 pb-5 bg-gray-100">
    <h1 class="md:text-3xl font-raleway font-semibold text-gray-500">Gowns and Tuxedo</h1>
    <div class="flex items-center space-x-10 m-10">
      <!-- Filter Button and Dropdown -->
      <div class="relative">
        <button 
          @click="toggleFilterDropdown" 
          class="filter-button flex items-center hover:bg-gray-400 p-1 rounded-lg"
        >
          <img src="/img/filter.png" class="h-6" />
          <span class="ml-2 text-md font-medium text-gray-700 font-amaticRegular">Filters</span>
        </button>
        
        <!-- Filter Dropdown -->
        <div 
          v-if="showFilterDropdown" 
          class="filter-dropdown absolute top-full left-0 mt-2 bg-white rounded-lg shadow-lg p-4 z-50 min-w-[200px]"
          @click.stop
        >
          <div class="space-y-4">
            <div>
              <h4 class="font-semibold mb-2">Outfit Type</h4>
              <div class="space-y-2">
                <label class="flex items-center space-x-2">
                  <input 
                    type="checkbox" 
                    v-model="selectedTypes" 
                    value="Gown"
                    class="rounded text-blue-500"
                  >
                  <span>Gowns</span>
                </label>
                <label class="flex items-center space-x-2">
                  <input 
                    type="checkbox" 
                    v-model="selectedTypes" 
                    value="Tuxedo"
                    class="rounded text-blue-500"
                  >
                  <span>Tuxedos</span>
                </label>
              </div>
            </div>
            
            <div>
              <h4 class="font-semibold mb-2">Status</h4>
              <div class="space-y-2">
                <label class="flex items-center space-x-2">
                  <input 
                    type="checkbox" 
                    v-model="selectedStatus" 
                    value="available"
                    class="rounded text-blue-500"
                  >
                  <span>Available</span>
                </label>
                <label class="flex items-center space-x-2">
                  <input 
                    type="checkbox" 
                    v-model="selectedStatus" 
                    value="unavailable"
                    class="rounded text-blue-500"
                  >
                  <span>Unavailable</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sort Dropdown -->
      <select 
        v-model="sortBy" 
        class="h-9 bg-gray-100 text-sm border border-gray-300 text-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-28"
      >
        <option value="" disabled>Sort</option>
        <option value="price-asc">Price: Low to High</option>
        <option value="price-desc">Price: High to Low</option>
        <option value="name-asc">Name: A to Z</option>
        <option value="name-desc">Name: Z to A</option>
      </select>

      <p class="text-gray-50 italic">{{ filteredOutfits.length }} <span>results</span></p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex justify-center items-center h-64">
      <div class="text-red-500 text-center">
        <p class="text-xl mb-2">{{ error }}</p>
        <button 
          @click="fetchOutfits" 
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Try Again
        </button>
      </div>
    </div>

    <!-- Outfit grid container -->
    <div v-else-if="filteredOutfits.length > 0" class="outfit-container grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-4 w-full">
      <div 
        v-for="outfit in filteredOutfits" 
        :key="outfit.outfit_id" 
        class="outfit-card bg-white border rounded-lg shadow-lg p-4 flex flex-col h-full cursor-pointer" 
        @click="showModal(outfit)"
      >
        <!-- Outfit Image -->
        <img :src="outfit.outfit_img" alt="Outfit Image" class="w-full h-60 object-cover rounded-lg mb-4" />

        <!-- Outfit Name and Description -->
        <h3 class="text-xl font-semibold mb-2">{{ outfit.outfit_name }}</h3>
      
        <!-- Price and Status -->
        <div class="flex flex-col flex-grow justify-between">
          <p class="text-yellow-400 font-medium">₱  {{ outfit.rent_price }}</p>
          <div class="flex justify-between">
            <p :class="{'text-green-600': outfit.status === 'available', 'text-red-600': outfit.status !== 'available'}" class="mt-2">
              {{ outfit.status }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- No Results Message -->
    <div v-else class="text-center py-8">
      <p class="text-gray-500 text-lg">No outfits found matching your filters.</p>
    </div>

    <!--Modal for Gown booking-->
    <div v-if="showGownDetailsModal" @click.self="closeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-[90%] md:max-w-[800px] max-h-[90vh] overflow-y-auto">
        <button @click="closeModal" class="text-gray-500 text-3xl float-right">&times;</button>
        <div class="flex flex-col md:flex-row ml-5 mt-10 space-x-5">
          <!-- Image Section -->
          <img :src="selectedOutfit.outfit_img" alt="Outfit Image" class="h-48 md:h-[25em] w-[350px] bg-gray-200 shadow-md rounded-lg" />
          
          <!-- Outfit Details Section -->
          <div class="flex flex-col mt-5 md:mt-0">
            <p class="text-gray-900 font-gothic font-semibold text-lg mb-2">Price: <span class="font-medium text-yellow-800">₱ {{ selectedOutfit.rent_price }}</span></p>
            <h3 class="text-2xl font-raleway font-medium text-gray-600">{{ selectedOutfit.outfit_name }}</h3>
            <p class="mt-3">Color: <span class="font-semibold">{{ selectedOutfit.outfit_color }}</span></p>
            <p class="mt-1">Size: <span class="font-semibold">{{ selectedOutfit.size }}</span></p>
            <p class="mt-1">Weight: <span class="font-semibold">{{ selectedOutfit.weight }}</span></p>
            <p class="mt-1">Category: <span class="font-semibold">{{ selectedOutfit.outfit_type }}</span></p>
            <p class="mt-3 text-sm italic text-gray-500">
              *** This item is available for purchase. Feel free to message us on our Facebook page to inquire about the price of this gown,
              or alternatively, you can reach us via email through our Contact Page.
            </p>
          </div>
        </div>

        <!-- Description Section -->
        <div class="ml-5 mt-7 flex-col space-y-3">
          <p class="font-medium">Description:</p>
          <p class="text-gray-700 text-lg">{{ selectedOutfit.outfit_desc }}</p>
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
      outfits: [],  // Array to hold outfit data
      showGownDetailsModal: false,
      selectedOutfit: null,
      pickup_date: '',
      return_date: '',
      bookForm: false,
      showFilterDropdown: false,
      selectedTypes: [],
      selectedStatus: [],
      sortBy: '',
      isLoading: true,
      error: null
    };
  },
  computed: {
    outfitsLength() {
      return this.outfits?.length || 0;
    },
    filteredOutfits() {
      if (!this.outfits) return [];
      
      let filtered = [...this.outfits];
      
      // Filter by outfit type
      if (this.selectedTypes.length > 0) {
        filtered = filtered.filter(outfit => 
          this.selectedTypes.includes(outfit.outfit_type)
        );
      }
      
      // Filter by status
      if (this.selectedStatus.length > 0) {
        filtered = filtered.filter(outfit => {
          const status = outfit.status === 'available' ? 'available' : 'unavailable';
          return this.selectedStatus.includes(status);
        });
      }
      
      // Sort outfits
      if (this.sortBy) {
        filtered.sort((a, b) => {
          switch (this.sortBy) {
            case 'price-asc':
              return a.rent_price - b.rent_price;
            case 'price-desc':
              return b.rent_price - a.rent_price;
            case 'name-asc':
              return a.outfit_name.localeCompare(b.outfit_name);
            case 'name-desc':
              return b.outfit_name.localeCompare(a.outfit_name);
            default:
              return 0;
          }
        });
      }
      
      return filtered;
    }
  },
  async created() {
    await this.fetchOutfits();
  },
  mounted() {
    // Close filter dropdown when clicking outside
    document.addEventListener('click', this.closeFilterDropdown);
  },
  beforeUnmount() {
    // Clean up event listener
    document.removeEventListener('click', this.closeFilterDropdown);
  },
  methods: {
    toggleFilterDropdown(event) {
      event.stopPropagation(); // Stop event from bubbling up
      this.showFilterDropdown = !this.showFilterDropdown;
    },
    closeFilterDropdown(event) {
      // Only close if clicking outside the dropdown
      const dropdown = document.querySelector('.filter-dropdown');
      const filterButton = document.querySelector('.filter-button');
      
      if (dropdown && !dropdown.contains(event.target) && 
          filterButton && !filterButton.contains(event.target)) {
        this.showFilterDropdown = false;
      }
    },
    async fetchOutfits() {
      this.isLoading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('access_token');
        const headers = {
          'Content-Type': 'application/json'
        };
        
        // Add authorization header only if token exists
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await axios.get('http://127.0.0.1:5000/outfits', {
          headers,
          withCredentials: true
        });
        
        console.log('API Response:', response.data); // Debug log
        this.outfits = response.data || [];
        console.log('Outfits after assignment:', this.outfits); // Debug log
        
      } catch (error) {
        console.error('Error fetching outfits:', error);
        this.error = 'Failed to load outfits. Please try again later.';
        this.outfits = [];
        
        // Handle specific error cases
        if (error.response?.status === 401 || error.response?.status === 422) {
          // User is not logged in or token is invalid - still try to fetch public data
          try {
            const response = await axios.get('http://127.0.0.1:5000/outfits', {
              headers: {
                'Content-Type': 'application/json'
              }
            });
            console.log('Public API Response:', response.data); // Debug log
            this.outfits = response.data || [];
            this.error = null;
          } catch (retryError) {
            console.error('Error fetching public outfits:', retryError);
            this.error = 'Failed to load outfits. Please try again later.';
            this.outfits = [];
          }
        }
      } finally {
        this.isLoading = false;
      }
    },
    showModal(outfit) {
      this.selectedOutfit = outfit;
      this.showGownDetailsModal = true;
    },
    closeModal() {
      this.showGownDetailsModal = false;
      this.selectedOutfit = {};
    },
    displayBookForm() {
      this.bookForm = true;
    },
    closeBookForm() {
      this.bookForm = false;
    },
    updateReturnDate() {
      if (this.pickup_date) {
        const pickup = new Date(this.pickup_date);
        pickup.setDate(pickup.getDate() + 4);  // Add 4 days to pickup date
        const returnDate = pickup.toISOString().split('T')[0];  // Format the date to yyyy-mm-dd
        this.return_date = returnDate;
      }
    },
    bookOutfit() {
      const bookingData = {
        outfit_id: this.selectedOutfit.outfit_id,
        pickup_date: this.pickup_date,
        return_date: this.return_date,
        status: 'booked', // You can modify the status as needed (e.g., "booked", "reserved", etc.)
        additional_charges: 0 // Set additional charges if necessary, or update based on user input
      };

      // Send the data to the backend using Axios
      axios
        .post('http://127.0.0.1:5000/book-outfit', bookingData, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        })
        .then((response) => {
          // Handle success (you can show a success message or redirect the user)
          console.log(response.data.message);
          alert('Outfit booked successfully!');
          this.closeBookForm(); // Close the modal after booking
        })
        .catch((error) => {
          // Handle error (you can show an error message to the user)
          console.error('Error booking outfit:', error);
          alert('There was an error booking the outfit. Please try again.');
        });
    },
  },
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

/* Add styles for filter dropdown */
.filter-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 50;
}
</style>
