<template>
    <div class="bg-[url('/img/background.jpg')] bg-cover bg-center h-screen">
      <div class="flex flex-col items-center justify-center h-full space-y-6">
        <h1 class="font-pacifico text-5xl sm:text-6xl md:text-7xl text-gray-100 font-medium italic">
            Crafting Memories
        </h1>
        <p class="font-medium font-raleway text-lg sm:text-xl text-white">
            We weave unforgettable Wedding Stories
        </p> 
        <button @click="wishlistBtn" class="h-12 bg-white px-4 rounded-full shadow-lg tracking-wide font-medium font-raleway 
        transition-transform duration-700 transform hover:scale-110 hover:bg-yellow-300 
        hover:text-gray-50 hover:tracking-wider hover:shadow-md hover:shadow-yellow-300">
         Add to Wishlist
        </button>
        </div>
      </div>

  <div v-if="wishlistAlert" class="fixed inset-0 z-50 flex items-center justify-center">
  <div class="flex flex-col gap-2 w-60 sm:w-72 text-[10px] sm:text-xs">
    <div class="error-alert cursor-default flex items-center justify-between w-full h-12 sm:h-14 rounded-lg bg-[#232531] px-[10px] shadow-lg">
      <div class="flex gap-2">
        <div class="text-[#d65563] bg-white/5 backdrop-blur-xl p-1 rounded-lg">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
            ></path>
          </svg>
        </div>
        <div>
          <p class="text-white">Please try again</p>
          <p class="text-gray-500">Logging in is required!</p>
        </div>
      </div>
    </div>
  </div>
