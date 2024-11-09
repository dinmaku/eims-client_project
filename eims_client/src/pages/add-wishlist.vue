<template>
  <div class="h-full flex items-center justify-center overflow-y-auto">
    <form @submit.prevent="submitWishlist" class="bg-gray-200 w-full h-full flex flex-col items-center">
      <div class="mt-32 flex flex-col items-center text-center space-y-2">
        <h1 class="text-5xl font-merriweatherBoldItalic font-semibold text-gray-800">Add to Wishlist</h1>
        <p class="text-md font-medium font-quicksand tracking-wide text-gray-500">Reserve your place for celebration.</p>
      </div>
      <hr class="border-t border-gray-400 my-8 w-[60%] mx-auto" />
      <div class="bg-gray-100 min-h-[180vh] max-w-4xl w-full flex flex-col justify-start mb-10 rounded-lg shadow-xl px-4 sm:px-6 lg:px-8">
        <div class="m-5 items-center">
          <h1 class="font-bold font-amaticBold text-lg text-blue-800">ⓘ Event Details</h1>
          <div class="ml-3 mt-10 space-y-3">
            <label for="eventInput" class="text-md font-semibold text-gray-700">Give your event a name. *</label>
            <p class="text-md text-gray-500">Provide a unique and descriptive name for your event.</p>
            <input type="text" v-model="event_name" class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md" placeholder="Enter event name here" required/>
          </div>
          <div class="ml-3 mt-10 space-y-3">
            <label for="eventType" class="text-md font-semibold text-gray-700">Choose a type of event. *</label>
            <p class="text-md text-gray-500">Select the category that best describes your event.</p>
            <select v-model="event_type" class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md">
              <option disabled selected value="">Pick your event here</option>
              <option value="Wedding">Wedding</option>
              <option value="Birthday">Birthday</option>
              <option value="Debut">Debut</option>
            </select>     
          </div>
          <div class="ml-3 mt-10 space-y-3">
            <label for="eventTheme" class="text-md font-semibold text-gray-700">Theme of your event. *</label>
            <p class="text-md text-gray-500">Define a captivating theme that sets the mood for your event.</p>
            <input type="text" v-model="event_theme" class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md" placeholder="Enter theme here" required/>
          </div>
          <div class="ml-3 mt-10 space-y-3">
            <label for="eventColor" class="text-md font-semibold text-gray-700">Pick a color of your event. *</label>
            <span class="ml-1 text-md text-gray-600">(You can choose up to 3 colors)</span>
            <p class="text-md text-gray-500">Select a vibrant color palette that embodies the spirit of your event.</p>
            <input type="text" v-model="event_color" class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md" placeholder="Enter the color(s) here" required/>
          </div>
          <div class="ml-3 mt-10 space-y-3">
            <label for="eventLocation" class="text-md font-semibold text-gray-700">Where is your event taking place? *</label>
            <p class="text-md text-gray-500">Find the location where the event will take place.</p>
            <div class="w-full h-64">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d252720.1027251007!2d123.93311977386475!3d8.227715578917763!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x325575d3797ab2ff%3A0xc0643772cbb0a54e!2sRed%20Carpet!5e0!3m2!1sen!2sph!4v1722243442790!5m2!1sen!2sph"
                class="w-full h-full border-0"
                allowfullscreen
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
              </iframe>
            </div>
          </div>
          <div class="ml-3 mt-10 space-y-3">
            <label for="eventVenue" class="text-md font-semibold text-gray-700">Choose your Venue. *</label>
            <p class="text-md text-gray-500">Choose a venue that reflects the essence of your celebration.</p>
            <input type="text" v-model="venue" class="w-full sm:w-9/12 h-12 rounded-lg font-medium shadow-md" placeholder="Enter your venue here" required/>
          </div>
          <div class="flex justify-center items-center space-x-4">
            <button class="mt-12 py-2 px-4 bg-gray-200 hover:bg-red-400 font-semibold text-gray-900 rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-110">Cancel</button>
            <button type="submit" class="mt-12 py-2 px-4 bg-blue-300 hover:bg-blue-400 font-semibold text-gray-900 rounded-lg shadow-lg transition-transform duration-300 transform hover:scale-110">Confirm</button>
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
      event_color: '',
      venue: '',
      isUserLoggedIn: false, // Track login state
      showAlert: false, // Show success alert
    };
  },
  mounted() {
    // Check login status when component mounts
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
          const token = localStorage.getItem('access_token');
          console.log('Token being sent:', token);  // Ensure token is not undefined
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

    async submitWishlist() {
      const token = localStorage.getItem('access_token'); // Get token
      if (!token) {
        alert('You are not logged in. Please log in to add to the wishlist.');
        return; // User not logged in, return early
      }

      const wishlistData = {
        event_name: this.event_name,
        event_type: this.event_type,
        event_theme: this.event_theme,
        event_color: this.event_color,
        venue: this.venue,
      };

      try {
        const response = await axios.post('http://127.0.0.1:5000/wishlist', wishlistData, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Send the JWT token
          },
          withCredentials: true,  // Send cookies with the request if needed
        });

        if (response.status === 201) {
            this.displayWishlistAlert(); // Display success alert
            setTimeout(() => {
              this.$router.push('/'); // Navigate to '/'
            }, 3000); // Adjust the delay as needed (e.g., 3 seconds to match alert auto-close)
          } else {
            alert('Something went wrong. Please try again.');
          }
      } catch (error) {
        console.error('Error adding event to wishlist:', error.response?.data || error.message);
        if (error.response) {
          if (error.response.status === 401) {
            alert('You must be logged in to add to the wishlist.');
          } else {
            alert(`Error: ${error.response.data.message || 'An unknown error occurred.'}`);
          }
        } else {
          alert(`Error: ${error.message}`);
        }
      }
    },

    displayWishlistAlert() {
      this.showAlert = true;
      setTimeout(() => {
        this.showAlert = false;
      }, 3000); // Auto-hide after 3 seconds
    },
  },
};

</script>




<style scoped>
/* Add your styles here */
</style>