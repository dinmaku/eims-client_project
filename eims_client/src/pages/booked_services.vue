<template>
    <div class="h-screen flex flex-col items-center bg-gray-200 overflow-x-hidden overflow-y-auto px-4 md:px-8">
        <div class="w-full mt-32">
            <div class="mt-12 md:mt-1 ml-2 md:ml-16">
                <h1 class="text-2xl md:text-4xl font-raleway font-medium text-gray-800 tracking-wide">Booking Status</h1>
                <p class="text-sm md:text-md text-gray-500">Track your outfit and event booking reservations.</p>
            </div>

            <div class="flex flex-col md:flex-row m-4 md:m-20 mt-4 md:mt-10">
                <div class="flex flex-col items-start space-y-4 mt-5 md:mt-10">
                    <button
                        @click="displayEventSection"
                        :class="{
                            'bg-gray-100 text-black shadow-lg': events_navigation,
                            'text-black': !events_navigation
                        }"
                        class="flex items-center px-3 py-2 md:px-4 md:py-1 rounded-md text-base md:text-lg font-medium hover:bg-blue-500 hover:text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
                    >
                    <img src="/img/booking.png" alt="Event Icon" class="h-5 w-5 md:h-7 md:w-7 mr-2" />
                       
                        Booked Event
                    </button>

                    <button
                         @click="displayOutfitsSection"
                        :class="{
                            'bg-gray-100 text-black shadow-lg': displayOutfits,
                            'text-black': !displayOutfits
                        }"
                        class="flex items-center px-3 py-2 md:px-4 md:py-2 rounded-md text-base md:text-lg font-medium hover:bg-blue-500 hover:text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
                    >
                    <img src="/img/booked-gown.png" alt="Event Icon" class="h-6 w-6 md:h-9 md:w-9 mr-2" />
                        
                        Gown Rental
                    </button>
                </div>

                <div class="flex flex-col items-center w-full mt-4 md:mt-0 md:ml-16 relative">
                    <div class="absolute top-2 sm:top-1 right-2 sm:right-24 z-10 w-full md:w-auto">  
                    <div v-if="events_navigation" class="flex flex-wrap items-center justify-center space-x-2 md:space-x-10 bg-gray-50 px-3 md:px-5 py-2 rounded-lg shadow-lg">
                        <button
                            @click="displayWishlist = !displayWishlist"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': displayWishlist,
                                'text-gray-600': !displayWishlist
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            Wishlist
                        </button>
                        <button
                            @click="displayEvents = !displayEvents"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': displayEvents,
                                'text-gray-600': !displayEvents
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                        
                            Events
                        </button>

                        <!-- Completed Button -->
                        <button
                           @click="displayCompleted = !displayCompleted"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': displayCompleted,
                                'text-gray-600': !displayCompleted
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            Completed
                        </button>

                        <!-- Rated Button -->
                        <button
                            @click="displayRated = !displayRated"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': displayRated,
                                'text-gray-600': !displayRated
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            Rated
                        </button>

                        <!-- Canceled Button -->
                        <button
                            @click="displayAll = !displayAll"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': displayAll,
                                'text-gray-600': !displayAll
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            Canceled
                        </button>
                        <button
                            @click="setActiveNav('all')"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'all',
                                'text-gray-600': activeNavButton !== 'all'
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            All
                        </button>
                    </div>

                    <div v-if="displayBookedWishlist" class="flex justify-center mt-5 md:mt-10">
                        <div class="bg-gray-100 p-3 md:p-5 rounded-lg shadow-md overflow-x-auto w-full">
                            <table class="min-w-full md:min-w-[700px] border-collapse">
                                <thead>
                                    <tr>
                                        <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Name</th>
                                        <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Type</th>
                                        <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Theme</th>
                                        <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Venue</th>
                                        <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Total Price</th>
                                        <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item, index) in bookedWishlist" :key="index">
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_name }}</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_type }}</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_theme }}</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.venue_name }}</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ formatPrice(item.total_price) }}</td>
                                        <td class="px-2  md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">
                                            <button @click="displayWishlistDetails(item)" class="text-blue-500 hover:text-blue-700">View</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            </div>
                        </div>

                        <div v-if="displayBookedOutfits" class="flex justify-center mt-5 md:mt-10">
                            <div class="bg-gray-100 p-3 md:p-5 rounded-lg shadow-md overflow-x-auto w-full">
                                <table class="min-w-full md:min-w-[700px] border-collapse">
                                    <thead>
                                        <tr>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Outfit ID</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Pickup Date</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Return Date</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Status</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Additional Charges</th>
                                            <th class="px-2 md:px-6 py-2 md:py-3 text-left text-xs md:text-sm font-medium text-gray-800 uppercase tracking-w-normal border-b border-blue-500">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(outfit, index) in bookedOutfits" :key="index">
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ outfit.outfit_id }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ outfit.pickup_date }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ outfit.return_date }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ outfit.status }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ outfit.additional_charges }}</td>
                                            <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">
                                                <button @click="displayBookedOutfitDetails(outfit)" class="text-blue-500 hover:text-blue-700">View</button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>


                        




                    </div>
                </div>
            </div>
        </div>


   <!-- Modal for selected wishlist details -->
