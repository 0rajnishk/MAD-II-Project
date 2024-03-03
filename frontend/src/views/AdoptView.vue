<!-- App.vue -->

<template>
    <NavBar />
    <div class="register">
        <AdoptForm />
    </div>
</template>

<script>

import NavBar from "../components/NavBar.vue";
import AdoptForm from "../components/AdoptForm.vue";
import axios from 'axios'; // Import Axios here

export default {
    components: {
        NavBar,
        AdoptForm,

    },
    data() {
        return {
            showSuccessModal: false,
        };
    },
    methods: {
        handleRegistration(formData) {
            // Make an API call to register the user/manager using the provided formData
            axios.post("http://127.0.0.1:5000/auth/register", formData)
                .then(response => {

                    if (response.status === 201) {
                        // Registration successful
                        alert("Registration successful!");
                        this.$router.push('/login');
                    }

                })
                .catch(error => {
                    // Handle error
                    console.error(error);
                });
        },
    },
};
</script>

<style scoped>
.register {
    margin-top: 5%;
}
</style>
