<template>
    <!-- Login Form -->
    <form v-if="loginForm" @click.self="closeLoginForm" @submit.prevent="handleLogin" class="flex justify-center items-center fixed inset-0 bg-gray-800 bg-opacity-70">
        <div class="bg-white w-full sm:w-1/3 h-4/5 p-7 rounded-lg shadow-xl overflow-y-hidden mr-2">
            
            <div class="flex flex-col justify-center items-center space-y-3 mt-5">
                <h1 class="text-3xl font-amaticBold font-extrabold text-blue-900">Sign In</h1>
                <p class="font-raleway font-medium text-sm tracking-wide text-gray-500 mt-2">Enter your email and password</p>
                <button class="flex justify-center items-center w-full h-12 bg-gray-100 rounded-xl hover:bg-gray-200">
                    <img src="/img/google.png" class="h-6 mr-4">Continue with Google
                </button>
                <div class="flex items-center my-4 w-full">
                    <div class="flex-grow border-t border-gray-300"></div>
                    <span class="mx-4 text-gray-600">or</span>
                    <div class="flex-grow border-t border-gray-300"></div>
                </div>
            </div>
            <div class="flex flex-col justify-start items-start mt-5 space-y-2">
                <p class="text-sm text-red-600" v-if="errorMessage">{{ errorMessage }}</p>
                <label for="emailInput" class="text-left text-sm text-gray-800">Email Address or Username</label>
                <input type="text" id="emailInput" v-model="identifier" class="mt-1 border border-gray-300 rounded pl-3 p-2 w-full h-10 font-medium text-sm" required/>
            </div>
            <div class="flex flex-col justify-start items-start mt-5 space-y-2">
                <label for="passwordInput" class="text-left text-sm text-gray-800">Password</label>
                <input type="password" id="passwordInput" v-model="password" class="mt-1 border border-gray-300 rounded pl-3 p-2 w-full h-10 font-medium text-sm" required/>
            </div>
            <div class="flex justify-between items-center mt-3">
                <div class="flex items-center">
                    <input type="checkbox" class="mr-2 bg-white border-2 rounded-sm border-gray-500">
                    <label class="text-sm text-gray-700">Keep me logged in</label>
                </div>
                <button class="text-sm text-blue-900 hover:text-blue-800">Forget password?</button>
            </div>
            <button type="submit" class="mt-8 w-full h-10 bg-blue-700 text-white rounded-lg shadow-md hover:bg-blue-500">Sign in</button>
            <div class="flex justify-center items-center mt-4 space-x-1">
                <p class="text-sm text-gray-700 font-medium">Not registered yet?</p>
                <button type="button" @click="showRegisterForm" class="text-sm hover:underline">Create an Account</button>
            </div>
        </div>
    </form>

    <!-- Register Form -->
    <form v-if="registerForm" @click.self="closeRegisterForm" @submit.prevent="handleRegister" class="flex justify-center items-center fixed inset-0 bg-gray-800 bg-opacity-70">
        <div class="bg-white w-full sm:w-[45%] h-[98%] p-7 rounded-lg shadow-xl overflow-y-auto mr-2">
            <div class="flex flex-col justify-start items-start space-y-1">
                <h1 class="text-2xl font-amaticBold font-extrabold text-blue-900">Create your account</h1>
                <div class="flex justify-center items-center mt-4 space-x-1">
                    <p class="font-raleway font-medium text-sm tracking-wide text-gray-500">Already have an account?</p>
                    <button type="button" @click="showLoginForm" class="text-sm font-raleway font-medium hover:underline">Login here!</button>
                </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-7">
                <div class="flex flex-col">
                    <label for="firstName" class="text-left text-sm text-gray-800">First Name</label>
                    <input type="text" v-model="firstName" id="firstName" class="border border-gray-300 rounded pl-3 p-2 h-9 font-medium text-sm mt-2 bg-gray-50" required>
                </div>
                <div class="flex flex-col">
                    <label for="lastName" class="text-left text-sm text-gray-800">Last Name</label>
                    <input type="text" v-model="lastName" id="lastName" class="border border-gray-300 rounded pl-3 p-2 h-9 font-medium text-sm mt-2 bg-gray-50" required>
                </div>
            </div>
            <div class="flex flex-col justify-start items-start mt-3 space-y-2">
                <label for="address" class="text-left text-sm text-gray-800">Username</label>
                <input type="text" v-model="username" class="mt-1 border border-gray-300 rounded pl-3 p-2 w-full h-9 font-medium text-sm bg-gray-50" required>
            </div>
            <div class="flex flex-col justify-start items-start mt-3 space-y-2">
                <label for="address" class="text-left text-sm text-gray-800">Email</label>
                <input type="text" v-model="email" class="mt-1 border border-gray-300 rounded pl-3 p-2 w-full h-9 font-medium text-sm bg-gray-50" required>
            </div>
            <div class="flex flex-col justify-start items-start mt-3 space-y-2">
              <label for="country" class="text-left text-sm text-gray-800">Address</label>
              <input type="text" v-model="address" class="mt-1 border border-gray-300 rounded pl-3 p-2 w-full h-9 font-medium text-sm bg-gray-50" required>
          </div>
            <div class="flex flex-col justify-start items-start mt-3 space-y-2">
                <label for="contactNumber" class="text-left text-sm text-gray-800">Contact Number</label>
                <input type="text" v-model="contactNumber" id="contactNumber" class="mt-1 border border-gray-300 rounded pl-3 p-2 w-full h-9 font-medium text-sm bg-gray-50" required>
            </div>
            <div class="flex flex-col justify-start items-start mt-3 space-y-2">
                <label for="password" class="text-left text-sm text-gray-800">Password</label>
                <input type="password" v-model="registerPassword" id="password" class="mt-1 border border-gray-300 rounded pl-3 p-2 w-full h-9 font-medium text-sm bg-gray-50" required>
            </div>
            <div class="flex items-center my-4 w-full">
                <div class="flex-grow border-t border-gray-300"></div>
                <span class="mx-4 text-gray-600">or</span>
                <div class="flex-grow border-t border-gray-300"></div>
            </div>
            <button class="flex justify-center items-center w-full h-12 bg-gray-100 rounded-xl hover:bg-gray-200">
                <img src="/img/google.png" class="h-6 mr-4">Sign up with Google
            </button>
            <div class="flex items-center mt-3">
                <div class="flex items-center">
                    <input type="checkbox" class="mr-2 bg-white border-2 rounded-sm border-gray-500 peer peer-checked:border-0 peer-checked:bg-purple-500">
                    <label class="text-sm font-medium text-gray-700">I accept the</label>
                </div>
                <button class="text-sm text-blue-900 font-semibold hover:text-blue-800 ml-1 hover:underline">Terms and Conditions</button>
            </div>
            <button type="submit" class="mt-8 w-full h-10 bg-blue-700 text-white rounded-lg shadow-md hover:bg-blue-500">Create an account</button>
        </div>
    </form>


