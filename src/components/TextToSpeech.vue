<template>
	<div
		class="flex flex-col lg:flex-row justify-center items-center h-screen p-4 gap-6 bg-gray-200"
	>
		<div
			class="flex-grow-0 flex flex-col items-center justify-center w-full max-w-lg gap-4 px-4"
			:class="{
				'lg:border-r-2 lg:border-dashed lg:border-gray-300':
					!isLoading && audioUrl,
			}"
		>
			<div
				class="relative text-4xl flex h-7 flex-row items-center justify-center"
			>
				<div
					class="pulse-animation relative w-7 h-7 rounded-full bg-black"
					:class="{ 'mr-2': displayText }"
				></div>
				<span v-if="displayText" class="typing-effect">{{
					displayText
				}}</span>
			</div>
			<div class="relative w-full">
				<textarea
					v-model="text"
					class="relative w-full h-full p-2 border-0 outline-none rounded shadow-md min-h-10 max-h-[50vh] focus:ring-4 focus:ring-gray-100 transition-all duration-300"
					placeholder="输入你要转换的文本"
					rows="5"
					:class="{
						'text-gray-500 bg-gray-100 cursor-not-allowed':
							isLoading,
						'bg-gray-50 focus:bg-white': !isLoading,
					}"
					:disabled="isLoading"
				>
				</textarea>
			</div>

			<div
				@click="convertTextToSpeech"
				class="flex items-center justify-center bg-gray-900 hover:bg-gray-800 text-white px-2 py-1 h-10 rounded shadow-md w-full select-none transition-colors duration-300"
				:class="{
					'cursor-not-allowed opacity-50': isLoading,
					'cursor-pointer': !isLoading,
				}"
				:disabled="isLoading"
			>
				<div
					v-if="isLoading"
					key="loading"
					class="flex items-center justify-center"
				>
					<div
						class="loader ease-linear rounded-full border-2 border-t-2 border-gray-200 h-6 w-6"
					></div>
				</div>
				<div v-else class="text-md">点击生成</div>
			</div>
		</div>
		<div v-if="!isLoading && audioUrl" class="w-full max-w-lg gap-4 px-4">
			<transition name="fade" mode="out-in">
				<div
					key="audio"
					class="flex flex-col w-full items-center justify-center animate-slide-up"
				>
					<AudioPlayer :audioUrl="audioUrl" />
				</div>
			</transition>
		</div>
	</div>
	<transition
		enter-active-class="transition-all duration-300 ease-out"
		enter-from-class="translate-y-full opacity-0"
		enter-to-class="translate-y-0 opacity-100"
		leave-active-class="transition-all duration-300 ease-in"
		leave-from-class="translate-y-0 opacity-100"
		leave-to-class="translate-y-full opacity-0"
	>
		<div
			v-if="errorMessage"
			class="fixed bottom-0 left-0 right-0 bg-red-500 text-white p-4 shadow-lg"
		>
			<div class="container mx-auto flex justify-between items-center">
				<span>{{ errorMessage }}</span>
				<button
					@click="closeErrorDrawer"
					class="text-white hover:text-gray-200"
				>
					<svg
						class="w-6 h-6"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
						xmlns="http://www.w3.org/2000/svg"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						></path>
					</svg>
				</button>
			</div>
		</div>
	</transition>
</template>

<script lang="ts" setup>
	import { ref, onMounted } from "vue";
	import AudioPlayer from "./AudioPlayer.vue";

	const text = ref("");
	const audioUrl = ref<string | null>(null);
	const isLoading = ref(false);
	const errorMessage = ref<string | null>(null);
	const fullText = "ChatTTS语音生成";
	const displayText = ref("");
	let currentIndex = 0;
	let isDeleting = false;

	interface Conversion {
		target: string;
		replacement: string;
	}

	const escapeRegExp = (string: string): string => {
		return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
	};

	const convertTextFormat = (text: string): string => {
		const conversions: Conversion[] = [
			{ target: "，", replacement: "," },
			{ target: ".", replacement: " [uv_break] " },
			{ target: ",", replacement: " [uv_break] " },
			{ target: "。", replacement: " [uv_break] " },
			{ target: "+", replacement: " [uv_break] " },
		];

		let convertedText = text;
		conversions.forEach((conversion) => {
			const regex = new RegExp(escapeRegExp(conversion.target), "g");
			convertedText = convertedText.replace(
				regex,
				conversion.replacement
			);
		});

		return convertedText;
	};

	const convertTextToSpeech = async () => {
		if (!text.value || isLoading.value) return;
		if (text.value.length < 6) {
			errorMessage.value = "输入内容过少，必须至少包含6个字符。";
			return;
		}

		isLoading.value = true;
		errorMessage.value = null;

		try {
			const response = await fetch(
				`${import.meta.env.VITE_API_BASE_URL}/tts`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						text: convertTextFormat(text.value),
					}),
				}
			);

			if (!response.ok) {
				if (response.status === 400) {
					const errorData = await response.json();
					throw new Error(errorData.error);
				}
				throw new Error("Network response was not ok");
			}

			const blob = await response.blob();
			const url = URL.createObjectURL(blob);
			audioUrl.value = url;
		} catch (error) {
			console.error("Error:", error);
			errorMessage.value = (error as Error).message;
		} finally {
			isLoading.value = false;
		}
	};

	const closeErrorDrawer = () => {
		errorMessage.value = null;
	};

	const typeText = () => {
		const speed = 150;
		const deleteSpeed = 50;
		const pauseBeforeDelete = 2000;
		const pauseBeforeType = 500;

		if (!isDeleting && currentIndex < fullText.length) {
			displayText.value = fullText.slice(0, currentIndex + 1);
			currentIndex++;
			setTimeout(typeText, speed);
		} else if (!isDeleting && currentIndex === fullText.length) {
			setTimeout(() => {
				isDeleting = true;
				typeText();
			}, pauseBeforeDelete);
		} else if (isDeleting && currentIndex > 0) {
			displayText.value = fullText.slice(0, currentIndex - 1);
			currentIndex--;
			setTimeout(typeText, deleteSpeed);
		} else if (isDeleting && currentIndex === 0) {
			isDeleting = false;
			setTimeout(typeText, pauseBeforeType);
		}
	};

	onMounted(() => {
		typeText();
	});

	defineProps({
		class: {
			type: String,
			default: "",
		},
	});
</script>

<style scoped>
	.loader {
		border-top-color: #ffffff;
		animation: spin 1s linear infinite;
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
		transition: opacity 0.3s ease;
	}

	.fade-enter-from,
	.fade-leave-to {
		opacity: 0;
	}

	.pulse-animation {
		animation: pulse 2s infinite;
	}

	@keyframes pulse {
		0% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.1);
		}
		100% {
			transform: scale(1);
		}
	}

	.animate-slide-up {
		animation: slideUp 0.5s ease-out;
	}

	@keyframes slideUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.typing-effect::after {
		content: "|";
		animation: blink 0.7s infinite;
	}

	@keyframes blink {
		0%,
		100% {
			opacity: 0;
		}
		50% {
			opacity: 1;
		}
	}
</style>
