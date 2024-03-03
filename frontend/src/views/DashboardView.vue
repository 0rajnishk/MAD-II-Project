<template>
    <NavBar />
    <br>
    <br>
    <br>
    <div class="dashboard-body bg-gradient-to-r from-blue-300 to-purple-300 pt-10 pb-10 flex items-center justify-center">
        <div class="overflow-x-auto w-auto md:w-3/4 text-center">
            <table class="min-w-full table-auto">
                <thead class="bg-gradient-to-b from-blue-400 to-purple-400 text-white">
                    <tr>
                        <th class="py-2 px-4">Tree Id</th>
                        <th class="py-2 px-4">Tree Name</th>
                        <th class="py-2 px-4">Growth Status</th>
                        <th class="py-2 px-4">Age</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Loop through user's trees and display details -->
                    <tr v-for="(tree, index) in userTrees" :key="index">
                        <td>
                            <span class="ml-2">{{ tree.id }}</span>
                        </td>
                        <td>{{ tree.tree_name }}</td>
                        <td>{{ tree.growth_status }}</td>
                        <td>{{ calculateAge(tree.adopted_on) }} years</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <AppFooter />
</template>

<script>

import AppFooter from '../components/AppFooter.vue';
import NavBar from '../components/NavBar.vue';

export default {
    components: {
        NavBar,
        AppFooter,
    },
    data() {
        return {
            userTrees: [],
        };
    },
    methods: {
        // Function to calculate the age of the tree based on the adoption date
        calculateAge(adoptedDate) {
            const currentDate = new Date();
            const adoptionDate = new Date(adoptedDate);
            const ageInYears = currentDate.getFullYear() - adoptionDate.getFullYear();
            return ageInYears;
        },
        fetchUserTrees() {
            const yourAuthToken = localStorage.getItem('token');
            fetch('http://127.0.0.1:5000/tree', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${yourAuthToken}`,
                },
            })
                .then(response => response.json())
                .then(data => {
                    this.userTrees = data;
                })
                .catch(error => {
                    console.error('Error fetching user trees:', error);
                });
        },
    },
    created() {
        this.fetchUserTrees();
    },
};
</script>




