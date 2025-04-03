<template>
  <div class="min-h-screen bg-gray-100 pt-32 pb-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
        {{ successMessage }}
      </div>

      <!-- Loading Indicator -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>

      <div v-else class="bg-white shadow-xl rounded-lg overflow-hidden">
        <!-- Profile Header - Made taller to accommodate the profile picture -->
        <div class="relative bg-gradient-to-r from-blue-500 to-purple-600 h-48 md:h-64">
          <!-- Profile Picture - Positioned within the header -->
          <div class="absolute left-0 bottom-0 w-full flex justify-center transform translate-y-1/2">
            <div class="relative group">
              <div class="w-36 h-36 rounded-full overflow-hidden border-4 border-white bg-gray-200 shadow-lg">
                <img 
                  :src="profileImageUrl" 
                  alt="Profile Picture" 
                  class="w-full h-full object-cover"
                  @error="handleImageError"
                />
                <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer" @click="triggerFileInput">
                  <span class="text-white text-sm font-medium">{{ uploadLoading ? 'Uploading...' : 'Change Photo' }}</span>
                </div>
              </div>
              <input 
                ref="fileInput" 
                type="file" 
                accept="image/*" 
                class="hidden" 
                @change="handleImageUpload"
              />
            </div>
          </div>
        </div>
        
        <!-- Profile Content Container - Added top padding to account for the profile picture -->
        <div class="px-4 sm:px-6 lg:px-8 pb-8 pt-20">
          <!-- Profile Information -->
          <div class="text-center mb-6">
            <h1 v-if="!editMode" class="text-3xl font-bold text-gray-800">
              {{ userProfile.firstname || '' }} {{ userProfile.lastname || '' }}
            </h1>
            <p v-if="!editMode" class="text-gray-500 text-sm mt-1">@{{ userProfile.username || 'Username not set' }}</p>
            <p v-if="!editMode" class="text-gray-500 font-semibold text-sm mt-1">{{ userProfile.user_type || 'Regular User' }}</p>
          </div>

          <!-- Edit/View Toggle -->
          <div class="text-center mb-6 space-x-4">
            <button 
              @click="toggleEditMode" 
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              {{ editMode ? 'Cancel' : 'Edit Profile' }}
            </button>
            <button 
              @click="togglePasswordMode" 
              class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
            >
              {{ passwordMode ? 'Cancel' : 'Change Password' }}
            </button>
          </div>

          <!-- Change Password Form -->
          <div v-if="passwordMode" class="mt-8 mb-2">
            <form @submit.prevent="changePassword" class="space-y-6 max-w-md mx-auto">
              <div>
                <label for="currentPassword" class="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
                <input 
                  type="password" 
                  id="currentPassword" 
                  v-model="passwordForm.currentPassword" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
                <input 
                  type="password" 
                  id="newPassword" 
                  v-model="passwordForm.newPassword" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">Confirm New Password</label>
                <input 
                  type="password" 
                  id="confirmPassword" 
                  v-model="passwordForm.confirmPassword" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div class="flex justify-end space-x-3">
                <button 
                  type="button" 
                  @click="passwordMode = false" 
                  class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
                  :disabled="changingPassword"
                >
                  {{ changingPassword ? 'Changing Password...' : 'Change Password' }}
                </button>
              </div>
            </form>
          </div>

          <!-- View Mode -->
          <div v-if="!editMode" class="w-full backdrop-blur-lg">
            <div class="border rounded-lg p-4">
              <h2 class="text-lg font-semibold mb-4 text-gray-700">Contact Information</h2>
              <div class="space-y-3">
                <div class="flex items-start">
                  <span class="text-gray-500 w-24">Email:</span>
                  <span class="text-gray-800 flex-1">{{ userProfile.email || 'Not provided' }}</span>
                </div>
                <div class="flex items-start">
                  <span class="text-gray-500 w-24">Phone:</span>
                  <span class="text-gray-800 flex-1">{{ userProfile.contactnumber || 'Not provided' }}</span>
                </div>
                <div class="flex items-start">
                  <span class="text-gray-500 w-24">Address:</span>
                  <span class="text-gray-800 flex-1">{{ userProfile.address || 'Not provided' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Edit Mode -->
          <div v-else class="mt-8">
            <form @submit.prevent="saveProfile" class="space-y-6">
              <!-- Personal Information -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="firstname" class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                  <input 
                    type="text" 
                    id="firstname" 
                    v-model="editedProfile.firstname" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label for="lastname" class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                  <input 
                    type="text" 
                    id="lastname" 
                    v-model="editedProfile.lastname" 
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <!-- Username -->
              <div>
                <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                <input 
                  type="text" 
                  id="username" 
                  v-model="editedProfile.username" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <!-- Contact Information -->
              <div>
                <label for="contactnumber" class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                <input 
                  type="text" 
                  id="contactnumber" 
                  v-model="editedProfile.contactnumber" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label for="address" class="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <textarea 
                  id="address" 
                  v-model="editedProfile.address" 
                  rows="3" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>

              <!-- Submit Buttons -->
              <div class="flex justify-end space-x-3">
                <button 
                  type="button" 
                  @click="editMode = false" 
                  class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  :disabled="saving"
                >
                  {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserProfile',
  data() {
    return {
      userProfile: {},
      editedProfile: {},
      loading: true,
      uploadLoading: false,
      error: null,
      successMessage: null,
      editMode: false,
      passwordMode: false,
      saving: false,
      changingPassword: false,
      previewImage: null,
      allowedFileTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      maxFileSize: 5 * 1024 * 1024, // 5MB
      apiBaseUrl: 'http://127.0.0.1:5000',
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    };
  },
  computed: {
    profileImageUrl() {
      // If there's a preview image being shown, use that
      if (this.previewImage) {
        return this.previewImage;
      }
      
      // If the user has a profile image set
      if (this.userProfile && this.userProfile.user_img) {
        // Check if it's a full URL or just a path
        if (this.userProfile.user_img.startsWith('http')) {
          return this.userProfile.user_img;
        } else {
          // Add the API base URL to the relative path
          return `${this.apiBaseUrl}${this.userProfile.user_img}`;
        }
      }
      
      // Default fallback
      return '/default-profile.jpg';
    }
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      this.loading = true;
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`${this.apiBaseUrl}/api/user/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.data.status === 'success') {
          this.userProfile = response.data.data;
          console.log('Profile data loaded:', this.userProfile);
          
          // Log the image URL for debugging
          if (this.userProfile.user_img) {
            console.log('Profile image URL:', `${this.apiBaseUrl}${this.userProfile.user_img}`);
          }
          
          // Create a deep copy for editing
          this.editedProfile = JSON.parse(JSON.stringify(this.userProfile));
          this.error = null;
        } else {
          this.error = response.data.message || 'Failed to load profile';
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
        this.error = error.response?.data?.message || 'An error occurred while loading profile';
      } finally {
        this.loading = false;
      }
    },
    
    handleImageError(e) {
      console.error('Image failed to load:', e.target.src);
      e.target.src = '/default-profile.jpg';
    },
    
    triggerFileInput() {
      if (!this.uploadLoading) {
        this.$refs.fileInput.click();
      }
    },
    
    // Preview the image before uploading
    previewSelectedImage(file) {
      if (!file) return;
      
      // Create temporary URL for preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewImage = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    // Validate the image file
    validateFile(file) {
      if (!file) return { valid: false, message: 'No file selected' };
      
      if (!this.allowedFileTypes.includes(file.type)) {
        return { 
          valid: false, 
          message: 'Invalid file type. Please select a JPEG, PNG, GIF, or WEBP image.' 
        };
      }
      
      if (file.size > this.maxFileSize) {
        return { 
          valid: false, 
          message: `File size is too large. Maximum allowed size is ${this.maxFileSize / (1024 * 1024)}MB.` 
        };
      }
      
      return { valid: true };
    },
    
    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      // Validate the file
      const validation = this.validateFile(file);
      if (!validation.valid) {
        this.error = validation.message;
        return;
      }
      
      // Show image preview
      this.previewSelectedImage(file);
      
      // Start upload
      this.uploadLoading = true;
      this.error = null;
      
      try {
        const formData = new FormData();
        formData.append('profile_image', file);
        
        const token = localStorage.getItem('access_token');
        const response = await axios.post(`${this.apiBaseUrl}/api/user/update-profile-picture`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        });
        
        if (response.data.status === 'success') {
          console.log('Profile picture updated successfully:', response.data);
          
          // Update local state with new image URL
          this.userProfile.user_img = response.data.data.image_url;
          this.successMessage = 'Profile picture updated successfully';
          
          // Clear the preview as we're now using the actual image
          setTimeout(() => {
            this.previewImage = null;
          }, 500);
          
          setTimeout(() => {
            this.successMessage = null;
          }, 3000);
        } else {
          this.error = response.data.message || 'Failed to update profile picture';
          // Clear the preview on error
          this.previewImage = null;
        }
      } catch (error) {
        console.error('Error uploading image:', error);
        this.error = error.response?.data?.message || 'An error occurred while uploading the image';
        // Clear the preview on error
        this.previewImage = null;
      } finally {
        this.uploadLoading = false;
        // Reset the file input to allow selecting the same file again
        this.$refs.fileInput.value = '';
      }
    },
    
    toggleEditMode() {
      if (this.editMode) {
        // Reset edited profile to current profile
        this.editedProfile = JSON.parse(JSON.stringify(this.userProfile));
      }
      this.editMode = !this.editMode;
    },
    
    togglePasswordMode() {
      this.passwordMode = !this.passwordMode;
      if (!this.passwordMode) {
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        };
      }
    },
    
    async saveProfile() {
      this.saving = true;
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.put(`${this.apiBaseUrl}/api/user/update-profile`, {
          firstname: this.editedProfile.firstname,
          lastname: this.editedProfile.lastname,
          username: this.editedProfile.username,
          contactnumber: this.editedProfile.contactnumber,
          address: this.editedProfile.address
        }, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.data.status === 'success') {
          // Update the main profile object
          this.userProfile = { ...this.userProfile, ...this.editedProfile };
          this.editMode = false;
          this.successMessage = 'Profile updated successfully';
          
          // Trigger a profile update event for the navigation component
          document.dispatchEvent(new CustomEvent('user-profile-updated'));
          
          setTimeout(() => {
            this.successMessage = null;
          }, 3000);
        } else {
          this.error = response.data.message || 'Failed to update profile';
        }
      } catch (error) {
        console.error('Error updating profile:', error);
        this.error = error.response?.data?.message || 'An error occurred while updating profile';
      } finally {
        this.saving = false;
      }
    },

    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        this.error = 'New passwords do not match';
        return;
      }

      this.changingPassword = true;
      this.error = null;
      this.successMessage = null;

      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post(
          `${this.apiBaseUrl}/api/user/change-password`,
          {
            current_password: this.passwordForm.currentPassword,
            new_password: this.passwordForm.newPassword
          },
          {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        );

        if (response.data.status === 'success') {
          this.successMessage = 'Password changed successfully';
          this.passwordMode = false;
          this.passwordForm = {
            currentPassword: '',
            newPassword: '',
            confirmPassword: ''
          };
        } else {
          this.error = response.data.message || 'Failed to change password';
        }
      } catch (error) {
        console.error('Error changing password:', error);
        this.error = error.response?.data?.message || 'An error occurred while changing password';
      } finally {
        this.changingPassword = false;
      }
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap');

.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}
</style> 