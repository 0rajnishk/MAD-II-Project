<template>
    <br>
    <br>
    <br>
    <div class="bg-midnight-blue-500 p-8 rounded-lg shadow-lg max-w-xl mx-auto" style="background-color: #00203F;">
        
        <h2 class="text-3xl font-semibold text-platinum-white mb-6" style="color: #EAEAEA;">Add New Album <span @click="something()" >something</span></h2> 

        
        <form @submit.prevent="submitForm" class="grid grid-cols-1 gap-4">
            
            <div class="grid grid-cols-2 gap-4">
                <div class="mb-4">
                    <label for="songName" class="block text-platinum-white text-sm font-medium mb-1"
                        style="color: #EAEAEA;">Album Name</label>
                    <input v-model="formData.name" type="text" id="songName" name="songName"
                        class="w-full px-4 py-2.5 border rounded-md focus:outline-none focus:border-electric-cyan-500"
                        placeholder="Enter song name" style="border-color: #ADEFD1;" />
                </div>

                <div class="mb-4">
                    <label for="singer" class="block text-platinum-white text-sm font-medium mb-1"
                        style="color: #EAEAEA;">singer</label>
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
            


            
            <div class="flex justify-center">
                <button type="submit"
                    class="bg-sunset-orange text-platinum-white px-6 py-3 rounded-md font-medium hover:bg-sunset-orange-dark"
                    style="background-color: #F66B0E; color: #EAEAEA;">
                    Add Album
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
            },
        };
    },
    methods: {
        async submitForm() {

            const token = localStorage.getItem('token');
            console.log(this.formData);

            try {
                const response = await fetch('http://127.0.0.1:8000/api/admin/albums', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                        'Accept': 'application/json',
                    },

                    body: JSON.stringify(this.formData),
                });
                const data = await response.json();
                if (data.status) {
                    this.showEventPopup('success', 'Album added successfully');
                    console.log(data.msg);
                } else {
                    console.error('Error adding album:');
                    this.showEventPopup('failure', 'Failed to add album')
                }
            } catch (error) {
                console.error('Error adding song:', error);
                console.log('Error sol pa song!!!');
            }
        },
        something() {
             this.showEventPopup('failure', "failse", 'Failed to add album')
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
