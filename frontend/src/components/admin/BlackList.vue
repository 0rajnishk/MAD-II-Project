<template>
    <div class="left-m">
        <h1 class="text-3xl font-bold mb-4">Blacklisted Users</h1>
        <div v-if="loading" class="text-gray-500">Loading...</div>
        <div v-else>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <div v-for="user in blacklistedUsers" :key="user.id" class="bg-white shadow-md rounded-lg p-6 mb-4">
                    <div class="mb-2">
                        <p class="text-lg font-semibold">{{ user.fname }} {{ user.lname }}</p>
                        <p class="text-gray-600">{{ user.email }}</p>
                        <p class="text-gray-600">{{ user.phone }}</p>
                    </div>
                    <div class="flex items-center mb-2">
                        <p class="mr-2">Roles:</p>
                        <div class="flex">
                            <span v-for="(role, index) in user.roles" :key="index"
                                class="bg-gray-200 text-gray-700 px-2 py-1 rounded-lg mr-2">{{ role.role }}</span>
                        </div>
                    </div>
                    <button @click="removeFromBlacklist(user.id)"
                        class="mt-4 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600">Remove from
                        Blacklist</button>
                </div>
            </div>
            <h1 v-if="blacklistNotfound || blacklistedUsers.length < 1" class="text-xl font-semibold text-gray-600">
                Blacklist is empty or not found</h1>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            blacklistedUsers: [],
            loading: true,
            blacklistNotfound: false
        };
    },
    mounted() {
        // Fetch blacklisted users from the API
        this.fetchBlacklistedUsers();
    },
    methods: {
        async fetchBlacklistedUsers() {
            const token = localStorage.getItem('token');
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://127.0.0.1:8000/api/blacklist_users',
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    },
                });
                const data = await response.json();
                if (data.status) {
                    this.blacklistedUsers = data.blacklisted_users;
                } else {
                    console.error('Error fetching blacklisted users:', data.error);
                    this.blacklistNotfound = true;
                }
            } catch (error) {
                console.error('Error fetching blacklisted users:', error);
                this.blacklistNotfound = true;
            } finally {
                this.loading = false;
            }
        },
        async removeFromBlacklist(userId) {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/blacklist_users?user_id=${userId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: 'Bearer ' + token,
                    },
                });
                const data = await response.json();
                if (data.status) {
                    // Remove the user from the list of blacklisted users
                    this.blacklistedUsers = this.blacklistedUsers.filter(user => user.id !== userId);
                } else {
                    console.error('Error removing user from blacklist:', data.error);
                }
            } catch (error) {
                console.error('Error removing user from blacklist:', error);
            }
        }
    }
};
</script>

<style scoped>
.left-m {
    margin-left: 20%;
    margin-right: 10%;
}
</style>
