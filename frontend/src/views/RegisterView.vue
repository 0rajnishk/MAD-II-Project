<!-- App.vue -->

<template>
  <div class="register">
    <RegistrationForm @register="handleRegistration" />
  </div>
</template>

<script>
import RegistrationForm from "@/components/RegistrationForm.vue";
import axios from 'axios'; 

export default {
  components: {
    RegistrationForm,
  },
  data() {
    return {
      showSuccessModal: false,
    };
  },
  methods: {
    handleRegistration(formData) {
      axios.post("http://127.0.0.1:8000/api/users", formData)
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
