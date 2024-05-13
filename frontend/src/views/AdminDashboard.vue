<template>
    <main>
        <NavBar />
        <event-popup :is-visible="showPopup" :type="popupType" :heading="popupHeading" :body="popupBody"
            @close="showPopup = false" :timeout="popupTimeout"></event-popup>

        <div class="flex">
            <SideBar @play-song="songID" :show-event-popup="showEventPopup" title="Dashboard" />


            <div class="flex-1 p-4">
                <!-- ============================================================================================================================= -->

                <ShowStats />
                <!-- Reported Songs Section -->
                <div class="left10">
                    <h1 class="text-3xl font-bold mb-4">Reported Songs</h1>
                    <div v-if="loading" class="text-gray-500">Loading...</div>
                    <div v-else>
                        <div v-if="reportedSongs.length === 0" class="text-gray-500">No reported songs found.</div>
                        <div v-else>
                            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                                <div v-for="reportedSong in reportedSongs" :key="reportedSong.id"
                                    class="bg-white shadow-md rounded-lg overflow-hidden">
                                    <div class="p-4">
                                        <h3 class="text-lg font-semibold mb-2">{{ reportedSong.reason }}</h3>
                                        <p class="text-sm text-gray-500">{{ formattedDate(reportedSong.timestamp) }}</p>
                                        <div class="flex justify-between mt-4">
                                            <button @click="DeleteSong(reportedSong.id)"
                                                class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600">Remove
                                                this song</button>
                                        </div>
                                    </div>
                                    <div class="border-t border-gray-200 p-4">
                                        <dl class="grid grid-cols-1 gap-x-4 gap-y-2">
                                            <div>
                                                <dt class="text-sm font-medium text-gray-500">Song ID</dt>
                                                <dd class="mt-1 text-sm text-gray-900">{{ reportedSong.song_id }}</dd>
                                            </div>
                                            <div>
                                                <dt class="text-sm font-medium text-gray-500">User ID</dt>
                                                <dd class="mt-1 text-sm text-gray-900">{{ reportedSong.user_id }}</dd>
                                            </div>
                                        </dl>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- End of Reported Songs Section -->

                <!-- ============== Blacklisted Users ========================================================= -->
                <BlackList />
                <users-comp />
                <!-- ============== Blacklisted Users ========================================================= -->
                <!-- ============================================================================================================================= -->
                <ShowSong @play-song="songID" />
                <ShowAlbum />
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
import eventPopup from '../components/EventPopup.vue';
import AudioPlayer from '../components/AudioPlayer.vue';

import NavBar from '../components/admin/NavBar.vue';
import ShowSong from '../components/admin/ShowSong.vue';
import ShowAlbum from '../components/admin/ShowAlbum.vue';
import SideBar from '../components/admin/SideBar.vue';
import ShowStats from '../components/admin/ShowStats.vue';
import BlackList from '../components/admin/BlackList.vue';
import UsersComp from '../components/admin/UsersComp.vue';

export default {
    components: {
        NavBar,
        ShowSong,
        AudioPlayer,
        ShowAlbum,
        AppFooter,
        SideBar,
        eventPopup,
        ShowStats,
        BlackList,
        UsersComp,
    },
    data() {
        return {
            song_id: null,
            showPopup: false,
            popupType: '',
            popupHeading: '',
            popupBody: '',
            popupTimeout: 3000 ,
                  loading: false,
            reportedSongs: []
        };
    },
    methods: {
        songID(song) {
            this.song_id = song;
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
        fetchReportedSongs() {
            this.loading = true;
            const token = localStorage.getItem('token');
            fetch('http://127.0.0.1:8000/api/reported_songs',{
                headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    },
            })
                .then(response => response.json())
                .then(data => {
                    this.reportedSongs = data.reported_songs;
                    this.loading = false;
                })
                .catch(error => {
                    console.error('Error fetching reported songs:', error);
                    this.loading = false;
                });
        },
        formattedDate(timestamp) {
            const date = new Date(timestamp);
            return date.toLocaleString();
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
        checkRole() {
            const role = localStorage.getItem('role');
            if (role === 'creator'){
                this.$router.push('/dashboard')
            };
            if (role === 'user'){
                this.$router.push('/')
            }
        },

    },
    mounted() {
        this.song_id = 0;
        this.fetchReportedSongs();
        this.checkRole();   
    },
    
};
</script>

<style>
main {
    background-color: #6E7E85;
    min-height: 100vh;
}
.left10 {
    margin-left: 18%;
    margin-right: 4%;
}
</style>