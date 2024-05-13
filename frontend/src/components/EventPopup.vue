<template>
    <transition name="event-popup">
        <div v-if="isVisible" :class="['event-popup', type]">
            <div class="event-popup-header">{{ heading }}</div>
            <div class="event-popup-body">{{ body }}</div>
        </div>
    </transition>
</template>

<script>
export default {
    name: 'EventPopup',
    props: {
        isVisible: {
            type: Boolean,
            default: false
        },
        type: {
            type: String,
            default: 'success' // Default to success, can be 'success' or 'failure'
        },
        heading: {
            type: String,
            default: ''
        },
        body: {
            type: String,
            default: ''
        },
        timeout: {
            type: Number,
            default: 3000 // Default timeout in milliseconds
        }
    },
    data() {
        return {
            timer: null
        }
    },
    watch: {
        isVisible(newVal) {
            if (newVal) {
                this.startTimer();
            } else {
                this.clearTimer();
            }
        }
    },
    methods: {
        startTimer() {
            if (this.timeout > 0) {
                this.timer = setTimeout(() => {
                    this.$emit('close');
                }, this.timeout);
            }
        },
        clearTimer() {
            clearTimeout(this.timer);
        }
    },
    beforeUnmount() {
        this.clearTimer();
    }
}
</script>

<style scoped>
.event-popup {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px;
    border-radius: 5px;
    z-index: 1000;
}

.event-popup-header {
    font-weight: bold;
}

.success {
    background-color: #32CD32;
    /* Use your preferred success color */
    color: #fff;
}

.failure {
    background-color: #FF6347;
    /* Use your preferred failure color */
    color: #fff;
}

.event-popup-enter-active,
.event-popup-leave-active {
    transition: opacity 0.5s;
}

.event-popup-enter,
.event-popup-leave-to

/* .event-popup-leave-active in <2.1.8 */
    {
    opacity: 0;
}
</style>
