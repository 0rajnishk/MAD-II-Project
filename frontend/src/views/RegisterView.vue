<!-- App.vue -->

<template>
  <div class="register">
    <RegistrationForm @signup="handleSignup" />
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
    async handleSignup(formData) {
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/users", formData);

        if (response.status === 201) {
          alert(JSON.stringify(response.data.msg));
          this.$router.push('/login');
        } else {
          if (response.status === 409) {
            alert("User already exists. Please choose a different email.");
          } else {
            alert("An error occurred. Please try again.");
          }
        }
      } catch (error) {
        alert('Error occurred while signing up');
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
.register {
  margin-top: 5%;
}
</style>
