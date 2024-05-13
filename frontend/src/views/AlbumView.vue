<template>
    <main>
        <NavBar />
        <div class="flex">
            <SideBar title="Dashboard" />
            <div class="flex-1 p-4 ">
                <div class="left-m">
                    <div class="container mx-auto mt-8 ">
                        <h1 class="text-3xl font-semibold mb-4 text-platinum-white"> Albums: {{ $route.params.id }}
                        </h1>
                        <div v-if="loading" class="text-center">
                            Loading...
                        </div>
                        <div v-else>
                            <div class="grid grid-cols-4 gap-4">
                                <div v-for="song in songs" :key="song.id" class="mb-4">
                                    <div class="card">
                                        <div class="card-body">
                                            <div class="relative">
                                                <img :src="decodeBase64Image(song.image)" alt="Song Image"
                                                    class="w-full h-40 object-cover rounded-md mb-2">
                                                <button @click="playSong(song.id)"
                                                    class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-sunset-orange text-white px-4 py-2 rounded-md">
                                                    Play
                                                </button>
                                            </div>
                                            <h2 class="text-lg font-semibold text-platinum-white">{{ song.name }}</h2>
                                            <!-- Add other song details here (e.g., artist, duration, etc.) -->
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div :class="{ 'hidden': song_id === null || song_id === 0, 'visible': song_id !== null && song_id !== 0 }">
            <audioPlayer :song_id="song_id" />
        </div>
        <AppFooter />
    </main>
</template>

<script>
import AppFooter from '../components/AppFooter.vue';
import AudioPlayer from '../components/AudioPlayer.vue';

import NavBar from '../components/NavBar.vue';
import SideBar from '../components/SideBar.vue';

export default {
    components: {
        NavBar,
        AudioPlayer,
        AppFooter,
        SideBar,
    },
    data() {
        return {
            song_id: null,
            songs: [],
        };
    },
    methods: {
        async fetchPlaylists(to) {
            console.log(this.$route.params.id + to);
            const token = localStorage.getItem('token');
            try {
                const response = await fetch("http://127.0.0.1:8000/api/albums/" + this.$route.params.id, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    }
                });
                const data = await response.json();
                if (data.status) {
                    console.log("playlist fetched")
                    this.songs = data.msg;
                    this.loading = false;
                } else {
                    console.log(data.error);
                }
            } catch (error) {
                console.error('Error fetching songs:', error);
            }
        },
        decodeBase64Image(base64Image) {
            return `data:image/png;base64,${base64Image}`;
        },
        playSong(song) {
            this.song_id = song;
        },

    },
    mounted() {
        this.fetchPlaylists();
        this.song_id = 0;
    },
    watch: {
        $route(to) {
            this.fetchPlaylists(to);
        },
    },
};
</script>

<style>
main {
    background-color: #6E7E85;
    min-height: 100vh;
}

.left10 {
    margin-left: 18%;
}
</style>