</div>


      
      <div class ="w-full h-[600px] bg-gray-100">
        <div class = "flex justify-center">
            <div class="flex flex-col text-center items-center mt-10 space-y-4">
                <h1 class="font-semibold font-merriweatherBoldItalic text-3xl md:text-4xl italic text-gray-800">
                    Welcome to Red Carpet, A premier wedding and event
                </h1>
                <h1 class="font-semibold font-merriweatherBoldItalic text-3xl md:text-4xl italic text-gray-800">
                    planning company in Iligan City, Philippines.
                </h1>
            </div>
        </div>
        
        <div class = "flex justify-center items-center mt-10">
            <img src="/img/services.png" alt="" class="max-w-xl sm:max-w-2xl md:max-w-3xl lg:max-w-4xl xl:max-w-5xl w-full h-auto">
        </div>
      </div>


      <div class="bg-[url('/img/background-aboutus.jpg')] bg-cover bg-center h-screen">
        <div class="flex justify-end mr-14 h-full">
        <div class="bg-gray-200 w-[660px] h-full flex flex-col justify-start"> 
        <div class="space-y-5 text-center mt-40">
            <h1 class="font-semibold lg:text-5xl font-merriweatherRegular text-gray-800 tracking-wider indent-10">About Us</h1>
            <p class="font-semibold md:text-1xl font-raleway tracking-widest text-gray-500">DISCOVER OUR STORY</p>
        </div>
        <div class="flex justify-center mt-12">
            <p class="text-center md:text-md px-10 font-medium font-raleway text-gray-700">
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
            </p>
        </div>
            <div class = "flex justify-center mt-24">
              <button class = "bg-gray-800 text-white py-2 px-5 rounded-lg shadow-xl font-medium transition-transform duration-300 transform hover:scale-105">
                Check the full story
              </button>
            </div>
        </div>
        
    </div>
     </div>


     
  <section class="bg-white dark:bg-gray-900">
  <div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6 ">
      <div class="mx-auto max-w-screen-sm text-center mb-8 lg:mb-16">
        <h2 class="mb-4 text-4xl font-raleway tracking-tight font-extrabold text-gray-900 dark:text-white">Our Team</h2>
        <p class="font-light text-gray-500 lg:mb-16 sm:text-xl dark:text-gray-400">Meet the passionate team behind our innovative event management platform, dedicated to enhancing your event experience</p>
      </div> 
      <div class="grid gap-8 mb-6 lg:mb-5 md:grid-cols-2">
          <div class="items-center bg-gray-50 rounded-lg shadow sm:flex dark:bg-gray-800 dark:border-gray-700">
              <a href="#">
                  <img class="w-full rounded-lg sm:rounded-none sm:rounded-l-lg" src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/avatars/sofia-mcguire.png" alt="Bonnie Avatar">
              </a>
              <div class="p-5">
                  <h3 class="text-xl font-bold tracking-tight text-gray-900 dark:text-white">
                      <a href="#">Ashley Calimpong</a>
                  </h3>
                  <span class="text-gray-500 dark:text-gray-400">Manager of Red Carpet</span>
                  <p class="mt-3 mb-4 font-light text-sm text-gray-500 dark:text-gray-400">Ashley shapes operational excellence in our event management system, for efficiency and user satisfaction.</p>
                  <ul class="flex space-x-4 sm:mt-0">
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                        <span class="inline-block">
                            <img src="/img/instagram.png" alt="Instagram" class="w-5 h-5">
                        </span>
                           </a>
                      </li>
                      <li>
                        <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                        <span class="inline-block">
                            <img src="/img/mail.png" alt="Instagram" class="w-5 h-5">
                        </span>
                           </a>
                      </li>
                  </ul>
              </div>
          </div> 
          <div class="items-center bg-gray-50 rounded-lg shadow sm:flex dark:bg-gray-800 dark:border-gray-700">
              <a href="#">
                  <img class="w-full rounded-lg sm:rounded-none sm:rounded-l-lg" src="/img/ID.jpg" alt="Jese Avatar">
              </a>
              <div class="p-5">
                  <h3 class="text-xl font-bold tracking-tight text-gray-900 dark:text-white">
                      <a href="#">Dean Mark Belano</a>
                  </h3>
                  <span class="text-gray-500 dark:text-gray-400">Developer of Red Carpet</span>
                  <p class="mt-3 mb-4 font-light text-sm text-gray-500 dark:text-gray-400">
                    Dean leads the development of our red carpet system, prioritizing efficient architecture and usability.</p>
                  <ul class="flex space-x-4 sm:mt-0">
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                        <span class="inline-block">
                            <img src="/img/instagram.png" alt="Instagram" class="w-5 h-5">
                        </span>
                           </a>
                      </li>
                      <li>
                        <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                        <span class="inline-block">
                            <img src="/img/mail.png" alt="Instagram" class="w-5 h-5">
                        </span>
                           </a>
                      </li>
                  </ul>
              </div>
          </div> 
          <div class="items-center bg-gray-50 rounded-lg shadow sm:flex dark:bg-gray-800 dark:border-gray-700">
              <a href="#">
                  <img class="w-full rounded-lg sm:rounded-none sm:rounded-l-lg" src="/img/kim-img.jpg" alt="Michael Avatar">
              </a>
              <div class="p-5">
                  <h3 class="text-xl font-bold tracking-tight text-gray-900 dark:text-white">
                      <a href="#">Kimberly Deloso</a>
                  </h3>
                  <span class="text-gray-500 dark:text-gray-400">Project Manager of Red Carpet</span>
                  <p class="mt-3 mb-4 font-light text-sm text-gray-500 dark:text-gray-400">Kimberly coordinates red carpet system initiatives, prioritizing efficiency and collaboration</p>
                  <ul class="flex space-x-4 sm:mt-0">
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                        <span class="inline-block">
                            <img src="/img/instagram.png" alt="Instagram" class="w-5 h-5">
                        </span>
                           </a>
                      </li>
                      <li>
                        <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                        <span class="inline-block">
                            <img src="/img/mail.png" alt="Instagram" class="w-5 h-5">
                        </span>
                           </a>
                      </li>
                  </ul>
              </div>
          </div> 
          <div class="items-center bg-gray-50 rounded-lg shadow sm:flex dark:bg-gray-800 dark:border-gray-700">
              <a href="#">
                  <img class="w-full rounded-lg sm:rounded-none sm:rounded-l-lg" src="/img/rozl-img.jpg" alt="Sofia Avatar">
              </a>
              <div class="p-5">
                  <h3 class="text-xl font-bold tracking-tight text-gray-900 dark:text-white">
                      <a href="#">Rozl Anne Looc</a>
                  </h3>
                  <span class="text-gray-500 dark:text-gray-400">Project Coordinator</span>
                  <p class="mt-3 mb-4 font-light text-sm text-gray-500 dark:text-gray-400">Rozl organizes meetings and documentation, supporting project alignment and stakeholder engagement</p>
                  <ul class="flex space-x-4 sm:mt-0">
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" /></svg>
                          </a>
                      </li>
                      <li>
                          <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                        <span class="inline-block">
                            <img src="/img/instagram.png" alt="Instagram" class="w-5 h-5">
                        </span>
                           </a>
                      </li>
                      <li>
                        <a href="#" class="text-gray-500 hover:text-gray-900 dark:hover:text-white">
                        <span class="inline-block">
                            <img src="/img/mail.png" alt="Instagram" class="w-5 h-5">
                        </span>
                           </a>
                      </li>
                  </ul>
              </div>
          </div>  
      </div>  
  </div>
  </section>

  <section class="bg-gray-300 h-screen flex items-center justify-center mb-10 overflow-y-auto" > 
  <div class="w-full h-full bg-gray-50 flex flex-col md:flex-row items-start justify-start">
    <div class="flex flex-col m-5 space-y-1">
      <h1 class="md:text-3xl text-2xl font-semibold font-raleway">Package Deal</h1>
      <p class="md:text-sm text-xs font-medium font-raleway tracking-wide text-gray-600 indent-5">Explore Package Offers</p>
    </div>
    <div class="flex flex-wrap justify-center mt-10 md:mt-20">
      <!-- Basic Package -->
      <div class="flex flex-col bg-[#f7c5f7] rounded-3xl m-2 md:m-5 w-full sm:w-[300px] h-auto shadow-md">
        <div class="px-6 py-8 sm:p-10 sm:pb-6">
          <div class="grid items-center justify-center w-full grid-cols-1 text-left">
            <div>
              <h2 class="text-lg font-medium tracking-tighter text-gray-600 lg:text-3xl">Package A</h2>
              <p class="mt-2 text-sm text-gray-500 font-raleway">Essential for your wedding.</p>
            </div>
            <div class="mt-6">
              <p>
                <span class="text-4xl font-light tracking-tight text-black">160k / 198k</span>
                <span class="text-sm font-medium text-gray-500 ml-2">php</span>
              </p>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Reception Venue</span>
            </div>
            <div class="flex mt-1 ml-7">
              <span class="text-xs font-medium text-gray-800">Creative design of lively decors</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Stage Decor</span>
            </div>
            <div class="flex mt-1 ml-7">
              <span class="text-xs font-medium text-gray-800">Beautiful Backdrop</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Entrance</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Bouquet</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Premium Package -->
      <div class="flex flex-col bg-blue-300 rounded-3xl m-2 md:m-5 w-full sm:w-[300px] h-auto shadow-md">
        <div class="px-6 py-8 sm:p-10 sm:pb-6">
          <div class="grid items-center justify-center w-full grid-cols-1 text-left">
            <div>
              <h2 class="text-lg font-medium tracking-tighter text-gray-600 lg:text-3xl">Package B</h2>
              <p class="mt-2 text-sm text-gray-500 font-raleway">Enhanced elegance and details.</p>
            </div>
            <div class="mt-6">
              <p>
                <span class="text-4xl font-light tracking-tight text-black">205k / 243k</span>
                <span class="text-sm font-medium text-gray-500 ml-2">php</span>
              </p>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Everything in package A</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Ceiling Works</span>
            </div>
            <div class="flex mt-1 ml-7">
              <span class="text-xs font-medium text-gray-800">Stylish stands with flower</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-1">
              <span class="text-base font-semibold text-gray-800">Vanity Wall with couple's name</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Bouquet</span>
            </div>
            <div class="flex mt-1 ml-7">
              <span class="text-xs font-medium text-gray-800">Premium flowers</span>
            </div>
          </div>
        </div>
      </div>

      <!-- VIP Package -->
      <div class="flex flex-col bg-yellow-300 rounded-3xl m-2 md:m-5 w-full sm:w-[300px] h-auto shadow-md">
        <div class="px-6 py-8 sm:p-10 sm:pb-6">
          <div class="grid items-center justify-center w-full grid-cols-1 text-left">
            <div>
              <h2 class="text-lg font-medium tracking-tighter text-gray-600 lg:text-3xl">Package C</h2>
              <p class="mt-2 text-sm text-gray-500 font-raleway">Ultimate night experience.</p>
            </div>
            <div class="mt-6">
              <p>
                <span class="text-4xl font-light tracking-tight text-black">255k / 288k</span>
                <span class="text-sm font-medium text-gray-500 ml-2">php</span>
              </p>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Everything in Package B</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Elegant Grand Entrance Arch</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Customized drapery and linens</span>
            </div>
            <div class="flex mt-4">
              <img src="/img/check-icon.png" alt="" class="w-5 h-5 mr-2">
              <span class="text-base font-semibold text-gray-800">Themed table settings</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="w-full bg-gray-100 py-10">
  <div class="flex flex-col md:flex-row justify-between items-center mx-10 mb-10"> 
    <div class="flex flex-col mb-4 md:mb-0">
      <h1 class="text-4xl font-bold font-merriweatherRegular tracking-wide">Gowns and Tuxedo</h1>
      <p class="text-gray-600 font-raleway font-medium">Discover our Collection</p>
    </div>
    <button class="font-medium text-blue-700 text-xl font-raleway hover:underline">
      View More &#8594;
    </button>
  </div>

  <div class="flex overflow-hidden">
    <transition name="fade">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full" :key="currentIndex">
        <div class="flex p-4 min-h-[250px]">
          <div class="bg-white rounded-lg shadow-lg overflow-hidden w-full flex py-2">
            <img :src="currentGown.img" alt="Gown" class="w-1/4 h-48 object-cover rounded-l-lg mt-7 ml-3" />
            <div class="flex flex-col justify-center p-4 w-2/3 space-y-2">
              <h3 class="text-lg font-semibold">{{ currentGown.name }}</h3>
              <p class="text-gray-600">{{ currentGown.description }}</p>
              <p class="text-xl font-bold mt-2">{{ currentGown.price }}</p>
            </div>
          </div>
        </div>

        <div class="flex p-4 min-h-[250px]">
          <div class="bg-white rounded-lg shadow-lg overflow-hidden w-full flex py-2">
            <img :src="currentTuxedo.img" alt="Tuxedo" class="w-[200px] h-48 object-cover rounded-l-lg mt-7 ml-3" />
            <div class="flex flex-col justify-center p-4 w-2/3 space-y-2 ml-5">
              <h3 class="text-lg font-semibold">{{ currentTuxedo.name }}</h3>
              <p class="text-gray-600">{{ currentTuxedo.description }}</p>
              <p class="text-xl font-bold mt-2">{{ currentTuxedo.price }}</p>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>

  <div class="flex justify-center space-x-4 mt-5">
    <button @click="prevItem" class="text-5xl text-gray-500 hover:text-gray-800 transition-transform duration-300 transform hover:scale-110">
      &larr;
    </button>
    <button @click="nextItem" class="text-5xl text-gray-500 hover:text-gray-800 transition-transform duration-300 transform hover:scale-110">
      &rarr;
    </button>
  </div>
