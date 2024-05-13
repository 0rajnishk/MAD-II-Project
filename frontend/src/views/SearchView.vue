<template>
    <main>
        <NavBar />
        <div class="flex">
            <SideBar title="Dashboard" @play-song="songID" />
            <div class="flex-1 p-4 ">
                <div class="left-m">
                    <div class="container mx-auto mt-8 ">
                        <h1 class="text-3xl font-semibold mb-4 text-platinum-white">All Songs</h1>
                        <div v-if="loadingSong" class="text-center">
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
                    <!-- ================================================================================================== -->
                    <div class=" container mx-auto mt-8">
                        <h1 class="text-3xl font-semibold mb-4 text-platinum-white">All Albums</h1>
                        <div v-if="loadingAlbum" class="text-center text-platinum-white">
                            Loading...
                        </div>
                        <div v-else>
                            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                                <div v-for="album in albums" :key="album.id" class="mb-4">
                                    <div
                                        class="relative rounded-lg overflow-hidden shadow-lg bg-sunset-orange text-white">
                                        <div class="p-4">
                                            <button @click="openAlbum(album.id)"
                                                class="bg-sunset-orange text-white px-4 py-2 rounded-md">
                                                Open
                                            </button>
                                            <h2 class="text-lg font-semibold">Name: {{ album.name }}</h2>
                                            <p class="text-base">Singer: {{ album.singer }}</p>
                                            <p class="text-base">Genre: {{ album.genre }}</p>
                                            <!-- <p class="text-base">{{ album.id }}</p> -->
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
            albums: [],
            loadingSong: true,
            loadingAlbum: true,
        };
    },
    methods: {
        async fetchalbums() {
            const token = localStorage.getItem('token');
            if (this.$route.params.query.includes('*')) {
            var query = this.$route.params.query.split('*')[0];
            var rating = this.$route.params.query.split('*')[1];

            } else {
                var query = this.$route.params.query;
                var rating = 0;
            }
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/search_albums?query=${query}&rating=${rating}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                })
                const data = await response.json();
                if (data.status) {
                    console.log(data.msg)
                    this.albums = data.msg;
                    this.loadingAlbum = false;
                } else {
                    console.log(data.error);
                }
            } catch (error) {
                console.error('Error fetching songs:', error);
            }
        },
        playSong(song) {
            this.song_id = song;
        },
        decodeBase64Image(base64Image) {
            return `data:image/png;base64,${base64Image}`;
        },
        async fetchSongs() {
            const token = localStorage.getItem('token');
            if (this.$route.params.query.includes('*')) {
            var query = this.$route.params.query.split('*')[0];
            var rating = this.$route.params.query.split('*')[1];

            } else {
                var query = this.$route.params.query;
                var rating = 0;
            }

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/search_songs?query=${query}&rating=${rating}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                })
                const data = await response.json();
                if (data.status) {
                    this.songs = data.msg;
                    console.log(data.msg)
                    this.loadingSong = false;
                } else {
                    console.log(data.error);
                }
            } catch (error) {
                console.error('Error fetching songs:', error);
            }
        },

        query(query) {
            this.search_query = query;
        },
        openAlbum(id) {
            this.$router.push({ name: 'AlbumView', params: { id: id } });
        },
        songID(song) {
            this.song_id = song;
        },
    },
    mounted() {
        this.fetchSongs();
        this.fetchalbums();
        this.song_id = 0;
    },
    watch: {
        '$route.params.query'(newVal, oldVal) {
            console.log(newVal, oldVal)
            this.songs = []
            this.albums =[]
            this.fetchalbums();
            this.fetchSongs();
        }
    },
};
</script>

<style scoped>
.left-m {
    margin-left: 20%;
}

.text-platinum-white {
    color: #110202;
}

.bg-sunset-orange {
    background-color: #F66B0E;
}

/* Add styles for the album card */
.rounded-lg {
    border-radius: 1rem;
}

.shadow-lg {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.object-cover {
    object-fit: cover;
}

/* Adjust the button styling */
.bg-sunset-orange:hover {
    background-color: #e2580e;
}

/* Improve the text readability */
.container h1,
.container p {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}
</style>