<template>
    <div class="left-m">
        <div class=" container mx-auto mt-8">
            <h1 class="text-3xl font-semibold mb-4 text-platinum-white">All Albums</h1>
            <div v-if="loading" class="text-center text-platinum-white">
                Loading...
            </div>
            <div v-else>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    <div v-for="album in albums" :key="album.id" class="mb-4">
                        <div class="relative rounded-lg overflow-hidden shadow-lg bg-sunset-orange text-white" @click="openAlbum(album.id)">
                            <div class="p-4">
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
</template>

<script>
export default {
    data() {
        return {
            albums: [],
            loading: true,
        };
    },
    mounted() {
        this.fetchalbums();
    },
    methods: {
        async fetchalbums() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('http://127.0.0.1:8000/api/albums', {
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
                    this.loading = false;
                } else {
                    console.log(data.error);
                }
            } catch (error) {
                console.error('Error fetching songs:', error);
            }
        },
        playSong(song) {
            this.$emit('play-song', song);
        },
        decodeBase64Image(base64Image) {
            return `data:image/png;base64,${base64Image}`;
        },
        openAlbum(albumId) {
            this.$router.push({ name: 'album', params: { id: albumId } });
        },

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