</section>



<section class="bg-[url('/img/ourteam-img.jpg')] bg-cover bg-center h-screen flex items-center justify-center">
  <div class="bg-gray-200 dark:bg-gray-900 w-full max-w-[1000px] h-full p-4">
    <div class="flex flex-col items-start my-8 mx-5 space-y-2">
      <h1 class="text-5xl font-bold font-merriweatherRegular tracking-wide">Gallery</h1>
      <p class="text-gray-600 font-raleway font-medium">Check our Recent Events</p>
    </div>
    <div class="grid gap-4">
      <!-- Expanded Image Section -->
      <div v-if="selectedImage" class="flex justify-center">
        <img 
          class="h-auto w-full max-w-[90%] rounded-lg object-cover object-center md:h-[480px] lg:max-w-[80%]"
          :src="selectedImage" 
          alt="" 
        />
      </div>
      
      <!-- Thumbnails Slider Section -->
      <div class="overflow-x-auto whitespace-nowrap flex justify-center">
        <div class="inline-flex space-x-2">
          <div 
            v-for="image in images" 
            :key="image" 
            @click="expandImage(image)"
            class="cursor-pointer"
          >
            <img
              :src="image"
              class="object-cover object-center h-20 rounded-lg" 
              alt="gallery-image" 
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</section>


  <section class="w-full h-[500px] bg-gray-50">
    <div class="w-full h-[500px] bg-gray-700">
      <div class = "flex justify-between m-5">
         <div class = "flex flex-col my-5 space-y-2">
            <p class ="text-md font-medium font-poppins text-gray-300">Contact Us</p>
            <span class = "text-md md:text-2xl font-semibold text-white font-poppins indent-5">09123456781</span>
            <span class = "text-md md:text-2xl font-semibold text-white font-poppins indent-5">225-0665</span>
         </div>
        <div class = "flex flex-col text-center my-5 space-y-2">
          <p class ="text-md font-medium font-poppins text-gray-300">Email us for support</p>
          <span class ="text-md md:text-2xl font-medium font-raleway text-yellow-300 ml-3">redcarpet.events@gmail.com</span>
      </div>
         <div class = "flex flex-col text-center my-5 space-y-2 mx-7">
        <p class ="text-md font-medium font-poppins text-gray-300">Follow us on</p>
        <div class = "flex items-center space-x-2">
            <a href="#" class = "text-xl font-semibold text-white font-poppins"><img src="/img/facebook.png" alt="facebook-logo" class="h-6 w-6 md:h-8 md:w-8 transition-transform duration-300 transform hover:scale-110"></a>
            <a href="#" class = "text-xl font-semibold text-white font-poppins"><img src="/img/instagram-black.png" alt="instagram-logo" class="h-6 w-6 md:h-8 md:w-8 transition-transform duration-300 transform hover:scale-110"></a>
            <a href="#" class = "text-xl font-semibold text-white font-poppins"><img src="/img/twitter.png" alt="twitter-logo" class="h-6 w-6 md:h-8 md:w-8 transition-transform duration-300 transform hover:scale-110"></a>
            <a href="#" class = "text-xl font-semibold text-white font-poppins"><img src="/img/linkedin.png" alt="twitter-logo" class="h-6 w-6 md:h-8 md:w-8 transition-transform duration-300 transform hover:scale-110"></a>
          </div>  
        </div>
       
        
      </div>
      <hr class="border-t border-gray-300 my-8 w-[90%] mx-auto" />

      <div class="flex justify-between m-5 mx-7">
    <div class="flex flex-col my-5">
        <h1 class="text-5xl font-semibold text-gray-50 font-dancing mb-5">RedCarpet</h1>
        <p class="text-start text-sm md:text-md font-medium text-gray-200 font-raleway">
            "From all of us, we believe every occasion deserves to be extraordinary. 
           <p class ="text-start text-sm md:text-md font-medium text-gray-200 font-raleway"> We appreciate your trust in us to make your events remarkable and </p>
           <p class ="text-start text-sm md:text-md font-medium text-gray-200 font-raleway"> look forward to bringing even more brilliance to your future celebrations."</p>
        </p>
    </div>
    <div class="flex flex-col text-center space-y-5 ml-5">
      <p class = "text-md font-medium font-poppins text-gray-300 ml">Explore</p>
      <ul class ="font-semibold text-lg text-center text-gray-50 space-y-1">
        <li class="transition-transform duration-300 transform hover:scale-105 hover:underline" ><a href="">About Us</a></li>
        <li class="transition-transform duration-300 transform hover:scale-105 hover:underline" ><a href="">OurTeam</a></li>
        <li class="transition-transform duration-300 transform hover:scale-105 hover:underline" ><a href="">Gallery</a></li>
      </ul>
    </div>

    <div class="flex flex-col items-end space-y-3 mt-10 mx-4 md:mt-20 md:mx-7">
      <p class="font-semibold font-poppins text-gray-200 text-center md:text-right">
        &copy; 2024 Red Carpet Services. All rights reserved.
      </p>
      <p class="font-semibold font-poppins text-gray-200 text-center md:text-right">
        @MSU, Naawan
      </p>
    </div>

