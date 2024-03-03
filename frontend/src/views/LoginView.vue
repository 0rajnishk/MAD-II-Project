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
            alert(token)
          localStorage.setItem('token', token);
          localStorage.setItem('user', JSON.stringify(user));
          if (user.isAdmin === true) {
            this.$router.push('/admin');
          } else {
            this.$router.push('/');
          }

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
