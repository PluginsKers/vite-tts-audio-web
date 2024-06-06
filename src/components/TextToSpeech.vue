<template>
    <div class="flex flex-col lg:flex-row justify-between items-center lg:justify-center h-screen p-4 gap-6">
        <div class="flex-grow-0 flex flex-col items-center justify-center w-full gap-4 px-4"
            :class="{ 'lg:border-r-2 lg:border-dashed lg:border-gray-300': !isLoading && audioUrl }">
            <h1 class="relative text-4xl flex flex-row items-center justify-center">
                <svg t="1717430346185" class="flashing mr-2 h-full" viewBox="0 0 1024 1024" version="1.1"
                    xmlns="http://www.w3.org/2000/svg" p-id="8066" width="26" height="26">
                    <path
                        d="M950.848 512q0 119.424-58.848 220.288t-159.712 159.712-220.288 58.848-220.288-58.848-159.712-159.712-58.848-220.288 58.848-220.288 159.712-159.712 220.288-58.848 220.288 58.848 159.712 159.712 58.848 220.288z"
                        p-id="8067" fill="#0a0a0a"></path>
                </svg>
                ChatTTS语音生成
            </h1>
            <div class="relative w-full max-w-lg">
                <textarea v-model="text"
                    class="relative w-full h-full p-2 border-0 outline-none rounded shadow-md min-h-10 max-h-[50vh] focus:ring-4 focus:ring-gray-100"
                    placeholder="输入你要转换的文本"
                    rows="5"
                    :class="{ 'text-gray-500 loader-stripes cursor-not-allowed': isLoading, 'bg-gray-50 focus:bg-white': !isLoading }"
                    :disabled="isLoading">
                </textarea>
            </div>

            <div @click="convertTextToSpeech"
                class="flex items-center justify-center bg-gray-900 hover:bg-gray-800 text-white px-2 py-1 h-10 rounded shadow-md w-full max-w-lg select-none"
                :class="{ 'cursor-not-allowed': isLoading, 'cursor-pointer': !isLoading }" :disabled="isLoading">
                <div v-if="isLoading" key="loading" class="flex items-center justify-center">
                    <div
                        class="loader border-t-gray-400 ease-linear rounded-full border-4 border-t-4 border-gray-200 h-6 w-6">
                    </div>
                </div>
                <div v-else class="text-md">点击生成</div>
            </div>
            <div v-if="errorMessage" class="text-red-500">{{ errorMessage }}</div>
        </div>
        <div v-if="!isLoading && audioUrl" class="w-full gap-4 px-4">
            <transition name="fade" mode="out-in">
                <div key="audio" class="flex flex-col w-full items-center justify-center">
                    <AudioPlayer :audioUrl="audioUrl" />
                </div>
            </transition>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import AudioPlayer from './AudioPlayer.vue'

const text = ref('')
const audioUrl = ref<string | null>(null)
const isLoading = ref(false)
const errorMessage = ref<string | null>(null)

interface Conversion {
    target: string;
    replacement: string;
}

const escapeRegExp = (string: string): string => {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const convertTextFormat = (text: string): string => {
    const conversions: Conversion[] = [
        { target: '，', replacement: ',' },
        { target: '.', replacement: ' [uv_break] ' },
        { target: ',', replacement: ' [uv_break] ' },
        { target: '。', replacement: ' [uv_break] ' },
        { target: '+', replacement: ' [uv_break] ' },
    ];

    let convertedText = text;
    conversions.forEach(conversion => {
        const regex = new RegExp(escapeRegExp(conversion.target), 'g');
        convertedText = convertedText.replace(regex, conversion.replacement);
    });

    return convertedText;
}

const convertTextToSpeech = async () => {
    if (!text.value || isLoading.value) return
    if (text.value.length < 6) {
        errorMessage.value = '输入内容过少，必须至少包含6个字符。'
        return
    }

    isLoading.value = true
    errorMessage.value = null

    try {
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/tts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: convertTextFormat(text.value) }),
        });

        if (!response.ok) {
            if (response.status === 400) {
                const errorData = await response.json();
                throw new Error(errorData.error);
            }
            throw new Error('Network response was not ok');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        audioUrl.value = url;
    } catch (error) {
        console.error('Error:', error);
        errorMessage.value = (error as Error).message;
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
.loader-stripes {
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(-45deg,
            transparent,
            transparent 10px,
            rgba(255, 255, 255, 0.8) 10px,
            rgba(255, 255, 255, 0.8) 20px);
}

.loader {
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}

.flashing {
    animation: flash 2s infinite;
}

@keyframes flash {

    0%,
    100% {
        opacity: 1;
    }

    10% {
        opacity: 0;
    }
}
</style>