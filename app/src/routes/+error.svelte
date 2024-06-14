<script>
	import { page } from '$app/stores';
	import { browser } from '$app/environment';
	import { LottiePlayer } from '@lottiefiles/svelte-lottie-player';

	let animation =
		$page.status === 404 ? '/animations/emoji-thinking.json' : '/animations/emoji-explosion.json';
	let title = $page.status === 404 ? 'Страница не найдена' : 'Произошла страшная ошибка!';
</script>

<div class="grow grid place-content-center place-items-center">
	{#if browser}
		<div class="flex flex-col items-center mb-40">
			<LottiePlayer
				src={animation}
				autoplay={true}
				loop={true}
				renderer="svg"
				background="transparent"
				width="500"
				speed="0.5"
			/>
			<h1 class="font-black text-4xl">{title}</h1>
		</div>
	{/if}
</div>
