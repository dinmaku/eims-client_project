<template>
  <div class="h-full flex items-center justify-center overflow-y-auto">
    <form @submit.prevent="submitWishlist" class="bg-gray-200 w-full h-full flex flex-col items-center">
      <div class="mt-32 flex flex-col items-center text-center space-y-2">
        <h1 class="text-5xl font-merriweatherBoldItalic font-semibold text-gray-800">Add to Wishlist</h1>
        <p class="text-md font-medium font-quicksand tracking-wide text-gray-500">Reserve your place for celebration.</p>
      </div>
      <hr class="border-t border-gray-400 my-8 w-[60%] mx-auto" />
      <div class="bg-gray-100 min-h-[110vh] max-w-4xl w-full flex flex-col justify-start mb-10 rounded-lg shadow-xl px-4 sm:px-6 lg:px-8 overflow-y-auto">
        <div v-if="wishlistDetailsForm" class="m-5 items-center">
          <h1 class="mt-5 font-bold font-amaticBold text-lg text-blue-800">ⓘ Event Details</h1>
          <div class="ml-3 mt-10 space-y-3">
            <label for="eventInput" class="text-md font-semibold text-gray-700">Give your event a name. *</label>
            <p class="text-md text-gray-500">Provide a unique and descriptive name for your event.</p>
            <input type="text" v-model="event_name" class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md" placeholder="Enter event name here" required/>
          </div>
          
              <div class="ml-3 mt-10 space-y-3">
                <label for="eventType" class="text-md font-semibold text-gray-700">Choose a type of event. *</label>
                <p class="text-md text-gray-500">Select the category that best describes your event.</p>

                <div v-if="loading" class="text-center">Loading event packages...</div>
                <div v-else>

                <select v-model="event_type" class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md">
                  <option disabled selected value="">Pick your event here</option>
                  
                  <!-- Dynamically populate event types from unique package types -->
                  <option v-for="type in uniquePackageTypes" :key="type" :value="type">{{ type }}</option>
                </select>
              </div>
            </div>
          <div class="ml-3 mt-10 space-y-3">
            <label for="eventTheme" class="text-md font-semibold text-gray-700">Theme of your event. *</label>
            <p class="text-md text-gray-500">Define a captivating theme that sets the mood for your event.</p>
            <input type="text" v-model="event_theme" class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md" placeholder="Enter theme here" required/>
          </div>
          <div class="flex flex-col ml-3 mt-10 space-y-3">
            <label for="eventColor" class="text-md font-semibold text-gray-700">Pick a color of your event. *</label>
            <p class="text-md text-gray-500">Select a vibrant color palette that embodies the spirit of your event.</p>

            <!-- Container for the text input and color picker -->
            <div class="flex relative items-center">
              <!-- Native HTML color picker input -->
              <input 
                type="color" 
                v-model="event_color" 
                class="absolute inset-0 opacity-0 cursor-pointer z-30"
                required
              /> 

              <!-- Custom circular button for color display inside the text input -->
              <div 
                :style="{ backgroundColor: event_color }" 
                class="absolute left-3 top-2.5 w-6 h-6 rounded-full border-none shadow-md cursor-pointer z-20"
              ></div>

              <!-- Regular text input field where user can also enter a color manually -->
              <input 
                type="text" 
                v-model="event_color" 
                class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md pl-12"
                placeholder="Enter the color(s) here" 
                required
              />
            </div>
          </div>

          <div class="flex justify-center items-center space-x-4">
            <button @click = "cancelSubmitWishlist" class="mt-16 py-2 px-4 bg-gray-200 hover:bg-red-400 font-semibold text-gray-900 rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-110">Cancel</button>
            <button @click="displayPackages" class="mt-16 py-2 px-4 bg-blue-300 hover:bg-blue-400 font-semibold text-gray-900 rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-110">Next</button>
          </div>
        </div>

        <div v-if="packagesForm" class="m-5 items-center">
           <div class = "flex justify-between items-center">
          <h1 class="mt-5 font-bold font-amaticBold text-lg text-blue-800">ⓘ Package Deals</h1>
           <button @click="prevEventDetails" class="mt-5 py-1 px-5 bg-gray-200 hover:bg-red-400 font-semibold text-gray-900 rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-110">
            Back</button>
        </div>
          <p class="text-md text-gray-500 mt-2">Choose from our variety of event packages and reserve your spot for an unforgettable celebration!</p>

 
      <!-- Packages Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-7">
      <div
        v-for="(pkg, index) in filteredPackages"
        :key="pkg.packageId"
        class="flex flex-col rounded-3xl h-[320px] w-[260px] cursor-pointer transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-lg hover:bg-opacity-90"
        :style="{ backgroundColor: getRandomColor() }"
        @click="selectPackage(pkg)"
      >
        <div class="px-6 py-8 sm:p-10 sm:pb-6">
          <div class="grid items-center justify-center w-full grid-cols-1 text-left">
            <div>
              <h2 class="text-lg font-medium tracking-tighter text-gray-600 lg:text-3xl">
                {{ pkg.package_name }}
              </h2>
              <p class="mt-2 text-sm text-gray-500 font-raleway">
                {{ pkg.description }}
              
                
              </p>
            </div>

            <div class="mt-6">
              <p>
                <span class="text-4xl font-light tracking-tight text-black">
                  {{ formatPrice(pkg.total_price) }}
                </span>
                <span class="text-sm font-medium text-gray-500 ml-2">php only</span>
              </p>
            </div>

            <div class="mt-4">
              <p class="text-xs font-semibold text-gray-500">Venue: {{ pkg.venue_name }}</p>
              <p class="text-xs font-semibold text-gray-500">Capacity: {{ pkg.capacity }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

    <!-- Package Details Form -->
    <div v-if="packagesDetailsForm" class="m-5 items-center">
      <div class="flex justify-between items-center">
        <h1 class="mt-5 font-bold font-amaticBold text-lg text-blue-800">ⓘ Package Details</h1>
        <button @click="prevPackageDeals" class="mt-5 py-1 px-5 bg-gray-200 hover:bg-red-400 font-semibold text-gray-900 rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-110">
          Back
        </button>
      </div>

      <div v-if="selectedPackage" class="mt-5">
        <h2 class="text-xl font-bold mb-3">{{ selectedPackage.package_name }}</h2>
        <h2 class="text-xl font-bold mb-3">{{ formatPrice(selectedPackage.total_price) }}</h2>
        
         <!-- Suppliers Section -->
        <div class="mb-5">
          <h3 class="text-lg font-semibold mb-2">Suppliers</h3>
          <div v-for="(supplier, index) in selectedPackage.suppliers" :key="index" class="mb-3">
            <div v-if="supplier.type === 'internal'">
              <p class="w-full p-2 border rounded bg-gray-100">
                Service: {{ supplier.service }} <br>
                Price: {{ formatPrice(supplier.price) }} <br>
                Remarks: {{ supplier.remarks }}
              </p>
            </div>
            <div v-else>
              <p class="w-full p-2 border rounded bg-gray-100">
                External Supplier Name: {{ supplier.external_supplier_name }} <br>
                Contact: {{ supplier.external_supplier_contact }} <br>
                Price: {{ formatPrice(supplier.external_supplier_price) }} <br>
                Remarks: {{ supplier.remarks }}
              </p>
            </div>
          </div>
        </div>





        <!-- Venue Section -->
          <div class="mb-5">
            <h3 class="text-lg font-semibold mb-2">Venue</h3>
            <p class="w-full p-2 border rounded bg-gray-100">
              Name: {{ selectedPackage.venue_name }} <br>
              Location: {{ selectedPackage.venue_location }} <br>
              Price: {{ formatPrice(selectedPackage.venue_price) }}
            </p>
          </div>



        <!-- Gown Package Section -->
          <div class="mb-5">
            <h3 class="text-lg font-semibold mb-2">Gown Package</h3>
            <p class="w-full p-2 border rounded bg-gray-100">
              Gown Package: {{ selectedPackage.gown_package_name }} <br>
              Price: {{ formatPrice(selectedPackage.gown_package_price) }}
            </p>
          </div>



        <!-- Event Schedule Section -->
        <div class="mb-5 space-x-4">
          <h3 class="text-lg font-semibold mb-2">Event Schedule</h3>
          <input v-model="eventSchedule.date" type="date" class="w-1/4 p-2 border rounded mb-2">
          <input v-model="eventSchedule.start_time" type="time" class="w-1/4 p-2 border rounded mb-2 ">
          <input v-model="eventSchedule.end_time" type="time" class="w-1/4 p-2 border rounded">
        </div>

        <button @click="submitWishlist" class="mt-5 py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-105">
          Add to Wishlist
        </button>
      </div>
    </div>


       
      </div>
    </form>

    <div v-if="showAlert" class="fixed inset-x-0 top-1/3 mx-auto max-w-md bg-green-100 border border-green-400 text-green-700 px-4 py-5 rounded shadow-lg transform transition-all duration-500 ease-in-out" role="alert">
    <div class="flex items-center">
      <div class = "text-3xl font-bold ml-1 rounded-full bg-gray-200 px-2">
        &check;
      </div>
      <div>
        <div class = "flex flex-col ml-5">
        <strong class="font-bold">Success!</strong>
        <span class="block sm:inline">Event successfully added to your wishlist!</span>
      </div>
      </div>
    </div>
  </div>



  </div>
</template>

<script>
import axios from 'axios';

// Ensure Axios is configured to send credentials with requests globally
axios.defaults.withCredentials = true;

export default {
  name: 'AddWishlist',
  data() {
    return {
      event_name: '',
      event_type: '',
      event_theme: '',
      event_color: "#000000",
      venue: '',
      isUserLoggedIn: false,
      showAlert: false,
      wishlistDetailsForm: true,
      packagesForm: false,
      packagesDetailsForm: false,
      packages: [],
      selectedPackage: { 
        gown_package_id: null,
        suppliers: [], 
        venue_id: null 
      },
      loading: true,
      availableSuppliers: [], 
      availableVenues: [], 
      availableGownPackages: [],
      eventSchedule: {
        date: '',
        start_time: '',
        end_time: ''
      },
      isSubmitting: false,
    };
  },
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem('access_token');
      console.log('Token being sent:', token); // Ensure token is not undefined
      if (!token) {
        console.log('No token found');
        return;
      }

      axios.get('http://127.0.0.1:5000/check-auth', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      .then(response => {
        console.log('Auth check successful:', response.data);
      })
      .catch(error => {
        console.error('Error checking auth status:', error.response.data);
      });
    },
    displayWishlistAlert() {
      this.showAlert = true;
      setTimeout(() => {
        this.showAlert = false;
      }, 3000); // Auto-hide after 3 seconds
    },
    async fetchPackages() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          alert('You are not logged in. Please log in to view event packages.');
          return;
        }

        const response = await axios.get('http://127.0.0.1:5000/created-packages', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          withCredentials: true,
        });

        // Process packages response
        this.packages = response.data.map((pkg) => ({
          packageId: pkg.package_id,
          package_name: pkg.package_name,
          package_type: pkg.package_type,
          venue_id: pkg.venue_id, // Ensure venue_id is captured
          venue_name: pkg.venue_name,
          venue_location: pkg.venue_location,
          venue_price: pkg.venue_price,
          total_price: pkg.total_price,
          capacity: pkg.capacity,
          description: pkg.description,
          gown_package_id: pkg.gown_package_id, // Ensure gown_package_id is captured
          gown_package_name: pkg.gown_package_name,
          gown_package_price: pkg.gown_package_price,
          suppliers: pkg.suppliers ? pkg.suppliers.map((supplier) => ({
            ...supplier,
            type: supplier.external_supplier_name ? 'external' : 'internal',
          })) : [],
          selected: false,
          detailsVisible: false,
        }));

        this.filterPackages();
        this.loading = false;
      } catch (error) {
        console.error('Error fetching packages:', error);
      }
    },
    async selectPackage(pkg) {
        this.packagesForm = false;
        this.packagesDetailsForm = true; // Hide the packages form
        this.selectedPackage = true;

        this.selectedPackage = { ...pkg };

        console.log('Selected package after copying base details:', this.selectedPackage);

        // Ensure suppliers are initialized if not present
        if (!this.selectedPackage.suppliers) {
          this.selectedPackage.suppliers = [];
        }

        // Fetch additional details if necessary
        if (!pkg.detailsFetched) {
          const details = await this.fetchPackageDetails(pkg.packageId);

          // Construct suppliers from fetched details
          const suppliers = details.supplier_ids.map((id, index) => {
            return {
              id: id,
              type: details.external_supplier_names[index] ? 'external' : 'internal',
              service: details.services[index],
              price: details.service_prices[index],
              external_supplier_name: details.external_supplier_names[index],
              external_supplier_contact: details.external_supplier_contacts[index],
              external_supplier_price: details.external_supplier_prices[index],
              remarks: details.remarks[index],
            };
          });

          this.selectedPackage.suppliers = suppliers;
          this.selectedPackage.detailsFetched = true;

          console.log('Fetched package details:', details);
          console.log('Constructed suppliers:', suppliers);
          console.log('Selected package after fetching details:', this.selectedPackage);
        }

        console.log('Final selected package:', this.selectedPackage);
      },

    
    filterPackages() {
      if (this.event_type && this.event_type !== '') {
        this.filteredPackages = this.packages.filter((pkg) => pkg.package_type === this.event_type);
      } else {
        this.filteredPackages = this.packages;
      }
    },
    async fetchPackageDetails(packageId) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/packages/${packageId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        // Log the fetched package details to check if suppliers and venue data are included
        console.log('Fetched package details:', response.data);

        return response.data; // Make sure the response contains suppliers and venue details
      } catch (error) {
        console.error('Error fetching package details:', error);
        return {};
      }
    },
    prevPackageDeals() {
      this.packagesDetailsForm = false;
      this.packagesForm = true;
    },
    addSupplier() {
      if (!this.selectedPackage.suppliers) {
        this.selectedPackage.suppliers = [];
      }
      this.selectedPackage.suppliers.push({
        type: 'external',
        external_supplier_name: '',
        external_supplier_contact: '',
        external_supplier_price: 0,
        remarks: '',
      });
    },
    async fetchAvailableSuppliers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/available-suppliers', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        this.availableSuppliers = response.data; // Check if this is populated correctly
        console.log('Available Suppliers:', this.availableSuppliers);
      } catch (error) {
        console.error('Error fetching available suppliers:', error);
      }
    },

    async fetchAvailableVenues() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/available-venues', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        this.availableVenues = response.data; // Check if this is populated correctly
        console.log('Available Venues:', this.availableVenues);
      } catch (error) {
        console.error('Error fetching available venues:', error);
      }
    },
    async fetchAvailableGownPackages() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/available-gown-packages', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        this.availableGownPackages = response.data;
      } catch (error) {
        console.error('Error fetching available gown packages:', error);
      }
    },
    async submitWishlist() {
    if (this.isSubmitting) {
      return;  // Prevent further submissions if already submitting
    }
    this.isSubmitting = true;  // Set the flag to indicate submission in progress
    
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert('You are not logged in. Please log in to add to the wishlist.');
      this.isSubmitting = false;  // Reset the flag if not logged in
      return;
    }

    try {
      const wishlistData = {
        event_name: this.event_name,
        event_type: this.event_type,
        event_theme: this.event_theme,
        event_color: this.event_color,
        package_id: this.selectedPackage.packageId,
        suppliers: this.selectedPackage.suppliers,
        schedule: this.eventSchedule.date,
        start_time: this.eventSchedule.start_time,
        end_time: this.eventSchedule.end_time,
        status: 'Wishlist',
      };

      const response = await axios.post('http://127.0.0.1:5000/wishlist', wishlistData, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 201) {
        this.showAlert = true;
        setTimeout(() => {
          this.showAlert = false;
          this.$router.push('/booked-services');
        }, 2000);
      }
    } catch (error) {
      console.error('Error adding event to wishlist:', error);
      alert('An error occurred while adding the event to wishlist. Please try again.');
    } finally {
      this.isSubmitting = false;  // Reset the flag after operation is complete
    }
  },



    cancelSubmitWishlist() {
      window.scrollTo(0, 0);
      this.$router.push('/');
    },
    displayPackages() {
      this.wishlistDetailsForm = false;
      this.packagesForm = true;
    },
    prevEventDetails() {
      this.packagesForm = false;
      this.wishlistDetailsForm = true;
    },
    getRandomColor() {
      const colors = [
        '#f7c5f7', // Light pink
        '#afe2f8', // Light blue
        '#f6f9a0', // Light yellow
        '#f7c5c5', // Light red
        '#e3f5d4', // Pale green
        '#fce6e2', // Pale peach
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    },
    formatPrice(price) {
      if (price === null || price === undefined || isNaN(price)) {
        return 'N/A'; // Return a fallback if price is invalid
      }
      // Round the price to 2 decimal places and format with commas
      return parseFloat(price).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    },
  },
  computed: {
    uniquePackageTypes() {
      const types = this.packages.map((pkg) => pkg.package_type);
      return [...new Set(types)]; // Use Set to remove duplicates
    },
    filteredPackages() {
      if (this.event_type && this.event_type !== '') {
        return this.packages.filter((pkg) => pkg.package_type === this.event_type);
      } else {
        return this.packages;
      }
    },
  },
  mounted() {
    this.checkLoginStatus();
    this.fetchPackages();
    this.fetchAvailableSuppliers();
    this.fetchAvailableVenues();
    this.fetchAvailableGownPackages();
  },
  watch: {
    event_type(newValue) {
      this.filterPackages(); // Call filterPackages when event_type changes
    },
  },
};
</script>






<style scoped>
/* Add your styles here */
</style>