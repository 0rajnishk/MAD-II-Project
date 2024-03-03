<template>
    <div class="bg-green-100 p-8 rounded-lg shadow-lg max-w-md mx-auto">
        <!-- Title -->
        <h2 class="text-3xl font-semibold text-green-800 mb-6">Adopt a Tree</h2>

        <!-- Form -->
        <form @submit.prevent="submitForm">
            <!-- Name Input -->
            <div class="mb-4">
                <label for="name" class="block text-green-800 text-sm font-medium mb-1">Your Name</label>
                <input v-model="formData.name" type="text" id="name" name="name"
                    class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-green-500"
                    placeholder="Enter your name" />
            </div>

            <!-- Tree Selection -->
            <div class="mb-4">
                <label for="tree" class="block text-green-800 text-sm font-medium mb-1">Choose a Tree</label>
                <select v-model="formData.tree" id="tree" name="tree"
                    class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-green-500">
                    <option value="oak">Oak Tree</option>
                    <option value="pine">Pine Tree</option>
                    <option value="maple">Maple Tree</option>
                    <option value="willow">Willow Tree</option>
                </select>
            </div>

            <!-- Number of Trees -->
            <div class="mb-4">
                <label for="numberOfTrees" class="block text-green-800 text-sm font-medium mb-1">Number of Trees</label>
                <select v-model="formData.numberOfTrees" id="numberOfTrees" name="numberOfTrees" @change="updateTotal"
                    class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-green-500">
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                    <option value="7">7</option>
                    <option value="8">8</option>
                    <option value="9">9</option>
                    <option value="10">10</option>
                </select>
            </div>

            <!-- Total -->
            <div>
                <p class="text-green-800 text-sm font-medium mb-1">Total (Tax incl.)</p>
                <p class="text-green-700 text-sm font-medium">&#8377;{{ total }}</p>
            </div>

            <!-- Submit Button -->
            <div class="flex justify-center">
                <button type="submit" class="bg-green-800 text-white px-6 py-3 rounded-md font-medium hover:bg-green-600">
                    Adopt Now
                </button>
            </div>
        </form>
    </div>
</template>


<script>
export default {
    data() {
        return {
            formData: {
                name: '',
                tree: '',
                numberOfTrees: 1,
            },
            total: 1500,
        };
    },
    created() {
        // Get the user details from local storage
        const user = JSON.parse(localStorage.getItem('user'));
        // Set the initial value of the name field if the user is logged in
        this.formData.name = user.name;
    },
    methods: {
        updateTotal() {
            this.total = this.formData.numberOfTrees * 1500;
        },
        submitForm() {
            const token = localStorage.getItem('token');
            console.log(this.formData)

            fetch('http://127.0.0.1:5000/adopt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(this.formData),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Adoption successful:', data);
                    alert('Adoption successful!!!');
                    // You can handle the response as needed
                })
                .catch(error => {
                    console.error('Error adopting tree:', error);
                    alert('Error adopting tree!!!');
                    // Handle errors
                });
        },
    },
};
</script>
