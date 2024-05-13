<!-- SideBar.vue -->

<template>
    <aside class="fixed w-1/6 bg-gray-800 p-4 mt-1.5 h-full flex flex-col ">
        <div>
            <h2 class="text-xl font-bold text-white mb-4">Admin Dashboard</h2>

            <!-- Search Bar -->
            <div class="mb-4 relative">
                <input type="text" placeholder="Search..." v-model="query"
                    class="w-full py-2 px-4 bg-gray-800 border border-gray-600 rounded-md focus:outline-none focus:border-blue-400 text-white placeholder-gray-500" />
                <router-link v-if="query" :to="{ name: 'adminsearch', params: { query: query } }">
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
                <router-link to="#stats"
                    class="text-white block mb-2 hover:text-blue-400 font-bold transition duration-300">Stats</router-link>
                <router-link to="#users"
                    class="text-white block mb-2 hover:text-blue-400 font-bold transition duration-300">Users</router-link>
                <router-link to="#songs"
                    class="text-white block mb-2 hover:text-blue-400 font-bold transition duration-300">Songs</router-link>
                <router-link to="#albums"
                    class="text-white block mb-2 hover:text-blue-400 font-bold transition duration-300">Albums</router-link>
            </nav>

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
                if (response.status){
                const data = await response.json();
                this.songs = data.msg;
                console.log(this.songs.length)
                    this.showEventPopup('success', 'success!', 'fetched recently played songs.');
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
            this.$emit('search', this.query);
        },
        typesomething() {
            alert("Please type something")
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
.fixed{
    z-index: 100;
}
</style>