<div v-if="selectedWishlist" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white p-4 md:p-6 rounded-xl shadow-lg w-full max-w-[95%] md:max-w-[700px] overflow-y-auto max-h-[90vh]">
        <button @click="closeWishlistModal" class="text-gray-500 text-2xl md:text-3xl float-right">&times;</button>
        <div class="mt-3 md:mt-5">
            <h1 class="text-lg md:text-xl font-bold mb-3 md:mb-4 font-raleway">Wishlist Details</h1>
            <div class="flex flex-col space-y-4">
                <p class="text-gray-600">Event Name: <span class="text-black">{{ selectedWishlist.event_name }}</span></p>
                <div class="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2">
                    <div class="bg-gray-300 w-full md:w-1/2 px-2 py-3 space-y-2 rounded-xl">
                        <p class="text-gray-700">Event Type</p>
                        <p>{{ selectedWishlist.event_type }}</p>
                    </div>
                    <div class="bg-gray-300 w-full md:w-1/2 px-2 py-3 space-y-2 rounded-xl">
                        <p class="text-gray-700">Event Theme</p>
                        <p>{{ selectedWishlist.event_theme }}</p>
                    </div>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Event Color</p>
                    <p>{{ selectedWishlist.event_color }}</p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Venue</p>
                    <p>{{ selectedWishlist.venue_name }}</p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                        <p class="text-gray-700">Package Name</p>
                        <p>{{ selectedWishlist.package_name }}</p>
                    </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Total Price</p>
                    <p>{{ formatPrice(selectedWishlist.total_price) }}</p>
                </div>
           
                <!-- Section for Suppliers with Expand Button -->
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Suppliers</p>
                    <button @click="showSuppliers = !showSuppliers" class="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        {{ showSuppliers ? 'Hide Suppliers' : 'Show Suppliers' }}
                    </button>
                    <div v-if="showSuppliers" class="mt-2 overflow-y-auto max-h-64 space-y-2">
                        <!-- Internal Suppliers -->
                        <div v-for="(name, index) in selectedWishlist.internal_supplier_names" :key="'internal-'+index" class="p-4 border rounded-lg bg-gray-100 shadow-sm">
                            <p class="font-semibold text-gray-800">Internal Supplier: {{ name }}</p>
                            <p class="text-gray-600">Service: {{ selectedWishlist.internal_services[index] }}</p>
                            <p class="text-gray-600">Price: {{ formatPrice(selectedWishlist.internal_service_prices[index]) }}</p>
                            <p class="text-gray-600">Remarks: {{ selectedWishlist.remarks[index] }}</p>
                        </div>

                        <!-- External Suppliers -->
                        <div v-for="(name, index) in selectedWishlist.external_supplier_names" :key="'external-'+index" class="p-4 border rounded-lg bg-gray-100 shadow-sm">
                            <p class="font-semibold text-gray-800">External Supplier: {{ name }}</p>
                            <p class="text-gray-600">Contact: {{ selectedWishlist.external_supplier_contacts[index] }}</p>
                            <p class="text-gray-600">Price: {{ formatPrice(selectedWishlist.external_supplier_prices[index]) }}</p>
                            <p class="text-gray-600">Remarks: {{ selectedWishlist.remarks[index + selectedWishlist.internal_supplier_names.length] }}</p>
                        </div>
                    </div>
                </div>

                <!-- Section for Gown Package -->
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Gown Package</p>
                    <p v-if="selectedWishlist.gown_package_name">
                        Package Name: {{ selectedWishlist.gown_package_name }} <br>
                        Package Price: {{ formatPrice(selectedWishlist.gown_package_price) }} <br>
                    </p>
                    <p v-if="selectedWishlist.outfit_name">
                        Outfit Name: {{ selectedWishlist.outfit_name }} <br>
                        Rent Price: {{ formatPrice(selectedWishlist.rent_price) }} <br>
                        Outfit Description: {{ selectedWishlist.outfit_desc }}
                    </p>
                    <p v-else>No Gown Package Details Available</p>
                </div>
            </div>
            <div class="mt-4 md:mt-7 flex justify-end items-center">
                <button class="flex items-center space-x-1 px-2 py-1 rounded-lg text-red-500 hover:shadow-lg hover:text-red-700 hover:border-b-2 border-red-600"
                        @click="deleteWishlistItem(selectedWishlist.events_id)">
                    <img src="/img/delete.png" alt="Delete Icon" class="w-4 md:w-5 h-4 md:h-5">
                    <span>Delete</span>
                </button>
            </div>
        </div>
    </div>
