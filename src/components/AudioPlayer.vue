<template>
  <div class="w-full max-w-lg mx-auto">
    <div class="flex items-center justify-between p-2 bg-gray-100 rounded shadow">
      <button @click="togglePlay" class="flex justify-center items-center w-10 h-10">
        <svg v-if="!isPlaying" t="1717430100452" class="icon" viewBox="0 0 1024 1024" version="1.1"
          xmlns="http://www.w3.org/2000/svg" p-id="4278" width="30" height="30">
          <path
            d="M817.088 484.96l-512-323.744C295.232 154.976 282.752 154.592 272.576 160.224 262.336 165.856 256 176.608 256 188.256l0 647.328c0 11.648 6.336 22.4 16.576 28.032 4.8 2.656 10.112 3.968 15.424 3.968 5.952 0 11.904-1.664 17.088-4.928l512-323.616C826.368 533.184 832 522.976 832 512 832 501.024 826.368 490.816 817.088 484.96z"
            fill="#2c2c2c" p-id="4279"></path>
        </svg>
        <svg v-else t="1717430144465" class="icon" viewBox="0 0 1024 1024" version="1.1"
          xmlns="http://www.w3.org/2000/svg" p-id="5500" width="40" height="40">
          <path d="M688 288H336a48 48 0 0 0-48 48v352a48 48 0 0 0 48 48h352a48 48 0 0 0 48-48V336a48 48 0 0 0-48-48z"
            fill="#2c2c2c" p-id="5501"></path>
        </svg>
      </button>
      <a :href="audioUrl" download class="flex justify-center items-center w-10 h-10">
        <svg t="1717430305832" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="6997" width="30" height="30">
          <path
            d="M707.84 384H640V170.666667c0-23.466667-19.2-42.666667-42.666667-42.666667h-170.666666c-23.466667 0-42.666667 19.2-42.666667 42.666667v213.333333H316.16c-37.973333 0-57.173333 46.08-30.293333 72.96l195.84 195.84c16.64 16.64 43.52 16.64 60.16 0l195.84-195.84c26.88-26.88 8.106667-72.96-29.866667-72.96zM213.333333 810.666667c0 23.466667 19.2 42.666667 42.666667 42.666666h512c23.466667 0 42.666667-19.2 42.666667-42.666666s-19.2-42.666667-42.666667-42.666667H256c-23.466667 0-42.666667 19.2-42.666667 42.666667z"
            fill="#2c2c2c" p-id="6998"></path>
        </svg>
      </a>
    </div>
    <audio ref="audio" :src="audioUrl" @ended="isPlaying = false" class="hidden"></audio>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

defineProps({
  audioUrl: {
    type: String,
    required: true
  }
})

const audio = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)

const togglePlay = () => {
  if (audio.value) {
    if (isPlaying.value) {
      audio.value.pause()
    } else {
      audio.value.play()
    }
    isPlaying.value = !isPlaying.value
  }
}
</script>