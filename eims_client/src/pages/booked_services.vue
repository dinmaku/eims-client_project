<template>
    <div class="h-screen flex flex-col items-center bg-gray-200 overflow-x-hidden overflow-y-auto px-4 md:px-8">
        <div class="w-full mt-32">
            <div class="mt-12 md:mt-1 ml-2 md:ml-16">
                <h1 class="text-2xl md:text-4xl font-raleway font-medium text-gray-800 tracking-wide">Booking Status</h1>
                <p class="text-sm md:text-md text-gray-500">Track your outfit and event booking reservations.</p>
            </div>

            <div class="flex flex-col md:flex-row m-4 md:m-20 mt-4 md:mt-10">
              
                <div class="flex flex-col items-center w-full mt-4 md:mt-0 md:ml-16 relative">
                    <div class="absolute top-2 sm:top-1 right-2 sm:right-24 z-10 w-full md:w-auto">  
                    <div v-if="events_navigation" class="flex flex-wrap items-center justify-center space-x-2 md:space-x-10 bg-gray-50 px-3 md:px-5 py-2 rounded-lg shadow-lg">
                        <button
                            @click="setActiveNav('wishlist')"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'wishlist',
                                'text-gray-600': activeNavButton !== 'wishlist'
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            Wishlist
                        </button>
                        <button
                            @click="setActiveNav('events')"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'events',
                                'text-gray-600': activeNavButton !== 'events'
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            Events
                        </button>
                        <button
                            @click="setActiveNav('completed')"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'completed',
                                'text-gray-600': activeNavButton !== 'completed'
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            Completed
                        </button>
                        <button
                            @click="setActiveNav('rated')"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'rated',
                                'text-gray-600': activeNavButton !== 'rated'
                            }"
                            class="text-sm md:text-md hover:text-blue-500 px-2 py-1 md:px-4 md:py-3"
                        >
                            Rated
                        </button>
                        <button
                            @click="setActiveNav('canceled')"
                            :class="{
                                'text-blue-600 border-b-2 border-blue-600': activeNavButton === 'canceled',
                                'text-gray-600': activeNavButton !== 'canceled'
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
                                    <tr v-for="(item, index) in filteredWishlist" :key="index">
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_name }}</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_type }}</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.event_theme }}</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ item.venue_name }}</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">{{ formatPrice(item.total_price) }} php</td>
                                        <td class="px-2 md:px-6 py-2 md:py-4 text-left text-xs md:text-sm text-gray-800">
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
<div v-if="selectedWishlist" @click.self="closeWishlistModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
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
                    <p class="text-gray-700">Schedule Details</p>
                    <p>Date: {{ selectedWishlist.schedule || 'Not set' }}</p>
                    <p>Start Time: {{ selectedWishlist.start_time || 'Not set' }}</p>
                    <p>End Time: {{ selectedWishlist.end_time || 'Not set' }}</p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Venue</p>
                    <p>{{ selectedWishlist.venue_name }}</p>
                    <p class="text-sm text-gray-600">Location: {{ selectedWishlist.location }}</p>
                    <p class="text-sm text-gray-600">Price: {{ formatPrice(selectedWishlist.venue_price) }} php</p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Package Details</p>
                    <p>Name: {{ selectedWishlist.package_name }}</p>
                    <p>Capacity: {{ selectedWishlist.capacity }} persons</p>
                    <p v-if="selectedWishlist.additional_capacity_charges">Additional Charges: {{ formatPrice(selectedWishlist.additional_capacity_charges) }} php per {{ selectedWishlist.charge_unit }} person(s)</p>
                    <p class="mt-2">Status: <span :class="{'text-green-600': selectedWishlist.package_status === 'Active', 'text-yellow-600': selectedWishlist.package_status === 'Pending', 'text-red-600': selectedWishlist.package_status === 'Cancelled'}">{{ selectedWishlist.package_status }}</span></p>
                </div>
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Total Price</p>
                    <p>{{ formatPrice(selectedWishlist.total_price) }} php</p>
                </div>
           
                <!-- Section for Suppliers -->
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl">
                    <p class="text-gray-700">Suppliers</p>
                    <button @click="showSuppliers = !showSuppliers" class="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        {{ showSuppliers ? 'Hide Suppliers' : 'Show Suppliers' }}
                    </button>
                    <div v-if="showSuppliers" class="mt-2 overflow-y-auto max-h-64 space-y-2">
                        <div v-if="selectedWishlist.suppliers && selectedWishlist.suppliers.length > 0">
                            <div v-for="supplier in selectedWishlist.suppliers" :key="supplier.supplier_id" class="p-4 border rounded-lg bg-gray-100 shadow-sm">
                                <p class="font-semibold text-gray-800">{{ supplier.name }}</p>
                                <p class="text-gray-600">Service: {{ supplier.service }}</p>
                                <p class="text-gray-600">Price: {{ formatPrice(supplier.price) }} php</p>
                                <p class="text-gray-600">Status: <span :class="{'text-green-600': supplier.status === 'Active', 'text-yellow-600': supplier.status === 'Pending', 'text-red-600': supplier.status === 'Cancelled'}">{{ supplier.status }}</span></p>
                                <p v-if="supplier.remarks" class="text-gray-600">Remarks: {{ supplier.remarks }}</p>
                            </div>
                        </div>
                        <p v-else class="text-gray-600">No suppliers selected</p>
                    </div>
                </div>

                <!-- Section for Outfit Package -->
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl mt-4">
                    <p class="text-gray-700 font-semibold">Outfit Package</p>
                    <div v-if="selectedWishlist.gown_package_name" class="space-y-2">
                        <div>
                            <p class="text-sm">Package Name: {{ selectedWishlist.gown_package_name }}</p>
                            <p class="text-sm">Package Price: {{ formatPrice(selectedWishlist.gown_package_price) }} php</p>
                        </div>
                        
                        <!-- Outfits Table -->
                        <div class="mt-4" v-if="selectedWishlist.outfits && selectedWishlist.outfits.length > 0">
                            <p class="text-sm font-medium mb-2">Included Outfits:</p>
                            <div class="overflow-x-auto">
                                <table class="min-w-full bg-white rounded-lg overflow-hidden">
                                    <thead class="bg-gray-100">
                                        <tr>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Name</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Type</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Color</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Price</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Status</th>
                                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-600">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-gray-200">
                                        <tr v-for="outfit in selectedWishlist.outfits" :key="outfit.outfit_id" class="hover:bg-gray-50">
                                            <td class="px-4 py-2 text-sm">{{ outfit.outfit_name }}</td>
                                            <td class="px-4 py-2 text-sm">{{ outfit.outfit_type }}</td>
                                            <td class="px-4 py-2 text-sm">{{ outfit.outfit_color }}</td>
                                            <td class="px-4 py-2 text-sm">{{ formatPrice(outfit.rent_price) }} php</td>
                                            <td class="px-4 py-2 text-sm">
                                                <span :class="{'text-green-600': outfit.status === 'Active', 'text-yellow-600': outfit.status === 'Pending', 'text-red-600': outfit.status === 'Cancelled'}">
                                                    {{ outfit.status }}
                                                </span>
                                            </td>
                                            <td class="px-4 py-2 text-sm">
                                                <button 
                                                    @click="viewOutfitImage(outfit)"
                                                    class="text-blue-500 hover:text-blue-700"
                                                >
                                                    View Image
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div v-else class="text-gray-600 text-sm">No outfits available in this package.</div>
                    </div>
                    <div v-else class="text-gray-600 text-sm">No outfit package selected.</div>
                </div>

                <!-- Section for Additional Services -->
                <div class="bg-gray-300 w-full px-2 py-3 space-y-2 rounded-xl mt-4">
                    <p class="text-gray-700 font-semibold">Additional Services</p>
                    <button @click="showAdditionalServices = !showAdditionalServices" class="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        {{ showAdditionalServices ? 'Hide Services' : 'Show Services' }}
                    </button>
                    
                    <div v-if="showAdditionalServices" class="mt-2 overflow-y-auto max-h-64 space-y-2">
                        <div v-if="selectedWishlist.additional_services && selectedWishlist.additional_services.length > 0">
                            <div v-for="service in selectedWishlist.additional_services" :key="service.add_service_id" class="p-4 border rounded-lg bg-gray-100 shadow-sm">
                                <p class="font-semibold text-gray-800">{{ service.add_service_name }}</p>
                                <p class="text-gray-600">{{ service.add_service_description }}</p>
                                <p class="text-gray-600">Price: {{ formatPrice(service.add_service_price) }} php</p>
                                <p class="text-gray-600">Status: <span :class="{'text-green-600': service.status === 'Active', 'text-yellow-600': service.status === 'Pending', 'text-red-600': service.status === 'Cancelled'}">{{ service.status }}</span></p>
                                <p v-if="service.remarks" class="text-gray-600">Remarks: {{ service.remarks }}</p>
                            </div>
                        </div>
                        <p v-else class="text-gray-600">No additional services selected</p>
                    </div>
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



        <!-- Outfit Image Modal -->
        <div 
            v-if="selectedOutfit" 
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
            @click.self="selectedOutfit = null"
        >
            <div class="bg-white p-4 rounded-lg max-w-xl w-full mx-4">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-semibold">{{ selectedOutfit.outfit_name }}</h3>
                    <button @click="selectedOutfit = null" class="text-gray-500 hover:text-gray-700">
                        <span class="text-2xl">&times;</span>
                    </button>
                </div>
                <div class="flex justify-center">
                    <img 
                        :src="selectedOutfit.outfit_img" 
                        :alt="selectedOutfit.outfit_name" 
                        class="w-auto h-[400px] object-contain rounded-lg"
                    >
                </div>
                <div class="mt-4 text-sm text-gray-600">
                    <p><span class="font-medium">Type:</span> {{ selectedOutfit.outfit_type }}</p>
                    <p><span class="font-medium">Color:</span> {{ selectedOutfit.outfit_color }}</p>
                    <p v-if="selectedOutfit.outfit_desc"><span class="font-medium">Description:</span> {{ selectedOutfit.outfit_desc }}</p>
                    <p><span class="font-medium">Status:</span> <span :class="{'text-green-600': selectedOutfit.status === 'Active', 'text-yellow-600': selectedOutfit.status === 'Pending', 'text-red-600': selectedOutfit.status === 'Cancelled'}">{{ selectedOutfit.status }}</span></p>
                    <p v-if="selectedOutfit.remarks"><span class="font-medium">Remarks:</span> {{ selectedOutfit.remarks }}</p>
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
            selectedOutfit: null,
            activeNavButton: 'wishlist',
            
            // Display flags
            displayWishlist: true,
            displayEvents: false,
            displayCompleted: false,
            displayRated: false,
            displayCanceled: false,
            displayAll: false,
            displayBookedWishlist: true,
            displayBookedOutfits: false,

            // Data arrays
            bookedWishlist: [],
            bookedOutfits: [],

            // Modal toggles
            showSuppliers: false,
            showAdditionalServices: false,
        };
    },
    computed: {
        filteredWishlist() {
            if (!this.bookedWishlist) return [];
            
            let filtered;
            switch (this.activeNavButton) {
                case 'wishlist':
                    filtered = this.bookedWishlist.filter(item => item.event_status === 'Wishlist');
                    break;
                case 'events':
                    filtered = this.bookedWishlist.filter(item => item.package_status === 'Active');
                    break;
                case 'completed':
                    filtered = this.bookedWishlist.filter(item => item.package_status === 'Completed');
                    break;
                case 'rated':
                    filtered = this.bookedWishlist.filter(item => item.package_status === 'Rated');
                    break;
                case 'canceled':
                    filtered = this.bookedWishlist.filter(item => item.package_status === 'Cancelled');
                    break;
                case 'all':
                default:
                    filtered = this.bookedWishlist;
            }
            
            return filtered;
        }
    },
    created() {
        this.fetchBookedWishlist();
        this.fetchBookedOutfits();
    },
    methods: {
        setActiveNav(type) {
            this.activeNavButton = type;
            // Reset all display flags
            this.displayWishlist = false;
            this.displayEvents = false;
            this.displayCompleted = false;
            this.displayRated = false;
            this.displayCanceled = false;
            this.displayAll = false;

            // Set the appropriate display flag
            switch (type) {
                case 'wishlist':
                    this.displayWishlist = true;
                    break;
                case 'events':
                    this.displayEvents = true;
                    break;
                case 'completed':
                    this.displayCompleted = true;
                    break;
                case 'rated':
                    this.displayRated = true;
                    break;
                case 'canceled':
                    this.displayCanceled = true;
                    break;
                case 'all':
                    this.displayAll = true;
                    break;
            }
        },
        
        toggleWishlistDisplay() {
            this.displayBookedWishlist = true;
        },
        
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

        formatPrice(price) {
            if (price === null || price === undefined || isNaN(price)) {
                return 'N/A'; // Return a fallback if price is invalid
            }
            // Round the price to 2 decimal places and format with commas
            return parseFloat(price).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        },

        async fetchBookedWishlist() {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    console.error('No access token found');
                    this.$router.push('/login');
                    return;
                }

                const response = await axios.get('http://127.0.0.1:5000/wishlist', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    withCredentials: true
                });
                
                this.bookedWishlist = response.data;
            } catch (error) {
                console.error('Error fetching booked wishlist:', error);
                if (error.response?.status === 401) {
                    // Token expired or invalid
                    localStorage.removeItem('access_token');
                    this.$router.push('/login');
                } else if (error.response?.status === 422) {
                    // Invalid data format
                    console.error('Invalid data format:', error.response.data);
                }
            }
        },

        async deleteWishlistItem(events_id) {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    console.error('No access token found');
                    this.$router.push('/login');
                    return;
                }

                const response = await axios.delete(`http://127.0.0.1:5000/booked_wishlist/${events_id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.status === 200) {
                    this.bookedWishlist = this.bookedWishlist.filter(item => item.events_id !== events_id);
                    alert('Event item deleted successfully!');
                    this.selectedWishlist = null;  // Changed from false to null to match the data type
                    this.closeWishlistModal();
                }
            } catch (error) {
                console.error('Error deleting event item:', error);
                if (error.response?.status === 401) {
                    // Token expired or invalid
                    localStorage.removeItem('access_token');
                    this.$router.push('/login');
                } else {
                    alert('Failed to delete event item. Please try again.');
                }
            }
        },

        displayWishlistDetails(item) {
            // Ensure outfits are properly formatted
            if (item.outfits && Array.isArray(item.outfits)) {
                this.selectedWishlist = item;
            } else {
                // Create empty outfits array if none exists
                this.selectedWishlist = {
                    ...item,
                    outfits: []
                };
            }
        },
        closeWishlistModal() {
            this.selectedWishlist = null;
            this.showSuppliers = false;
            this.showAdditionalServices = false;
        },

        async fetchBookedOutfits() {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    console.error('No access token found');
                    this.$router.push('/login');
                    return;
                }

                const response = await axios.get('http://127.0.0.1:5000/booked-outfits', {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    withCredentials: true
                });
                this.bookedOutfits = response.data;
            } catch (error) {
                console.error('Error fetching booked outfits:', error);
                if (error.response?.status === 401) {
                    // Token expired or invalid
                    localStorage.removeItem('access_token');
                    this.$router.push('/login');
                } else if (error.response?.status === 422) {
                    // Invalid data format
                    console.error('Invalid data format:', error.response.data);
                }
            }
        },
        viewOutfitImage(outfit) {
            if (outfit && outfit.outfit_img) {
                this.selectedOutfit = outfit;
            } else {
                alert('No image available for this outfit.');
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