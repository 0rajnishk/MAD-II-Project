<template>
    <div class="left10">
        <h1 class="text-3xl font-bold mb-4">Stats</h1>
        <div v-if="loading" class="text-gray-500">Loading...</div>
        <div v-else>
            <div class="grid grid-cols-2 gap-4">
                <!-- Total Songs -->
                <div class="p-4 bg-white rounded-lg shadow-md">
                    <h2 class="text-xl font-bold mb-2">Total Songs</h2>
                    <p class="text-3xl font-bold">{{ stats.total_songs }}</p>
                </div>

                <!-- Total Albums -->
                <div class="p-4 bg-white rounded-lg shadow-md">
                    <h2 class="text-xl font-bold mb-2">Total Albums</h2>
                    <p class="text-3xl font-bold">{{ stats.total_albums }}</p>
                </div>

                <!-- Total Users -->
                <div class="p-4 bg-white rounded-lg shadow-md">
                    <h2 class="text-xl font-bold mb-2">Total Users</h2>
                    <p class="text-3xl font-bold">{{ stats.total_users }}</p>
                </div>

                <!-- Total Creators -->
                <div class="p-4 bg-white rounded-lg shadow-md">
                    <h2 class="text-xl font-bold mb-2">Total Creators</h2>
                    <p class="text-3xl font-bold">{{ stats.total_creators }}</p>
                </div>
            </div>
        </div>

        <div class="container mx-auto mt-8">
            <h1 class="text-3xl font-semibold mb-4 text-platinum-white">Top Songs</h1>
            <div v-if="TopSongsloading" class="text-center text-platinum-white">
                Loading...
            </div>
            <div v-else>
                <div v-if="!songs.length" class="text-platinum-white">
                    No top songs found.
                </div>
                <div v-else>
                    <div v-for="(song, index) in songs" :key="song.name" class="mb-8">
                        <h2 class="text-xl font-semibold text-platinum-white mb-2">{{ index + 1 }}. {{ song.name }}</h2>
                        <div class="flex justify-center">
                            <img :src="'data:image/png;base64,' + song.image" alt="Song Chart" class="w-64 h-auto">
                        </div>
                        <div class="flex items-center">
                            <div v-for="(count, rating) in song.rating_distribution" :key="rating" class="mr-4">
                                <span class="text-base text-platinum-white">{{ rating }}: {{ count }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            TopSongsloading: true,
            songs: [],
            loading: false,
            stats: {
                total_songs: 0,
                total_albums: 0,
                total_users: 0,
                total_creators: 0
            }
        };
    },
    mounted() {
        this.fetchStats();
        this.fetchTopSongs();
    },
    methods: {
        fetchStats() {
            this.loading = true;
            fetch('http://127.0.0.1:8000/api/stats')
                .then(response => response.json())
                .then(data => {
                    this.stats = data.stats;
                    this.loading = false;
                })
                .catch(error => {
                    console.error('Error fetching stats:', error);
                    this.loading = false;
                });
        },
        async fetchTopSongs() {
            this.TopSongsloading = true;
            try {
                const response = await fetch('http://127.0.0.1:8000/api/stats/top_songs');
                const data = await response.json();
                if (data.status) {
                    this.TopSongsloading = false;
                    this.songs = Object.entries(data.encoded_images).map(([name, image]) => ({
                        name,
                        image,
                        // average_rating: data.stats[name].average_rating,
                        // rating_distribution: data.stats[name].rating_distribution,
                    }));
                } else {
                    console.error('Error fetching top songs:', data.error);
                }
            } catch (error) {
                console.error('Error fetching top songs:', error);
            } finally {
                this.loading = false;
            }
        },
    }
};
</script>

<style scoped>
.left10 {
    margin-left: 18%;
    margin-right: 4%;
}
.text-platinum-white {
    color: #EAEAEA;
}
</style>
