<template>
    <div>
        <div class="stars">
            <span v-for="index in 5" :key="index" @click="rate(index)"
                :class="{ 'star-filled': index <= currentRating }">
                <img :src="index <= currentRating ? starFill : star" alt="star" @mouseover="hoverStar(index)"
                    @mouseleave="leaveStar" />
            </span>
        </div>
    </div>
</template>

<script>
import star from '@/assets/icons/star.svg';
import starFill from '@/assets/icons/star-fill.svg';

export default {
    data() {
        return {
            currentRating: 0,
            star,
            starFill,
        };
    },
    methods: {
        rate(index) {
            this.currentRating = index;
            this.updateRating(this.currentRating);

        },
        hoverStar(index) {
            for (let i = 0; i < index; i++) {
                this.$refs[`star${i + 1}`][0].classList.add('star-filled');
            }
        },
        leaveStar() {
            for (let i = 0; i < this.currentRating; i++) {
                if (i >= this.currentRating) {
                    this.$refs[`star${i + 1}`][0].classList.remove('star-filled');
                }
            }
        },
        async fetchRating(songid) {
            this.currentRating = 0;
            if(songid === 0) return
            const token = localStorage.getItem('token');
            try {
                const response = await fetch('http://127.0.0.1:8000/api/rating?song_id='+songid, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    }
                });
                const data = await response.json();
                this.currentRating = data.msg.rating;
            } catch (error) {
                console.error('Error fetching rating:', error);
            }
        },
        async updateRating(rating) {
            const token = localStorage.getItem('token');
            const requestData = {
                song_id: this.song__id,
                rating: rating
            };
            try {
                const response = await fetch('http://127.0.0.1:8000/api/rating', {
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
    },
    props: ['song__id'],
    mounted() {
        this.fetchRating(this.song__id);
    },
    watch: {
        song__id: function (newVal, oldVal) {
            console.log('song__id changed:', newVal, oldVal);
            this.fetchRating(newVal);
        }
    },
};
</script>

<style scoped>
.stars {
    display: flex;
    justify-content: center;
}

.stars img {
    width: 30px;
    height: 30px;
    cursor: pointer;
    margin: 0 5px;
    /* Add some margin between stars */
}

.star-filled img {
    filter: invert(36%) sepia(87%) saturate(4526%) hue-rotate(88deg) brightness(92%) contrast(88%);
}
</style>