</div>

    </div>
    
  </section>

  








    
  </template>
  
  <script>


  export default {
    name: 'Home',

    data() {
    return {
      selectedImage: null,
      wishlistAlert: false,

      images: [
        "/img/gallery-img1.png",
        "/img/gallery-img2.png",
        "/img/gallery-img3.jpg",
        "/img/gallery-img4.png",
        "/img/gallery-img5.png",
      ],
      gowns: [
        { name: 'Royal Blue Evening Gown', description: 'Sequined blue gown with sweetheart neckline.', price: '₱2,000', img: '/img/img-gown/gown1.png' },
        { name: 'Vintage Lace Gown', description: 'Charming vintage gown with lace overlay.', price: '₱3,000', img: '/img/img-gown/gown2.png' },
        { name: 'Bohemian Dream Gown', description: 'Whimsical gown with flowing sleeves.', price: '₱1,500', img: '/img/img-gown/gown3.png' },
        { name: 'Simple Satin Gown', description: 'Elegant satin gown with timeless design.', price: '₱1,200', img: '/img/img-gown/gown4.png' },
        { name: 'Romantic Ball Gown', description: 'Classic chiffon A-line gown with train.', price: '₱1,800', img: '/img/img-gown/gown5.png' },
      ],
      tuxedos: [
        { name: 'Classic Black Tuxedo', description: 'Timeless black tuxedo with satin lapels.', price: '₱2,800', img: '/img/img-tuxedo/tuxedo1.png' },
        { name: 'Velvet Tuxedo', description: 'Luxurious velvet tuxedo for standout occasions.', price: '₱4,500', img: '/img/img-tuxedo/tuxedo2.png' },
        { name: 'Midnight Blue Tuxedo', description: 'Elegant blue tuxedo with a modern cut.', price: '₱3,200', img: '/img/img-tuxedo/tuxedo3.png' },
        { name: 'White Dinner Jacket', description: 'Stylish white jacket for formal events.', price: '₱2,500', img: '/img/img-tuxedo/tuxedo4.png' },
        { name: 'Black Shawl Lapel Tuxedo', description: 'Classic black tuxedo with shawl lapel.', price: '₱3,000', img: '/img/img-tuxedo/tuxedo5.png' },
        { name: 'Patterned Tuxedo', description: 'Unique patterned tuxedo for trendy looks.', price: '₱3,500', img: '/img/img-tuxedo/tuxedo6.png' },
        { name: 'Burgundy Tuxedo', description: 'Rich burgundy tuxedo for special events.', price: '₱3,300', img: '/img/img-tuxedo/tuxedo7.png' },
      ],
    currentIndex: 0,
    
    };
  },
  created() {
    this.selectedImage = this.images[0];
  },
  computed: {
    currentGown() {
      return this.gowns[this.currentIndex % this.gowns.length];
    },
    currentTuxedo() {
      return this.tuxedos[this.currentIndex % this.tuxedos.length];
    },
  },
  methods: {
    expandImage(image) {
      this.selectedImage = image;
    },
    nextItem() {
      this.currentIndex++;
    },
    prevItem() {
      this.currentIndex--;
    },
    wishlistBtn() {
      const loggedIn = localStorage.getItem('loggedIn') === 'true'; 
      if (loggedIn) {
        this.$router.push('/add-wishlist');
      } else {
        this.wishlistAlert = true;
          setTimeout(() => {
        this.wishlistAlert = false;
        }, 3000); 
        
      }
    },
  },
  
 };
  </script>
  
  <style scoped>
    .bg-transparent-important {
    background-color: transparent !important;
    }
    .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0;
    }
  </style>