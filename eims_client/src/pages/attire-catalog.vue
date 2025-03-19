<template>
  <div class="pt-32 px-5 pb-5 bg-gray-500">
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

      <p class="text-gray-50 italic">{{ outfitsLength }} <span>results</span></p>
    </div>

    <!-- Outfit grid container -->
    <div class="outfit-container grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-4 w-full">
      <div v-for="outfit in outfits" :key="outfit.outfit_id" class="outfit-card bg-white border rounded-lg shadow-lg p-4 flex flex-col h-full cursor-pointer" @click="showModal(outfit)">
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
    };
  },
  mounted() {
    this.fetchOutfits();
  },
  methods: {
    async fetchOutfits() {
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
        
        this.outfits = response.data;
      } catch (error) {
        console.error('Error fetching outfits:', error);
        // Handle specific error cases
        if (error.response?.status === 401 || error.response?.status === 422) {
          // User is not logged in or token is invalid - still try to fetch public data
          try {
            const response = await axios.get('http://127.0.0.1:5000/outfits', {
              headers: {
                'Content-Type': 'application/json'
              }
            });
            this.outfits = response.data;
          } catch (retryError) {
            console.error('Error fetching public outfits:', retryError);
            this.outfits = []; // Set empty array if all attempts fail
          }
        }
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
  computed: {
    outfitsLength() {
      return this.outfits.length;
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
</style>
