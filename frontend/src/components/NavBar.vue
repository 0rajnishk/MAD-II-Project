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

            <router-link to="/">
                <li class="mx-4 my-4 md:my-0" cursor-pointer>Home</li>
            </router-link>

            <div v-if="!showDashboard">

                <li @click="becomeCreator()" class="mx-4 my-4 md:my-0 cursor-pointer">Become creator</li>

            </div>
            <div v-if="showDashboard">
                <router-link to="/dashboard">
                    <li class="mx-4 my-4 md:my-0 cursor-pointer">Dashboard</li>
                </router-link>
            </div>





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
            role: null,
            showDashboard: false,
        };
    },
    computed: {
        isLoggedIn() {
            const user = localStorage.getItem('user');
            return user !== null;
        },

    },
    methods: {
        toggleMobileMenu() {
            this.isMobileMenuOpen = !this.isMobileMenuOpen;
            // this.toggleDropdown();
        },
        checkRole() {
            const role = localStorage.getItem('role');
            if (role === 'creator'){
                this.showDashboard = true;
            };
            if (role === 'admin'){
                this.$router.push('/admin')
            }
        },
        toggleDropdown() {
            console.log('Dropdown');
            this.isDropdownOpen = !this.isDropdownOpen;
        },
        logout() {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            if (localStorage.getItem('role') === 'creator') {
                localStorage.removeItem('role');
                this.$router.push('/login');
            } else if (localStorage.getItem('admin') === 'admin'){
                localStorage.removeItem('role')
                this.$router.push('/adminlogin')
            } else {
                localStorage.removeItem('role')
                this.$router.push('/')
            }
            
        },
        async becomeCreator() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('http://127.0.0.1:8000/api/update_role', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    }
                });
                if (response.status) {
                    this.showDashboard = true;
                    localStorage.setItem('role', 'creator');
                    alert(response.msg)
                }
            } catch (error) {
                console.error('Error fetching rating:', error);
            }
        },
    },
    mounted() {
        if (!this.isLoggedIn) {
            this.$router.push('/login');
        }
        this.checkRole();
    },

};
</script>