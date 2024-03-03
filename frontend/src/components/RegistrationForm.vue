<!-- RegistrationForm.vue -->

<template>
    <div class="login-wrap">
        <h2>Signup</h2>
        <form @submit.prevent="submitForm" class="form">
            <!-- 
        "fname": "rajnish",
    "lname": "kumar",
    "email": "shailesh@gmail.com",
    "phone": "9876987698", 
    "password": "0rajnishK@gmail.com"
 -->
            <!-- Use v-model directly on formData properties -->
            <input type="text" placeholder="First Name" v-model="formData.fname" />
            <input type="text" placeholder="Last Name" v-model="formData.lname" />
            <input type="text" placeholder="Email" v-model="formData.email" />
            <input type="text" placeholder="Phone" v-model="formData.phone" />
            <input type="password" placeholder="Password" v-model="formData.password" />
            <button type="submit">Sign in</button>
            <router-link to="/login">
                <p>Already have an account? login</p>
            </router-link>
        </form>
    </div>
</template>


<script>
export default {
    data() {
        return {
            formData: {
                fname: "",
                lname: "",
                email: "",
                phone:"",
                password: ""
            },
        };
    },
    methods: {
        submitForm() {
            // Send registration data to the backend
            this.$emit("register", this.formData);
        },
    },
};
</script>


<style>
.login-wrap {
    position: relative;
    margin: 0 auto;
    background: #ecf0f1;
    width: 350px;
    border-radius: 5px;
    box-shadow: 3px 3px 10px #333;
    padding: 15px;
}

.login-wrap h2 {
    text-align: center;
    font-weight: 200;
    font-size: 2em;
    margin-top: 10px;
    color: #34495e;
}

.login-wrap .form {
    padding-top: 20px;
}

.login-wrap input[type="text"],
.login-wrap input[type="password"],
.login-wrap button {
    width: 80%;
    margin-left: 10%;
    margin-bottom: 25px;
    height: 40px;
    border-radius: 5px;
    outline: 0;
}

.login-wrap input[type="text"],
.login-wrap input[type="password"] {
    border: 1px solid #bbb;
    padding: 0 0 0 10px;
    font-size: 14px;
}

.login-wrap input[type="text"]:focus,
.login-wrap input[type="password"]:focus {
    border: 1px solid #3498db;
}

.login-wrap a {
    text-align: center;
    font-size: 10px;
    color: #3498db;
}

.login-wrap a p {
    padding-bottom: 10px;
}

.login-wrap button {
    background: #e74c3c;
    border: none;
    color: white;
    font-size: 18px;
    font-weight: 200;
    cursor: pointer;
    transition: box-shadow 0.4s ease;
}

.login-wrap button:hover {
    box-shadow: 1px 1px 5px #555;
}

.login-wrap button:active {
    box-shadow: 1px 1px 7px #222;
}

.login-wrap:after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background: -webkit-linear-gradient(left,
            #27ae60 0%,
            #27ae60 20%,
            #8e44ad 20%,
            #8e44ad 40%,
            #3498db 40%,
            #3498db 60%,
            #e74c3c 60%,
            #e74c3c 80%,
            #f1c40f 80%,
            #f1c40f 100%);
    background: -moz-linear-gradient(left,
            #27ae60 0%,
            #27ae60 20%,
            #8e44ad 20%,
            #8e44ad 40%,
            #3498db 40%,
            #3498db 60%,
            #e74c3c 60%,
            #e74c3c 80%,
            #f1c40f 80%,
            #f1c40f 100%);
    height: 5px;
    border-radius: 5px 5px 0 0;
}
</style>
