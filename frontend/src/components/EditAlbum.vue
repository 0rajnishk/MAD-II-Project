<template>
    <div class="bg-midnight-blue-500 p-8 rounded-lg shadow-lg max-w-xl mx-auto" style="background-color: #00203F;">

        <h2 class="text-3xl font-semibold text-platinum-white mb-6" style="color: #EAEAEA;">Edit Album</h2>


        <form @submit.prevent="submitForm" class="grid grid-cols-1 gap-4">

            <div class="grid grid-cols-2 gap-4">
                <div class="mb-4">
                    <label for="songName" class="block text-platinum-white text-sm font-medium mb-1"
                        style="color: #EAEAEA;">Album Name</label>
                    <input v-model="albumData.name" type="text" id="songName" name="songName"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                        placeholder="Enter song name" style="border-color: #ADEFD1;" />
                </div>

                <div class="mb-4">
                    <label for="singer" class="block text-platinum-white text-sm font-medium mb-1"
                        style="color: #EAEAEA;">singer</label>
                    <input v-model="albumData.singer" type="text" id="singer" name="singer"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                        placeholder="Enter singer name" style="border-color: #ADEFD1;" />
                </div>
            </div>


            <div class="mb-4">
                <label for="genre" class="block text-platinum-white text-sm font-medium mb-1"
                    style="color: #EAEAEA;">Genre</label>
                <input v-model="albumData.genre" type="text" id="genre" name="genre"
                    class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                    placeholder="Enter genre" style="border-color: #ADEFD1;" />
            </div>

            <div class="flex justify-center">
                <button type="submit" @click="updateAlbum()"
                    class="bg-sunset-orange text-platinum-white px-6 py-3 rounded-md font-medium hover:bg-sunset-orange-dark"
                    style="background-color: #F66B0E; color: #EAEAEA;">
                    Update Album
                </button>
            </div>
        </form>
    </div>
    <br>
</template>

<script>
export default {
    data() {
        return {
            albumData: {
                name: '',
                singer: '',
                genre: '',
            },
        };
    },
    props: {
        albumId: Number,
    },
    created() {
        this.fetchAlbum(this.albumId);
    },
    methods: {
        async fetchAlbum(albumId) {

            const token = localStorage.getItem('token');

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/album/${albumId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                });
                const data = await response.json();
                if (data.status) {
                    console.log(data.albums);
                    this.albumData.name = data.msg.name;
                    this.albumData.singer = data.msg.singer;
                    this.albumData.genre = data.msg.genre;
                } else {
                    console.error('Error adding album:');
                    console.log('Error adding album!!!');
                }
            } catch (error) {
                console.error('Error adding song:', error);
                console.log('Error album catch!!!');
            }
        },
        async updateAlbum() {
            const token = localStorage.getItem('token');

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/admin/albums?album_id=${this.albumId}`, {
                    method: 'PUT', 
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify(this.albumData),
                });

                const data = await response.json();

                if (data.status) {
                    // Optionally, you can fetch the updated data again if needed
                    // this.fetchAlbum();
                } else {
                    console.error('Error updating album:');
                    console.log('Error updating album!!!');
                }
            } catch (error) {
                console.error('Error updating album:', error);
                console.log('Error updating album!!!');
            }
        },

        convertToBase64(key, event) {
            return new Promise((resolve, reject) => {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.albumData[key] = e.target.result;
                        resolve();
                    };
                    reader.onerror = reject; 
                    reader.readAsDataURL(file);
                } else {
                    resolve();
                }
            });
        },

    },
};
</script>