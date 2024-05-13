<template>
    <!-- ====================================================================================================================== -->
    <div>

        <div v-if="showModal" class="fixed inset-0 z-50 overflow-auto bg-gray-500 bg-opacity-75 flex">
            <div class="relative p-8 bg-white w-full max-w-md m-auto flex-col flex rounded-lg">
                <button @click="showModal = false" class="absolute top-0 right-0 p-4">
                    <svg class="h-6 w-6 fill-current text-gray-600" xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20">
                        <path
                            d="M13.414 12l4.293 4.293a1 1 0 01-1.414 1.414L12 13.414l-4.293 4.293a1 1 0 01-1.414-1.414L10.586 12 6.293 7.707a1 1 0 111.414-1.414L12 10.586l4.293-4.293a1 1 0 011.414 1.414L13.414 12z" />
                    </svg>
                </button>

                <h1 class="text-lg font-bold mb-4">Add to Playlist</h1>

                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2">Choose:</label>
                    <div class="flex items-center">
                        <input type="radio" id="create" value="create" v-model="option" class="mr-2">
                        <label for="create" class="mr-4">Create New Playlist</label>

                        <input type="radio" id="existing" value="existing" v-model="option" class="mr-2">
                        <label for="existing">Add to Existing Playlist</label>
                    </div>
                </div>

                <div v-if="option === 'create'" class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2">Playlist Name:</label>
                    <input type="text" v-model="newPlaylistName" class="w-full px-3 py-2 border rounded">
                </div>

                <div v-if="option === 'existing'" class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2">Select Playlist:</label>
                    <select v-model="selectedPlaylistId" class="w-full px-3 py-2 border rounded">
                        <option value="">Select Playlist</option>
                        <option v-for="playlist in playlists" :key="playlist.id" :value="playlist.id">{{ playlist.name
                            }}</option>
                    </select>
                </div>

                <div class="text-right">
                    <button @click="addToPlaylist"
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Add Song
                    </button>
                </div>
            </div>
        </div>
    </div>
    <!-- ====================================================================================================================== -->
    <div class="grid grid-cols-3 gap-4 floating-audio-player">
        <div class="maximize-minimize-icons">
            <button @click="toggleWide" v-if="wide">
                <img src="../assets/icons/maximize.svg" alt="Maximize" class="w-6 h-6">
            </button>
            <button @click="toggleWide" v-else>
                <img src="../assets/icons/minimize.svg" alt="Minimize" class="w-6 h-6">
            </button>
        </div>

        <div class="audio-player-container mx-auto my-8 p-6 mb-4 col-start-2 col-end-6 bg-gray-300 rounded-lg shadow-lg flex items-center"
            :class="{ 'w-4/5 mr-8': wide, 'w-2/5 mr-8': !wide }">


            <div class="track-info flex-grow">
                <div class="grid grid-cols-5" @click="toggleLyricsHeight">
                    <div class="col-start-0 col-end-2">
                        <h3 class="text-lg font-semibold text-gray-800">{{ artist_name }}</h3>
                        <p class="text-gray-600">{{ track_title }}</p>
                        <div class="album-art flex-shrink-0">
                            <img :src="albumArtSrc" alt="Album Art" class="w-24 h-24 rounded-lg shadow-sm">
                        </div>
                    </div>
                    <div class="col-start-2 col-end-6 lyrics-container" :class="{ expanded: isExpanded }">
                        <span v-html="sanitizeLyrics(lyrics)"></span>
                    </div>
                </div>
                <div style="margin-left: 90vh;" v-if="wide">
                    <!-- Custom Play/Pause Button -->

                    <div class="ml-8">
                        <button @click="reportSong" class="mr-4">
                            <img src="../assets/icons/report-song.svg" alt="Play" class="w-8 h-8">
                        </button>
                        <!-- Add to Playlist Button -->
                        <!-- <button @click="likeSong">
                            <img v-if="!like" src="../assets/icons/empty-heart.svg" alt="Add to Playlist"
                                class="w-8 h-8">
                            <img v-else src="../assets/icons/filled-heart.svg" alt="Add to Playlist" class="w-8 h-8">
                        </button> -->
                    </div>
                    <div class="mr-4">
                        <RatingComp :song__id="song__id" />
                    </div>
                </div>
                <div class="flex items-center mt-4">
                    <!-- Custom Play/Pause Button -->
                    <button @click="togglePlay" class="mr-4">
                        <img v-if="!isPlaying" src="../assets/icons/play.svg" alt="Play" class="w-8 h-8">
                        <img v-else src="../assets/icons/pause.svg" alt="Pause" class="w-8 h-8">
                    </button>
                    <!-- Add to Playlist Button -->
                    <button @click="showModal = true">
                        <img src="../assets/icons/add-to-playlist.svg" alt="Add to Playlist" class="w-8 h-8">
                    </button>

                    <input type="range" class="timeline-slider ml-4" :value="currentTime" @input="seekAudio">
                </div>

                <!-- Hidden Native Audio Player -->
                <audio ref="audio" :song_id="2" @ended="audioFinish" @timeupdate="updatePlaybackTime" class="hidden"
                    controls></audio>
            </div>
        </div>
    </div>

