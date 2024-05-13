<template>
    <main>
        <NavBar />
        <div class="flex">
            <SideBar title="Dashboard" @play-song="songID" />
            <div class="flex-1 p-4 ">
                <div class="left-m">
                    <div class="container mx-auto mt-8">
                        <h1 class="text-3xl font-semibold mb-4 text-platinum-white">All Songs</h1>
                        <div v-if="loadingSong" class="text-center">
                            Loading...
                        </div>
                        <div v-else>
                            <div class="grid grid-cols-4 gap-4">
                                <div v-for="song in songs" :key="song.id" class="mb-4">
                                    <div class="relative rounded-lg overflow-hidden shadow-lg bg-white">
                                        <img :src="decodeBase64Image(song.image)" alt="Song Image"
                                            class="w-full h-40 object-cover rounded-t-lg">
                                        <div class="p-4">
                                            <h2 class="text-lg font-semibold text-gray-800">{{ song.name }}</h2>
                                            <!-- Add other song details here (e.g., artist, duration, etc.) -->
                                            <div class="flex justify-end mt-2">
                                                <button @click="playSong(song.id)"
                                                    class="bg-sunset-orange text-white px-4 py-2 rounded-md mr-2">
                                                    Play
                                                </button>
                                                <button @click="removeSong(song.id)"
                                                    class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">
                                                    Remove
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>


                    <!-- ================================================================================================== -->
                    <div class="container mx-auto mt-8">
                        <h1 class="text-3xl font-semibold mb-4 text-platinum-white">All Albums</h1>
                        <div v-if="loadingAlbum" class="text-center text-platinum-white">
                            Loading...
                        </div>
                        <div v-else>
                            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                                <div v-for="album in albums" :key="album.id" class="mb-4">
                                    <div class="relative rounded-lg overflow-hidden shadow-lg bg-white">
                                        <div class="p-4">
                                            <button @click="openAlbum(album.id)"
                                                class="bg-sunset-orange text-white px-4 py-2 rounded-md mr-2">
                                                Open
                                            </button>
                                            <button @click="removeAlbum(album.id)"
                                                class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">
                                                Remove
                                            </button>
                                            <h2 class="text-lg font-semibold text-gray-800">Name: {{ album.name }}</h2>
                                            <p class="text-base">Singer: {{ album.singer }}</p>
                                            <p class="text-base">Genre: {{ album.genre }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>


                    <!-- Search for users -->
                    <h1 class="text-3xl font-semibold mb-4 text-platinum-white">Users</h1>
                    <div class="container mx-auto mt-8">
                        <div v-if="loadingUsers" class="text-center text-platinum-white">
                            Loading...
                        </div>
                        <div v-else>
                            <div v-if="!users.length && !loadingUsers" class="text-platinum-white">
                                No users found.
                            </div>
                            <div v-else>
                                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                                    <div v-for="user in users" :key="user.id" class="mb-4">
                                        <div class="card bg-white shadow-md rounded-lg p-4">
                                            <div class="flex justify-between items-center mb-2">
                                                <h2 class="text-lg font-semibold text-platinum-white">{{ user.fname }}
                                                    {{ user.lname }}</h2>
                                                <button @click="blacklistUser(user.id)"
                                                    class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">
                                                    Blacklist
                                                </button>
                                            </div>
                                            <p class="text-base">Email: {{ user.email }}</p>
                                            <p class="text-base">Phone: {{ user.phone }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Search for creators -->
                    <div class="container mx-auto mt-8">
                        <h1 class="text-3xl font-semibold mb-4 text-platinum-white">Creators</h1>
                        <div v-if="loadingCreators" class="text-center text-platinum-white">
                            Loading...
                        </div>
                        <div v-else>
                            <div v-if="!creators.length && !loadingCreators" class="text-platinum-white">
                                No creators found.
                            </div>
                            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                                <div v-for="creator in creators" :key="creator.id" class="mb-4">
                                    <div class="card bg-white shadow-md rounded-lg p-4">
                                        <div class="flex justify-between items-center mb-2">
                                            <h2 class="text-lg font-semibold text-platinum-white">{{ creator.fname }} {{
                                                creator.lname }}</h2>
                                            <button @click="blacklistCreator(creator.id)"
                                                class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">
                                                Blacklist
                                            </button>
                                        </div>
                                        <p class="text-base">Email: {{ creator.email }}</p>
                                        <p class="text-base">Phone: {{ creator.phone }}</p>
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

import NavBar from '../components/admin/NavBar.vue';
import SideBar from '../components/admin/SideBar.vue';

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
            userSearchQuery: '',
            creatorSearchQuery: '',
            users: [],
            creators: [],
            loadingUsers: false,
            loadingCreators: false,
        };
    },
    methods: {
        async fetchalbums() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/search_albums?query=` + this.$route.params.query, {
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

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/search_songs?query=` + this.$route.params.query, {
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
        // Method to search for users
        async searchUsers() {
            this.loadingUsers = true;
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/search_users?query=${this.$route.params.query}`);
                const data = await response.json();
                if (data.status) {
                    this.users = data.users;
                } else {
                    console.error(data.error);
                }
            } catch (error) {
                console.error('Error searching users:', error);
            } finally {
                this.loadingUsers = false;
            }
        },
        // Method to search for creators
        async searchCreators() {
            this.loadingCreators = true;
            try {
                // Send a request to search creators based on the query
                // Update this part according to your API endpoint for searching creators
                const response = await fetch(`http://127.0.0.1:8000/api/search_creators?query=${this.$route.params.query}`);
                const data = await response.json();
                if (data.status) {
                    this.creators = data.creators;
                } else {
                    console.error(data.error);
                }
            } catch (error) {
                console.error('Error searching creators:', error);
            } finally {
                this.loadingCreators = false;
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
        blacklist(id) {
            console.log(id)
            this.$router.push({ name: 'BlacklistCreator', params: { id: id } });
        },
    },
    mounted() {
        this.fetchSongs();
        this.fetchalbums();
        this.searchUsers();
        this.searchCreators();
        this.song_id = 0;
    },
    watch: {
        '$route.params.query'(newVal, oldVal) {
            console.log(newVal, oldVal)
            this.songs = []
            this.albums =[]
            this.fetchalbums();
            this.fetchSongs();
            this.searchCreators();
            this.searchUsers();
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
