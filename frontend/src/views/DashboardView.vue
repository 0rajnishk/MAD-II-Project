<template>
    <NavBar />
    <div>
        <event-popup :is-visible="showPopup" :type="popupType" :heading="popupHeading" :body="popupBody"
            @close="showPopup = false" :timeout="popupTimeout"></event-popup>

    </div>

    <div class="flex justify-start mt-1.5 p-4 bg-gradient-to-r from-teal-400 to-blue-500">
        <button @click="AddSong()"
            class="text-white bg-green-500 hover:bg-green-600 text-xl font-semibold px-4 py-2 mr-2 border border-transparent hover:border-gray-300 rounded transition ease-in-out duration-150">
            Add song
        </button>
        <button @click="AddAlbum()"
            class="text-white bg-green-500 hover:bg-green-600 text-xl font-semibold px-4 py-2 border border-transparent hover:border-gray-300 rounded transition ease-in-out duration-150">
            Add album
        </button>

            <button @click="exportData()"
            class="text-white bg-green-500 hover:bg-green-600 text-xl font-semibold px-4 py-2 mx-4 border border-transparent hover:border-gray-300 rounded transition ease-in-out duration-150">
            Export
        </button>

    </div>


    <div class="popup" style="background-color: rgba(255, 255, 255, 0.8);">
        <span class="close" @click="closePopup()">&times;</span>
        <AddSong v-if="addsong" :show-event-popup="showEventPopup" />
        <AddAlbum v-if="addalbum" :show-event-popup="showEventPopup" />
        <EditAlbum v-if="editalbum" :albumId="albumId" :show-event-popup="showEventPopup" />
        <EditSong v-if="editsong" :songId="songId" :show-event-popup="showEventPopup" />
    </div>

    <div class="bg-gradient-to-r from-teal-400 to-blue-500">
        <div class="dashboard-body pt-10 pb-10 flex items-center justify-center">
            <div class="overflow-x-auto w-auto md:w-3/4 text-center">
                <table class="min-w-full table-auto border border-gray-300 p-4">
                    <thead class="bg-teal-500 text-white">
                        <tr>
                            <th class="py-4 px-6">Song Id</th>
                            <th class="py-4 px-6">Song Name</th>
                            <th class="py-4 px-6">Singer</th>
                            <th class="py-4 px-6">Genre</th>
                            <th class="py-4 px-6">Album</th>
                            <th class="py-4 px-6">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Loop through user's songs and display details -->
                        <tr v-for="(song, index) in songs" :key="index"
                            class="border-b text-gray-800 hover:bg-gray-200">
                            <td>
                                <span class="ml-2">{{ song.id }}</span>
                            </td>
                            <td>{{ song.name }}</td>
                            <td>{{ song.singer }}</td>
                            <td>{{ song.genre }}</td>
                            <td>{{ song.album_id }}</td>

                            <td>
                                <button @click="EditSong(song.id)"
                                    class="text-white bg-green-500 hover:bg-green-600 text-xl font-semibold px-4 py-2 mr-2 border border-transparent hover:border-gray-300 rounded transition ease-in-out duration-150">
                                    Edit
                                </button>
                                <button @click="DeleteSong(song.id)"
                                    class="text-white bg-red-600 hover:bg-red-700 text-xl font-semibold px-4 py-2 border border-transparent hover:border-gray-300 rounded transition ease-in-out duration-150">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>
        </div>

        <!-- fetch all -->
        <div class="dashboard-body pt-10 pb-10 flex items-center justify-center">
            <div class="overflow-x-auto w-auto md:w-3/4 text-center">
                <table class="min-w-full table-auto border border-gray-300 p-4">
                    <thead class="bg-teal-500 text-white">
                        <tr>
                            <th class="py-4 px-6">Album Name</th>
                            <th class="py-4 px-6">Singer</th>
                            <th class="py-4 px-6">Genre</th>
                            <th class="py-4 px-6">Action</th>
                        </tr>
                    </thead>
                    <tbody>

                        <!-- Loop through user's albums and display details -->
                        <tr v-for="(album, index) in albums" :key="index"
                            class="border-b text-gray-800 hover:bg-gray-200">
                            <td>
                                <span class="ml-2">{{ album.name }}</span>
                            </td>
                            <td>{{ album.singer }}</td>
                            <td>{{ album.genre }}</td>
                            <td>
                                <button @click="EditAlbum(album.id)"
                                    class="text-white bg-green-500 hover:bg-green-600 text-xl font-semibold px-4 mr-4 py-2 border border-transparent hover:border-gray-300 rounded transition ease-in-out duration-150">
                                    Edit
                                </button>
                                <button @click="DeleteAlbum(album.id)"
                                    class="text-white bg-red-600 hover:bg-red-700 text-xl font-semibold px-4 py-2 border border-transparent hover:border-gray-300 rounded transition ease-in-out duration-150">
                                    Delete
                                </button>
                            </td>
                        </tr>

                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <AppFooter />