</template>
<style scoped>
/* Add styling for the timeline slider */
.timeline-slider {
    width: 100%;
    height: 4px;
    border-radius: 2px;
    background: linear-gradient(to right, #00203F, #ADEFD1, #F66B0E);
    outline: none;
    opacity: 0.7;
    transition: opacity 0.2s;
}

.timeline-slider:hover {
    opacity: 1;
}

.album-art img {
    border: 4px solid #EAEAEA;
}

.track-info h3 {
    color: #00203F;
}

.track-info p {
    color: #6E7E85;
}

.lyrics-container {
    letter-spacing: 2px;
    word-spacing: 5px;
    text-align: center;
    max-height: 150px;
    overflow-y: auto;
    padding-right: 10px;
    scrollbar-width: thin;
    scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
    transition: max-height 0.3s ease;
}

.lyrics-container.expanded {
    max-height: 400px;
}

.lyrics-container::-webkit-scrollbar {
    width: 8px;
}

.lyrics-container::-webkit-scrollbar-thumb {
    background-color: var(--scrollbar-thumb);
}

.lyrics-container::-webkit-scrollbar-track {
    background-color: var(--scrollbar-track);
}

.floating-audio-player {
    position: fixed;
    bottom: 0;
    right: 0;
    width: 100%;
    background-color: #ffffff00;
    z-index: 10;
}

.maximize-minimize-icons {
    position: absolute;
    top: 3vh;
    right: 4vh;
    padding: 10px;
}
</style>
<script>
import RatingComp from './RatingComp.vue';

export default {
    name: "AudioPlayer",
    props: {
        song_id: Number,
    },
    components: {
        RatingComp,
    },
    data() {
        return {
            artist_name: 'Track Title',
            track_title: 'Song Name',
            isPlaying: true,
            currentTime: 0,
            lyrics: `Lyrics not available for this song. `,
            isExpanded: false,
            albumArtSrc: 'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg',
            wide: true,
            like: false,
            showModal: false,
            option: 'create',
            newPlaylistName: '',
            selectedPlaylistId: null,
            playlists: [],
            song__id: 0,
        };
    },
    methods: {
        async loadAudio(songId) {
            if (songId != null && songId != 0) {
                try {
                    const response = await fetch(`http://127.0.0.1:8000/api/songs/audio/${songId}?audio=1`);
                    const data = await response.json();


                    const base64Audio = data.msg.audio_file;
                    this.lyrics = data.msg.lyrics;
                    this.albumArtSrc = `data:image/png;base64,${data.msg.image}`;
                    this.artist_name = data.msg.user_id;
                    this.track_title = data.msg.name;


                    if (!base64Audio) {
                        console.error('Base64 audio data is missing or empty.');
                        return;
                    }

                    const binaryData = atob(base64Audio);
                    const arrayBuffer = new ArrayBuffer(binaryData.length);
                    const uint8Array = new Uint8Array(arrayBuffer);

                    for (let i = 0; i < binaryData.length; i++) {
                        uint8Array[i] = binaryData.charCodeAt(i);
                    }

                    const blob = new Blob([uint8Array], { type: 'audio/mp3' });


                    const objectUrl = URL.createObjectURL(blob);
                    this.$refs.audio.src = objectUrl;

                    await new Promise(resolve => {
                        this.$refs.audio.addEventListener('loadedmetadata', resolve, { once: true });
                    });
                    this.addToRecentlyPlayed();

                } catch (error) {
                    console.error('Error fetching audio:', error);
                }
            }
        },
        async addToRecentlyPlayed() {
            const token = localStorage.getItem('token');
            const requestData = {
                song_id: this.song__id,
            };
            try {
                const response = await fetch('http://127.0.0.1:8000/api/recently_played_songs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    },
                    body: JSON.stringify(requestData)
                });
                const data = await response.json();
                console.log(data.msg);
            } catch (error) {
                console.error('Error updating rating:', error);
            }
        },
        async togglePlay() {
            try {
                if (this.isPlaying) {
                    await this.$refs.audio.pause();
                } else {

                    if (!this.$refs.audio.src) {

                        await this.loadAudio();
                    }
                    await this.$refs.audio.play();
                }

                this.isPlaying = !this.isPlaying;
            } catch (error) {
                console.error('Error toggling play:', error);
            }
        },

        audioFinish() {
            this.isPlaying = false;
        },

        updatePlaybackTime() {
            if (this.$refs.audio) {
                const playPercentage = (this.$refs.audio.currentTime / this.$refs.audio.duration) * 100;
                this.currentTime = playPercentage;
            }
        },

        seekAudio(event) {

            const percentage = event.target.value;
            const newTime = (percentage / 100) * this.$refs.audio.duration;

            this.$refs.audio.currentTime = newTime;
            this.currentTime = percentage;

            if (this.isPlaying) {
                this.$refs.audio.play();
            }
        },

        sanitizeLyrics(lyrics) {
            return lyrics.replace(/\n/g, '<br>');
        },

        toggleLyricsHeight() {
            this.isExpanded = !this.isExpanded;
        },

        handleMessageUpdate(message, oldValue) {
            console.log("Message updated in ComponentB: " + message + " (was: " + oldValue + ")");
        },

        toggleWide() {
            this.wide = !this.wide;
        },

        async likeSong() {
            // Toggle the like state immediately for responsive UI, but you might want to wait for successful response depending on your UX choice
            this.like = !this.like;

            const token = localStorage.getItem('token');
            // const action = this.like ? 'like' : 'unlike'; // Determine the action based on the current like state
            const method = this.like ? 'POST' : 'DELETE'; // POST to like, DELETE to unlike

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/like`, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        "song_id": this.song_id,
                    })
                });

                if (response.ok) {
                    // Handle response here, e.g., show a message or update the UI accordingly
                    console.log(`Song d successfully.`);
                } else {
                    // If the request failed, revert the like state change
                    this.like = !this.like;
                    console.log(`There was a problem  the song. Please try again later.`);
                }
            } catch (error) {
                // If there's an error, revert the like state change
                this.like = !this.like;
                console.error(`Error song:`, error);
                console.log('There was an error. Please try again later.');
            }
        },

        reportSong() {
            // Prompt user for a reason for the report
            const reason = window.prompt("Please enter the reason for reporting this song:");
            if (reason) {
                this.sendReport(this.song_id, reason);
            }
        },
        async sendReport(songId, reason) {
            console.log('Sending report...');
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('http://127.0.0.1:8000/api/report', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        "song_id": songId,
                        "reason": reason
                    })
                });

                if (response.ok) {
                    console.log('Thank you for your report. We will review it shortly.');
                } else {
                    console.log('There was a problem submitting your report. Please try again later.');
                }
            } catch (error) {
                console.error('Error submitting report:', error);
                console.log('There was an error. Please try again later.');
            }
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

        async addToPlaylist() {
            if (this.option === 'create') {
                if (!this.newPlaylistName) {
                    console.log('Please enter a name for the new playlist.');
                    return;
                } else {
                    this.createNewPlaylist();
                }
            } else if (this.option === 'existing') {
                if (!this.selectedPlaylistId) {
                    console.log('Please select a playlist to add the song to.');
                    return;
                }
                this.addToExistingPlaylist();
            }
        },

        async createNewPlaylist() {
            console.log('Creating new playlist...');
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('http://127.0.0.1:8000/api/playlists', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        "name": this.newPlaylistName,
                        "song_id": this.song_id
                    }),
                });
                const data = await response.json();
                if (response.ok) {
                    console.log(data.msg);
                    this.fetchPlaylists(); // Assuming this method exists to fetch playlists after creation
                } else {
                    throw new Error(data.error || 'Failed to create playlist.');
                }
            } catch (error) {
                console.error('Error creating playlist:', error);
                console.log('Error creating playlist: ' + error.message);
            }
        },

        async addToExistingPlaylist() {
            console.log('Adding to existing playlist...');
            const token = localStorage.getItem('token');
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/playlists`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        "song_id": this.song_id,
                        "playlist_id": this.selectedPlaylistId
                    }),
                });
                const data = await response.json();
                if (response.ok) {
                    console.log('Song added to playlist successfully!!!');
                } else {
                    throw new Error(data.error || 'Failed to add song to playlist.');
                }
            } catch (error) {
                console.error('Error adding song to playlist:', error);
                console.log('Error adding song to playlist: ' + error.message);
            }
        },

    },
    mounted() {
        this.fetchPlaylists();
    },
    watch: {
        async song_id(newValue) {
            this.song__id = newValue;
            this.loadAudio(newValue);
            this.togglePlay();

            this.$refs.audio.addEventListener('loadedmetadata', async () => {
                this.$refs.audio.currentTime = 0;

                // Ensure the current time is updated before toggling play
                await this.$nextTick();

                if (this.isPlaying) {
                    await this.togglePlay();
                }

                // Play the new song
                await this.togglePlay();
            }, { once: true });
        },

    },
};

</script>
