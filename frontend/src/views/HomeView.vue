<template>
  <main>
    <NavBar />
    <event-popup :is-visible="showPopup" :type="popupType" :heading="popupHeading" :body="popupBody"
      @close="showPopup = false" :timeout="popupTimeout"></event-popup>

    <div class="flex">
      <SideBar @play-song="songID" :show-event-popup="showEventPopup" title="Dashboard" />
      <div class="flex-1 p-4">
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

import NavBar from '../components/NavBar.vue';
import ShowSong from '../components/ShowSong.vue';
import ShowAlbum from '../components/ShowAlbum.vue';
import SideBar from '../components/SideBar.vue';

export default {
  components: {
    NavBar,
    ShowSong,
    AudioPlayer,
    ShowAlbum,
    AppFooter,
    SideBar,
    eventPopup,
  },
  data() {
    return {
      song_id: null,
      showPopup: false,
      popupType: '',
      popupHeading: '',
      popupBody: '',
      popupTimeout: 3000 
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
    checkRole() {
      const role = localStorage.getItem('role');
      if (role == '"admin"') {
        alert('You are not authorized to view this page');
        this.$router.push('/admin');
      };
    },
  },
  mounted() {
    this.song_id = 0;
    this.checkRole();
  },
};
</script>

<style>
main {
  background-color: #6E7E85;
  min-height: 100vh;
}
</style>