</template>
<style>
.left-m {
    margin-left: 0%;
}

.popup {
    display: none;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9;
    background: white;
    padding: 50px;
    border-radius: 10px;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.1);
}

.close {
    position: absolute;
    top: -10px;
    right: 10px;
    font-size: 42px;
    cursor: pointer;
    color: #000;
}
</style>


<script>

import AddSong from '../components/AddSong.vue';
import AddAlbum from '../components/AddAlbum.vue';
import EditAlbum from '../components/EditAlbum.vue';
import EditSong from '../components/EditSong.vue';
import AppFooter from '../components/AppFooter.vue';
import NavBar from '../components/NavBar.vue';
import eventPopup from '../components/EventPopup.vue';

export default {
    components: {
        NavBar,
        AppFooter,
        AddSong,
        AddAlbum,
        EditAlbum,
        EditSong,
        eventPopup,
    },
    data() {
        return {
            songs: [],
            albums: [],
            sloading: true,
            aloading: true,
            addsong: false,
            addalbum: false,
            editsong: false,
            editalbum: false,
            songId: null,
            albumId: null,
            showPopup: false,
            popupType: '',
            popupHeading: '',
            popupBody: '',
            popupTimeout: 3000 
        };
    },
    methods: {
        // Function to fetch all songs and albums
        async fetchallsongs() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/admin/songs`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                        'Accept': 'application/json',
                    },
                });
                const data = await response.json();
                if (data.status) {
                    this.songs = data.songs;
                    this.sloading = false;
                } else {
                    console.log(data.error);
                }
            } catch (error) {
                console.error('Error fetching songs:', error);
            }
        },
        // fetch all albums
        async fetchallalbums() {
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('http://127.0.0.1:8000/api/admin/albums', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                });
                const data = await response.json();
                console.log(data.msg);
                if (data.status) {
                    this.albums = data.msg;
                    this.loading = false;
                } else {
                    console.log(data.error);
                }
            } catch (error) {
                console.error('Error fetching albums:', error);
            }
        },
        AddSong() {
            var popup = document.querySelector('.popup');
            this.addsong = true;
            popup.style.display = 'block';
        },
        AddAlbum() {
            var popup = document.querySelector('.popup');
            this.addalbum = true;
            popup.style.display = 'block';
        },
        EditSong(id) {
            this.songId = id;
            var popup = document.querySelector('.popup');
            this.editsong = true;
            popup.style.display = 'block';
            this.$nextTick(() => {
                this.$watch('songId', this.fetchSong);
            });
        },
        EditAlbum(id) {
            this.albumId = id;
            var popup = document.querySelector('.popup');
            this.editalbum = true;
            popup.style.display = 'block';
            this.$nextTick(() => {
                this.$watch('albumId', this.fetchAlbum);
            });
        },
        closePopup() {
            var popup = document.querySelector('.popup');
            this.addsong = false;
            this.addalbum = false;
            this.editsong = false;
            this.editalbum = false;
            popup.style.display = 'none';
        },
        async DeleteSong(id) {
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
        async DeleteAlbum(id) {
            const token = localStorage.getItem('token');
            try {
                // /api/albums?album_id=2
                const response = await fetch(`http://127.0.0.1:8000/api/albums?album_id=${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                });
                const data = await response.json();
                if (data.status) {
                    this.showEventPopup('success', 'success', 'Album deleted successfully');
                    this.fetchallalbums()

                } else {
                    console.log(data.error);
                }
            } catch (error) {
                console.error('Error deleting song:', error);
            }     
        },
    showEventPopup(type, heading, body, timeout) {
      this.popupType = type;
      this.popupHeading = heading;
      this.popupBody = body;
      this.showPopup = true;

      if (timeout !== undefined) {
        this.popupTimeout = timeout;
      }
    },
    async exportData() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://127.0.0.1:8000/api/export', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (data.status) {
          this.showEventPopup('success', 'success', 'Data exported successfully');
          alert('exporting data')
        } else {
          console.log(data.error);
        }
        } catch (error) {
            console.error('Error exporting data:', error);
            }
    },

    },
    mounted() {
        this.fetchallsongs();
        this.fetchallalbums();
    },
};
</script>

