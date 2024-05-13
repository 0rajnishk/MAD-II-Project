<!-- SideBar.vue -->

<template>
    <aside class="fixed w-1/6 bg-gray-800 p-4 mt-1.5 h-full flex flex-col ">
        <div>
            <h2 class="text-xl font-bold text-white mb-4">Dashboard</h2>

            <!-- Search Bar -->
            <div class="mb-4 relative">
                <input type="text" placeholder="Search..." v-model="query"
                    class="w-full py-2 px-4 bg-gray-800 border border-gray-600 rounded-md focus:outline-none focus:border-blue-400 text-white placeholder-gray-500" />
                <router-link v-if="query" :to="{ name: 'search', params: { query: query } }">
                    <button class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 focus:outline-none"
                        @click="search()">
                        🔍
                    </button>
                </router-link>
                <button v-if="!query"
                    class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 focus:outline-none">
                    <button class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 focus:outline-none"
                        @click="typesomething()">
                        🔍
                    </button>
                </button>

                <div v-if="query">
                    <select v-model="selectedRating" @change="search()">
                        <option value="">Select Rating</option>
                        <option value="1">Rating 1</option>
                        <option value="2">Rating 2</option>
                        <option value="3">Rating 3</option>
                        <option value="4">Rating 4</option>
                        <option value="5">Rating 5</option>
                    </select>
                </div>

            </div>

            <div v-if="filteredSuggestions.length > 0"
                class="absolute w-full bg-gray-800 border border-gray-600 rounded-md overflow-hidden shadow-md">
                <ul class="py-2">
                    <li v-for="(suggestion, index) in filteredSuggestions" :key="index"
                        class="cursor-pointer hover:bg-gray-700 transition duration-300 px-4 py-2 text-white"
                        @click="selectSuggestion(suggestion)">
                        {{ suggestion }}
                    </li>
                </ul>
            </div>
            <!-- Navigation Links -->
            <nav class="mb-8">
            </nav>

        </div>


        <div class="mb-8">
            <h3 class="text-lg font-bold text-white mb-4">Playlists</h3>
            <ul class="text-white pl-4" v-for="playlist in playlists" :key="playlist.id">

                <router-link :to="{ name: 'playlist', params: { id: playlist.id } }">
                    <li class="mb-2 flex items-center hover:text-blue-400 cursor-pointer transition duration-300">
                        <svg class="w-4 h-4 mr-2 fill-current text-blue-400" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24">
                            <path
                                d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm0 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8z" />
                        </svg>
                        {{ playlist.name }}
                    </li>
                </router-link>
            </ul>
        </div>


        <div class="mb-8">
            <h3 class="text-lg font-bold text-white mb-4">Recently Played</h3>
            <ul class="text-white pl-4" v-for="song in songs" :key="song.id">
                <li class="mb-2 flex items-center cursor-pointer hover:text-blue-400 transition duration-300"
                    @click="playSong(song.song_id)">
                    <svg class="w-4 h-4 mr-2 fill-current text-blue-400" xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24">
                        <!-- Add your custom icon here (e.g., music note, clock, etc.) -->
                        <!-- Example: Music Note Icon -->
                        <path
                            d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm0 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8z" />
                    </svg>
                    {{ song.song_name }}
                </li>
                <!-- Add more songs as needed -->
            </ul>
        </div>

        <!-- choose language -->
        <div class="mt-0 -z-50">
            <h3 class="text-lg font-bold text-white mb-4">Choose Language</h3>
            <select
                class="w-full py-2 px-3 bg-gray-700 border border-gray-600 rounded focus:outline-none focus:border-blue-400 text-white">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="it">Italian</option>
                <option value="pt">Portuguese</option>
                <option value="ru">Russian</option>
                <option value="zh">Chinese</option>
                <option value="ja">Japanese</option>
                <option value="ko">Korean</option>
            </select>
        </div>
        <button @click="showEventPopup('success', 'Success!', 'Sidebar action succeeded.')">
            Trigger Success Popup in Sidebar
        </button>
    </aside>
</template>

<script>
export default {
    data() {
        return {
            searchQuery: "",
            selectedRating: "0",
            suggestionList: ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
            playlists: [],
            songs: [],
            query: null,
            songNotFound: false,
            albumNotFound: false,
        };
    },
    methods: {


        selectSuggestion(selectedSuggestion) {
            console.log("Selected Suggestion:", selectedSuggestion);
            this.searchQuery = "";
        },

        async fetchPlaylists() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('http://127.0.0.1:8000//api/playlists',
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token,
                        },
                    }
                );
                const data = await response.json();
                this.playlists = data.msg;
            } catch (error) {
                console.error('Error fetching playlists:', error);
            }
        },

        async fetchRecentlyPlayedSongs() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('http://127.0.0.1:8000/api/recently_played_songs',
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token,
                        },
                    }
                );
                if (response.status) {
                    const data = await response.json();
                    this.songs = data.msg;
                    console.log(this.songs.length)
                } else {
                    this.songNotFound = true;
                    this.showEventPopup('failure', 'Failed!', 'failed to fetch recently played songs.');
                }
            } catch (error) {
                console.error('Error fetching playlists:', error);
            }
        },
        playSong(song) {
            console.log(song)
            this.$emit('play-song', song);
        },
        search() {
            if (this.query.includes('*')) {
                this.query = this.query.split('*')[0]+ '*' + String(this.selectedRating);
            } else {
                this.query = this.query.trim()+ '*' + String(this.selectedRating);
            }
            this.$emit('search',  this.query);
        },
        typesomething() {
            alert("Please type something")
        },
        formatQuery() {
            if (this.query.includes('*')) {
                return this.query.split('*')[0]
            } else {
               return this.query.trim()
            }
        }
    },

    computed: {
        filteredSuggestions() {
            // Filter suggestions based on the search query
            return this.suggestionList.filter(
                (suggestion) =>
                    suggestion.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
                    this.searchQuery.length >= 3
            );
        },
    },
    mounted() {
        this.fetchPlaylists();
        this.fetchRecentlyPlayedSongs();
    },
    props: ['showEventPopup']
};
</script>

<style>
.left-m {
    margin-left: 15%;
}


::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-thumb {
    background-color: #4a5568;
}

::-webkit-scrollbar-track {
    background-color: #2d3748;
}

.fixed {
    z-index: 100;
}
</style>
