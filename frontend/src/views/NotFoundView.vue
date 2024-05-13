<template>
    <div class="flex flex-col items-center justify-center h-screen bg-platinum-white">
        <h1 class="text-4xl font-bold text-midnight-blue">404</h1>
        <p class="text-lg text-sunset-orange">Page Not Found</p>
        <router-link to="/"
            class="mt-8 px-4 py-2 bg-sunset-orange text-platinum-white rounded-lg hover:bg-sunset-orange-dark">Go
            Home</router-link>
    </div>
</template>

<script>
export default {
    name: 'NotFound',
}
</script>

<style scoped>
/* Add Tailwind CSS utility classes here */
</style>
