<template>
  <div class="home">
    <LoginForm class="login" @login="handleLogin" />
  </div>
  <!-- <AppFooter /> -->
</template>

<script>
import LoginForm from '@/components/LoginForm.vue';
// import AppFooter from '../components/AppFooter.vue';
import axios from 'axios';


export default {
  name: 'HomeView',
  components: {
    LoginForm,

  },
  data() {
    return {
      showSuccessModal: false,
      token: null,
    };
  },
  methods: {
    handleLogin(formData) {
      axios.post("http://127.0.0.1:8000/api/login", formData)
        .then(response => {
          // Extract the token from the response
        const resp = response.data
         if (resp.status == true){
           const token = resp.access_token;
          const user = resp.user;
            console.log(token)

           const roleNames = user.roles.map(role => role.role);
           if (roleNames.includes('Creator')) {
             localStorage.setItem('token', token);
             localStorage.setItem('user', JSON.stringify(user));
             localStorage.setItem('role','creator');
             this.$router.push('/');
           } else if (roleNames.includes('user')) {
             localStorage.setItem('token', token);
             localStorage.setItem('user', JSON.stringify(user));
             localStorage.setItem('role', 'user');
             this.$router.push('/');
           } else{
             alert("You are not a creator or user")}
        } else {
           console.log(response.data.error)
        }
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.login {
  margin-top: 10%;
}
</style>
