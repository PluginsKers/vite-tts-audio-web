<template>
  <GithubIcon />
  <TextToSpeech class="bg-gray-200" />
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import TextToSpeech from './components/TextToSpeech.vue';
import GithubIcon from './components/Github.vue';

export default defineComponent({
  name: 'App',
  components: {
    TextToSpeech,
    GithubIcon
  }
})
</script>

<style>
body {
  background-color: rgb(229 231 235);
}
</style>