</template>

<script>
import axios from 'axios';

axios.defaults.withCredentials = true;

export default {
  name: 'LoginRegister',
  data() {
    return {
      registerForm: false,
      identifier: '',
      password: '',
      firstName: '',
      lastName: '',
      address: '',
      contactNumber: '',
      registerPassword: '',
      errorMessage: '',
    };
  },
  props: {
    loginForm: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['close', 'update:loginForm', 'update:registerForm','loginSuccess'],
  methods: {
    closeLoginForm() {
      this.$emit('close');
      this.resetLoginForm();
    },
    showRegisterForm() {
    this.$emit('update:loginForm', false); // Emit the event to update the loginForm value in the parent
    this.registerForm = true;
  },
    closeRegisterForm()
    {
      this.registerForm = false;
      this.resetRegisterForm();
      this.$emit('close');
    },
    showLoginForm() {
      this.registerForm = false;
      this.$emit('update:loginForm', true);
    },
    async handleLogin() {
          try {
              const response = await axios.post('http://127.0.0.1:5000/login', {
                  identifier: this.identifier,  // Can be email or username
                  password: this.password,
              });

              // Store the JWT token in localStorage
              localStorage.setItem('access_token', response.data.access_token);

              // Emit an event with login success
              this.$emit('loginSuccess');
              
              // Reset the login form and close it
              this.resetLoginForm();
              this.closeLoginForm();

              // Redirect to a desired page after successful login
              this.$router.push('');  // Ensure this is the correct route
          } catch (error) {
              // Handle errors during login attempt
              if (error.response && error.response.data) {
                  this.errorMessage = error.response.data.message || 'Login failed. Please check your credentials.';
              } else {
                  this.errorMessage = 'An error occurred. Please try again later.';
              }
              console.error('Login error:', error);
          }
      },

      resetLoginForm() {
          this.identifier = '';  // Clear identifier (email/username)
          this.password = '';
          this.errorMessage = '';
      },


    async handleRegister() {
          try {
              // Check if all fields are populated before sending the request
              const fields = [
                  this.firstName, this.lastName, this.username, this.email,
                  this.contactNumber, this.registerPassword, this.address, 
                  
              ];
              
              if (fields.some(field => !field)) {
                  this.errorMessage = 'All fields are required!';
                  return;
              }

              const response = await axios.post('http://127.0.0.1:5000/register', {
                  firstName: this.firstName,
                  lastName: this.lastName,
                  username: this.username,
                  email: this.email,
                  contactNumber: this.contactNumber,
                  password: this.registerPassword,
                  address: this.address,
            
              });

              // Reset form and navigate to login after successful registration
              this.resetRegisterForm();
              this.showLoginForm();
              alert(response.data.message);
          } catch (error) {
              if (error.response && error.response.data) {
                  this.errorMessage = error.response.data.message || 'Registration failed.';
              } else {
                  this.errorMessage = 'An error occurred. Please try again later.';
              }
          }
      },

    resetRegisterForm() {
      this.firstName = '';
      this.lastName = '';
      this.username = '',
      this.email = '';
      this.address = '';
      this.contactNumber = '';
      this.registerPassword = '';
      this.errorMessage = '';
    },
  },
};
</script>

<style scoped>
/* Add your styles here if needed */
</style>
