<template>
    <nav class="fixed top-0 left-0 w-full bg-transparent md:flex md:items-center md:justify-between p-2 "
        style="z-index: 1000; background-color: rgba(250, 235, 215, 0.456);">
        <div class="flex items-center justify-between">
            <a href="/"><img src="../assets/img/logo.webp" alt="" class="w-10"></a>
            <!-- MOBILE MENU BUTTON -->
            <button class="text-3xl cursor-pointer md:hidden block mx-2" @click="toggleMobileMenu">
                <svg class="ast-mobile-svg ast-menu2-svg" fill="currentColor" version="1.1"
                    xmlns="http://www.w3.org/2000/svg" width="24" height="28" viewBox="0 0 24 28">
                    <path
                        d="M24 21v2c0 0.547-0.453 1-1 1h-22c-0.547 0-1-0.453-1-1v-2c0-0.547 0.453-1 1-1h22c0.547 0 1 0.453 1 1zM24 13v2c0 0.547-0.453 1-1 1h-22c-0.547 0-1-0.453-1-1v-2c0-0.547 0.453-1 1-1h22c0.547 0 1 0.453 1 1zM24 5v2c0 0.547-0.453 1-1 1h-22c-0.547 0-1-0.453-1-1v-2c0-0.547 0.453-1 1-1h22c0.547 0 1 0.453 1 1z">
                    </path>
                </svg>
            </button>
        </div>
        <ul class="text-sm font-bold md:flex md:items-center md:pr-2 w-full md:w-auto cursor-pointer"
            :class="{ 'opacity-100': isMobileMenuOpen, 'top-[70px]': isMobileMenuOpen, 'top-[-55px]': !isMobileMenuOpen }"
            v-show="!isMobileMenuOpen">
            <!-- link -->
            <button @click="exportData">
                <li
                    class="border-box text-white p-2 bg-gradient-to-r from-blue-600 via-blue-500 to-purple-400 w-[70px] rounded-lg items-center">
                    &nbsp; Export </li>
                </button>
            <li class="mx-4 my-4 md:my-0">
            </li>
            <a v-if="!isLoggedIn" href="/login">
                <li class="mx-4 my-4 md:my-0">Log in</li>
            </a>
            <a v-if="!isLoggedIn" href="/register">
                <li
                    class="border-box text-white p-2 bg-gradient-to-r from-blue-600 via-blue-500 to-purple-400 w-[70px] rounded-lg items-center">
                    Sign up</li>
            </a>
            <a v-if="isLoggedIn" @click="logout">
                <li
                    class="border-box text-white p-2 bg-gradient-to-r from-blue-600 via-blue-500 to-purple-400 w-[60px] rounded-lg items-center">
                    logout </li>
            </a>
        </ul>
    </nav>
    <br>
    <br>
</template>

<script>
export default {
    data() {
        return {
            isMobileMenuOpen: false,
            isDropdownOpen: false,
        };
    },
    computed: {
        isLoggedIn() {
            // Check if the user details exist in local storage
            const user = localStorage.getItem('user');
            return user !== null;
        },
    },
    methods: {
        toggleMobileMenu() {
            this.isMobileMenuOpen = !this.isMobileMenuOpen;
            // this.toggleDropdown();
        },
        toggleDropdown() {
            console.log('Dropdown');
            this.isDropdownOpen = !this.isDropdownOpen;
        },
        logout() {
            // Remove the token and user from local storage
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            // Redirect to the home page
            this.$router.push('/login');
        },
        async exportData() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://127.0.0.1:8000/api/export', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (data.status) {
          this.showEventPopup('success', 'success', 'Data exported successfully');
          alert('exporting data')
        } else {
          console.log(data.error);
        }
        } catch (error) {
            console.error('Error exporting data:', error);
            }
    },

    },
};
</script>