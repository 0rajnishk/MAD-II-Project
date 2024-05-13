<template>
  <div class="left-m">
    <div class="container mx-auto mt-8 ">
      <h1 class="text-3xl font-semibold mb-4 text-platinum-white">All Songs</h1>
      <div v-if="loading" class="text-center">
        Loading...
      </div>
      <div v-else>
        <div class="grid grid-cols-4 gap-4">
          <div v-for="song in songs" :key="song.id" class="mb-4">
            <div class="card relative">
              <img :src="decodeBase64Image(song.image)" alt="Song Image" class="w-full h-40 object-cover rounded-md mb-2">
              <button @click="playSong(song.id)" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-sunset-orange text-white px-4 py-2 rounded-md">
                Play
              </button>
              <button @click="removeSong(song.id)" class="absolute top-0 right-0 bg-red-500 text-white px-2 py-1 rounded-bl-md hover:bg-red-600">
                Remove Song
              </button>
              <div class="card-body">
                <h2 class="text-lg font-semibold text-platinum-white">{{ song.name }}</h2>
                <!-- Add other song details here (e.g., artist, duration, etc.) -->
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
      songs: [],
      loading: true,
    };
  },
  mounted() {
    this.fetchSongs();
  },
  methods: {
    async fetchSongs() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://127.0.0.1:8000/api/songs', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        })
        const data = await response.json();
        if (data.status) {
          this.songs = data.songs;
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
    async removeSong(id) {
      alert("deleting song")
      const token = localStorage.getItem('token');
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/songs?song_id=${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                });
                const data = await response.json();
                if (data.status) {
                    this.showEventPopup('success', 'success', 'Song deleted successfully');
                    this.fetchallsongs()
                } else {
                    console.log(data.error);
                }
            } catch (error) {
                console.error('Error deleting song:', error);
            }
    },
  },
  props: ['showEventPopup']
};
</script>

<style scoped>
.left-m {
  margin-left: 20%;
}
.bg-sunset-orange {
  background-color: #F66B0E;
}
.text-platinum-white {
  color: #110202;
}
.card {
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  overflow: hidden;
  transition: transform 0.2s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.card:hover {
  transform: scale(1.05);
}
.card-body {
  padding: 1.5rem;
}
</style>
