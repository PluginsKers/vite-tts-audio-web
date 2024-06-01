<template>
    <div class="flex flex-col lg:flex-row justify-start items-center lg:justify-center h-screen p-4 gap-6">
        <div class=" flex-grow-0 flex flex-col items-center justify-center w-full gap-4 px-4"
            :class="{ 'lg:border-r-2 lg:border-dashed lg:border-gray-300': !isLoading && audioUrl }">
            <h1 class="relative text-4xl flex flex-row items-center justify-center flex-wrap">
                <svg t="1717244450571" class="mb-[-6px] mr-1" viewBox="0 0 1024 1024" version="1.1"
                    xmlns="http://www.w3.org/2000/svg" p-id="8317" width="32" height="32">
                    <path
                        d="M577.641026 91.897436 577.641026 590.769231 433.230769 590.769231 433.230769 91.897436 577.641026 91.897436ZM341.333333 610.571054C341.333333 650.318585 373.656418 682.666667 413.474002 682.666667L597.397793 682.666667C637.229686 682.666667 669.538462 650.406676 669.538462 610.571054L669.538462 72.095613C669.538462 32.348081 637.215376 0 597.397793 0L413.474002 0C373.642109 0 341.333333 32.259991 341.333333 72.095613L341.333333 610.571054ZM760.62615 617.003113C760.348488 682.270116 707.346905 735.179487 641.89335 735.179487L380.794092 735.179487C315.497551 735.179487 262.564103 682.319623 262.564103 617.003113L262.564103 426.666667C262.564103 401.289886 241.992205 380.717949 216.615385 380.717949 191.238564 380.717949 170.666667 401.289886 170.666667 426.666667L170.666667 643.278494C170.666667 744.787561 253.012152 827.076923 354.506831 827.076923L669.493169 827.076923C771.025264 827.076923 853.333333 744.839562 853.333333 643.278494L853.333333 426.666667C853.333333 401.289886 832.761436 380.717949 807.384615 380.717949 782.007795 380.717949 761.435897 401.289886 761.435897 426.666667L760.62615 617.003113ZM479.179487 925.538462 249.360279 925.538462C224.016673 925.538462 203.487179 946.110398 203.487179 971.487179 203.487179 996.812314 224.025206 1017.435897 249.360279 1017.435897L774.639721 1017.435897C799.983327 1017.435897 820.512821 996.863961 820.512821 971.487179 820.512821 946.162045 799.974794 925.538462 774.639721 925.538462L571.076923 925.538462 571.076923 892.685325C571.076923 867.282051 550.505026 846.769231 525.128205 846.769231 499.80311 846.769231 479.179487 867.326569 479.179487 892.685325L479.179487 925.538462Z"
                        fill="#000" p-id="8318"></path>
                </svg>
                ChatTTS语音生成
            </h1>
            <div class="relative w-full max-w-lg">
                <textarea v-model="text"
                    class="relative w-full h-full p-2 border-0 outline-none rounded-md shadow-md focus:ring-4 focus:ring-gray-100"
                    rows="5"
                    :class="{ 'text-gray-500 loader-stripes cursor-not-allowed': isLoading, 'bg-gray-50 focus:bg-white': !isLoading }"
                    :disabled="isLoading">
                </textarea>
            </div>

            <div @click="convertTextToSpeech"
                class="flex items-center justify-center bg-gray-900 hover:bg-gray-800 text-white px-2 py-1 h-10 rounded-md shadow-md w-full max-w-lg"
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
        <div v-if="!isLoading && audioUrl" class="w-full min-w-[20vw]">
            <transition name="fade" mode="out-in">
                <div key="audio" class="flex flex-col w-full items-center justify-center">
                    <audio ref="audio" class="w-full max-w-lg" controls :src="audioUrl"></audio>
                    <div @click="reset"
                        class="flex items-center justify-center cursor-pointer bg-red-700 hover:bg-red-700/90 text-white p-2 rounded-md shadow-md mt-4 h-10 max-w-lg w-full">
                        重新生成?
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const text = ref('')
const audioUrl = ref<string | null>(null)
const isLoading = ref(false)
const errorMessage = ref<string | null>(null)

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
            body: JSON.stringify({ text: text.value }),
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

const reset = () => {
    audioUrl.value = null;
    convertTextToSpeech();
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
</style>
