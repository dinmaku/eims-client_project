<template>
    <div class="h-full overflow-y-auto overflow-x-hidden">
      <!-- Header with responsive layout -->
      <div class="flex justify-between items-center w-full h-20 bg-gray-100 shadow-lg antialiased mt-28 px-4 sm:px-6 lg:px-8">
        <h1 class="flex font-medium font-amaticBold text-2xl ml-5 sm:text-xl">My Booked Schedule</h1>
      </div>
  
      <!-- Sidebar (will slide in/out based on isSidebarOpen) -->
      <aside class="fixed top-0 right-0 w-full md:w-[450px] h-full bg-[#f8f9ef] shadow-lg transition-transform z-50 custom-shadow" :class="isSidebarOpen ? 'translate-x-0' : 'translate-x-full'">
        <div class="p-4">
          <div class="flex items-center">
            <button @click="toggleSidebar" class="px-3 h-8 text-md bg-gray-200 font-bold rounded-full transform-transition duration-300 transform hover:scale-110">X</button>
          </div>
          <h2 class="text-xl font-semibold">Schedule Event</h2>
          <p class="mb-10 text-base text-gray-500">Capture your upcoming events in one place.</p>
  
          <form @submit.prevent="addEvent">
            <div class="mt-8 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-2 font-raleway">Event Name: </label>
                <input type="text" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="eventTitle" v-model="eventTitle" required />
              </div>
            </div>
            <div class="mt-8 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-2 font-raleway">Venue: </label>
                <input type="text" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="eventVenue" v-model="eventVenue" required />
              </div>
            </div>
            <div class="mt-8 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">Date: </label>
                <input type="date" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="eventDate" v-model="eventDate" required />
              </div>
            </div>
            <div class="mt-12 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">Start Time: </label>
                <input type="time" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="startTime" v-model="eventStartTime" required />
              </div>
            </div>
            <div class="mt-4 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">End Time: </label>
                <input type="time" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="endTime" v-model="eventEndTime" required />
              </div>
            </div>
  
            <div class="mt-10">
              <button type="submit" class="h-10 bg-blue-400 text-md font-bold px-2 rounded-lg shadow-lg w-full sm:w-auto">
                Set Schedule
              </button>
            </div>
          </form>
        </div>
      </aside>
  
      <!-- Modal for Event Details -->
      <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="modal-overlay absolute inset-0 bg-black opacity-50"></div>
        <div class="modal-content bg-white rounded-lg overflow-hidden shadow-lg z-50">
          <div class="p-10">
            <h2 class="text-lg font-bold mb-10 text-gray-800">Scheduled Event Details</h2>
            <p class="mb-2"><strong>Name:</strong> {{ selectedEvent.title }}</p>
            <p class="mb-2"><strong>Venue:</strong> {{ selectedEvent.extendedProps.venue }}</p>
            <p class="mb-2"><strong>Start:</strong> {{ selectedEvent.start }}</p>
            <p class="mb-2"><strong>End:</strong> {{ selectedEvent.end }}</p>
            <div class="mt-8 flex justify-end">
              <button @click="editEvent" class="mr-2 bg-blue-500 text-black px-4 py-2 rounded">Edit</button>
              <button @click="closeModal" class="ml-2 bg-gray-300 text-gray-800 px-4 py-2 rounded">Close</button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- FullCalendar View -->
      <div class="flex justify-start ml-12 items-center h-screen mb-10 py-5">
        <div class="w-full max-w-4xl h-full">
          <FullCalendar :options="calendarOptions" class="w-full h-full font-merriweatherRegular" />
        </div>
      </div>
    </div>
  </template>
  
  
  <script>
  import FullCalendar from '@fullcalendar/vue3'
  import dayGridPlugin from '@fullcalendar/daygrid'
  import interactionPlugin from '@fullcalendar/interaction'
  
  export default {
    components: {
      FullCalendar
    },
    data() {
    return {
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        dateClick: this.handleDateClick,
        events: [],
        eventContent: this.renderEvent,
        eventClick: this.handleEventClick,
        timeZone: 'Asia/Manila',
      },
      isSidebarOpen: false,
      isModalOpen: false,
      selectedEvent: null,
      eventTitle: '',
      eventDate: '',
      eventVenue: '',
      eventStartTime: '',
      eventEndTime: '',
  
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    },
    addEvent() {
      if (this.eventTitle && this.eventDate && this.eventVenue && this.eventStartTime && this.eventEndTime) {
        const newEvent = {
          title: this.eventTitle,
          start: `${this.eventDate}T${this.eventStartTime}:00`, 
          end: `${this.eventDate}T${this.eventEndTime}:00`, 
          extendedProps: {
          venue: this.eventVenue,
          },
          backgroundColor: '#1E90FF',
          borderColor: '#1E90FF',
        };
        
        this.calendarOptions.events.push(newEvent);
        
        // Reset form fields
        this.eventTitle = ''; 
        this.eventDate = '';
        this.eventVenue = '';
        this.eventStartTime = '';
        this.eventEndTime = '';
        
        this.toggleSidebar(); // Close the sidebar after adding
      }
    },
    renderEvent(eventInfo) {
      const eventTitle = eventInfo.event.title;
      const eventBackgroundColor = eventInfo.event.backgroundColor || '#ffffff'; 
  
      const element = document.createElement('div');
      element.innerText = eventTitle;
      element.style.backgroundColor = eventBackgroundColor;
      element.style.padding = '5px';
      element.style.borderRadius = '4px';
      element.style.color = '#fff';
  
      return { html: element.outerHTML };
    },
    handleEventClick(info) {
      this.selectedEvent = info.event; // Get the clicked event
      this.isModalOpen = true; // Open the modal
    },
    closeModal() {
      this.isModalOpen = false; // Close the modal
    },
    editEvent() {
      if (this.selectedEvent) {
        this.eventTitle = this.selectedEvent.title;
        this.eventDate = this.selectedEvent.start.toISOString().split('T')[0]; // Format date
        this.eventVenue = this.selectedEvent.extendedProps.venue;
        this.eventStartTime = this.selectedEvent.start.toTimeString().split(' ')[0]; // Format time
        this.eventEndTime = this.selectedEvent.end.toTimeString().split(' ')[0]; // Format time
        this.isModalOpen = false; // Close the modal
        this.toggleSidebar(); // Open sidebar for editing
      }
    },
    deleteEvent() {
      if (this.selectedEvent) {
        this.calendarOptions.events = this.calendarOptions.events.filter(event => event !== this.selectedEvent);
        this.isModalOpen = false; // Close the modal
      }
    },
  },
  }
  </script> 
  <style scoped>
  .custom-shadow {
    box-shadow: 1px 0 8px rgba(0, 0, 0, 0.2); 
  }
  
  </style>