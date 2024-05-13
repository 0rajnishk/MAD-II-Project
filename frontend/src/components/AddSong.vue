<template>
    <br>
    <br>
    <br>
    <div class="bg-midnight-blue-500 p-8 rounded-lg shadow-lg max-w-xl mx-auto" style="background-color: #00203F;">        
        <h2 class="text-3xl font-semibold text-platinum-white mb-6" style="color: #EAEAEA;">Add New Song</h2>        
        <form @submit.prevent="submitForm" class="grid grid-cols-1 gap-4">

            <div class="grid grid-cols-2 gap-4">
                <div class="mb-4">
                    <label for="songName" class="block text-platinum-white text-sm font-medium mb-1"
                        style="color: #EAEAEA;">Song Name</label>
                    <input v-model="formData.name" type="text" id="songName" name="songName"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                        placeholder="Enter song name" style="border-color: #ADEFD1;" />
                </div>

                <div class="mb-4">
                    <label for="singer" class="block text-platinum-white text-sm font-medium mb-1"
                        style="color: #EAEAEA;">Singer</label>
                    <input v-model="formData.singer" type="text" id="singer" name="singer"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                        placeholder="Enter singer name" style="border-color: #ADEFD1;" />
                </div>
            </div>

            <div class="mb-4">
                <label for="genre" class="block text-platinum-white text-sm font-medium mb-1"
                    style="color: #EAEAEA;">Genre</label>
                <input v-model="formData.genre" type="text" id="genre" name="genre"
                    class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                    placeholder="Enter genre" style="border-color: #ADEFD1;" />
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="mb-4">
                    <label for="audioFile" class="block text-platinum-white text-sm font-medium mb-1"
                        style="color: #EAEAEA;">Audio File</label>
                    <input type="file" id="audioFile" name="audioFile"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                        @change="convertToBase64('audio_file', $event)" />
                </div>

                <div class="mb-4">
                    <label for="image" class="block text-platinum-white text-sm font-medium mb-1"
                        style="color: #EAEAEA;">Image</label>
                    <input type="file" id="image" name="image"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                        @change="convertToBase64('image', $event)" />
                </div>
            </div>

            <div class="mb-4">
                <label for="lyrics" class="block text-platinum-white text-sm font-medium mb-1"
                    style="color: #EAEAEA;">Lyrics</label>
                <textarea v-model="formData.lyrics" id="lyrics" name="lyrics"
                    class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                    placeholder="Enter lyrics" style="border-color: #ADEFD1;"></textarea>
            </div>

            <div class="flex justify-center">
                <button type="submit"
                    class="bg-sunset-orange text-platinum-white px-6 py-3 rounded-md font-medium hover:bg-sunset-orange-dark"
                    style="background-color: #F66B0E; color: #EAEAEA;">
                    Add Song
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
            formData: {
                name: '',
                singer: '',
                genre: '',
                audio_file: '',
                image: '',
                lyrics: '',
            },
            albums: [],
        };
    },

    methods: {
        async submitForm() {
            const token = localStorage.getItem('token');
            console.log(this.formData);
            try {
                const response = await fetch('http://127.0.0.1:8000/api/admin/songs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                        'Accept': 'application/json',
                    },
                    body: JSON.stringify(this.formData),
                });
                const data = await response.json();
                if (data.status){
                    console.log('Song added successfully:', data);
                    this.showEventPopup('success', 'success', 'Song added successfully');
                } else{
                    this.showEventPopup('failure', 'Failed to add song', data.error);
                }
            } catch (error) {
                this.showEventPopup('failure', 'Failed to add song', error);
                console.error('Error adding song:', error);
            }
        },

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
                    console.log(data.msg);
                    this.albums = data.msg;
                    this.loading = false;
                } else {
                    this.showEventPopup('failure', 'Error fetching albums', data.error);
                }
            } catch (error) {
                this.showEventPopup('failure', 'Error fetching albums', error);
            }
        },

        convertToBase64(key, event) {
            return new Promise((resolve, reject) => {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.formData[key] = e.target.result;
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
    props: ['showEventPopup']
};
</script>