</div>





       
   

    </div>
</template>


<script>
import axios from 'axios';

    export default{
        data() {
        return {
        events_navigation: true,
        selectedWishlist: null,

        bookedWishlistDetails: false,
        displayBookedOutfits: false,
        
        // booked outfits
        displayBookedOutfits: false,

        //events navigation 
        displayBookedWishlist: true,
        displayCompleted: false,
        displayRated: false,
        displayCanceled: false,
        displayAll: false,

        bookedWishlist: [],
        bookedOutfits: [],

        showSuppliers: false,
        };
    },
    created() {
    this.fetchBookedWishlist();
    this.fetchBookedOutfits();
  },
    methods: {
         displayEventSection() {
            this.displayBookedWishlist = true;
            this.events_navigation = true;
            this.displayBookedOutfits = false;
            },
         displayOutfitsSection() {
            this.displayBookedWishlist = false;
            this.events_navigation = false;
            this.displayBookedOutfits = true;
            },

            displayWishlist()
            {
                this.displayBookedWishlist = true;
            },
    
            formatPrice(price) {
                if (price === null || price === undefined || isNaN(price)) {
                    return 'N/A'; // Return a fallback if price is invalid
                }
                // Round the price to 2 decimal places and format with commas
                return parseFloat(price).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                },
            
        
                

                async fetchBookedWishlist() {
                    try {
                    const token = localStorage.getItem('access_token');  // Assuming the JWT token is stored in localStorage
                    const response = await axios.get('http://127.0.0.1:5000/wishlist', {
                        headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`  // Send the JWT token
                        },
                        withCredentials: true  // Send cookies with the request if needed
                    });
                    this.bookedWishlist = response.data;  // Populate bookedWishlist array with data from API
                    console.log("Fetched booked wishlist:", this.bookedWishlist);  // Log the data to verify structure
                    } catch (error) {
                    console.error('Error fetching booked wishlist:', error);
                    }
                },

            async deleteWishlistItem(events_id) {
                try {
                    const token = localStorage.getItem('access_token');  // Get JWT token from localStorage

                    // Send a DELETE request to the backend with the events_id
                    const response = await axios.delete(`http://127.0.0.1:5000/booked_wishlist/${events_id}`, {
                        headers: {
                            'Authorization': `Bearer ${token}`,  // Send the JWT token
                        }
                    });

                    if (response.status === 200) {
                        // Remove the deleted item from the local wishlist array (events list)
                        this.bookedWishlist = this.bookedWishlist.filter(item => item.events_id !== events_id);
                        alert('Event item deleted successfully!');
                        this.selectedWishlist = false;  // Optional: Clear the selected item if needed
                    } else {
                        alert('Failed to delete event item');
                    }
                } catch (error) {
                    console.error('Error deleting event item:', error);
                    alert('Error deleting event item');
                }
            },


            displayWishlistDetails(item) {
            this.selectedWishlist = item;
            },
            closeWishlistModal() {
                this.selectedWishlist = null;
                this.showSuppliers = false;
            },


            async fetchBookedOutfits() {
                try {
                    const token = localStorage.getItem('access_token');  // Get JWT token from localStorage
                    const response = await axios.get('http://127.0.0.1:5000/booked-outfits', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`  // Send the JWT token in the header
                    },
                    withCredentials: true  // Send cookies with the request if needed
                    });
                    this.bookedOutfits = response.data;  // Populate bookedOutfits array with data from API
                } catch (error) {
                    console.error('Error fetching booked outfits:', error);
                    alert('Error fetching booked outfits');
                }
        },
    },

    mounted() {
        this.fetchBookedWishlist();
        this.fetchBookedOutfits();  // Automatically call the function when the component is mounted
    },
}
</script>

<style scoped>
</style>