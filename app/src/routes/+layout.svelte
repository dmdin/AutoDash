<script lang="ts">
	import { onMount } from 'svelte';
	import { scale, fly } from 'svelte/transition';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { page } from '$app/stores';

	import Github from '~icons/devicon/github';
	import Google from '~icons/flat-color-icons/google';
	import Cancel from '~icons/iconoir/cancel';
	import Enter from '~icons/iconamoon/enter';
	import Exit from '~icons/iconamoon/exit';
	import Moon from '~icons/ph/moon';
	import Sun from '~icons/ph/sun';
	import Robot from '~icons/mdi/robot-outline';
	import Plus from '~icons/ic/round-plus';
	import { SignIn } from "@auth/sveltekit/components"

	import '../app.css';
	import { theme, model, avaliableModels, type Themes } from '$stores';
	import { showLayout } from './index';
	export let data;

	onMount(() => {
		const savedTheme = localStorage.getItem('theme') ?? 'light';
		theme.set(savedTheme as Themes);
	});
</script>

{#if $showLayout}
	<dialog id="signinModal" class="modal">
		<div class="modal-box !bg-base-100">
			<div class="border rounded-md border-neutral/40 flex flex-col">
				<form method="dialog" class="self-end p-2">
					<button class="btn btn-ghost btn-square btn-sm"><Cancel width="20" height="20" /></button>
				</form>

				<div class="w-fit self-center flex flex-col justify-between pb-10">
					<h1 class="text-2xl font-bold mb-5 text-neutral">Войти с помощью SSO</h1>
					<div class="flex flex-col gap-2">
						<button class="btn" on:click={() => signIn('github')}><Github /> GitHub</button>
						<button class="btn" on:click={signIn}>Войти при помощи email</button>						
						<!-- <SignIn provider="resend" /> -->
						<!-- <button class="btn" on:click={() => signIn('google')}><Google /> Google</button> -->
					</div>
				</div>
			</div>
		</div>
	</dialog>

	<div
		id="theme-root"
		data-theme={$theme}
		class="w-full h-full min-h-[100vh] flex flex-col transition-colors"
	>
		<header class="m-2 border-b border-neutral/10">
			<div class="navbar">
				<div class="flex-1 gap-10">
					<a
						href="/"
						class="p-0 btn btn-ghost bg-gradient-to-r from-accent to-secondary inline-block text-transparent bg-clip-text text-xl font-black"
						><i class="text-3xl">AutoDash</i></a
					>

					{#if $page.data.session}
						<div class="flex gap-6 p-2 px-8 rounded-xl">
							<a
								href="/dashboards"
								class:bg-primary={$page.url.href.endsWith('dashboards')}
								class:text-primary-content={$page.url.href.endsWith('dashboards')}
								class="rounded-md px-2 py-1 transition-colors"
							>
								Отчеты
							</a>

							<div class="tooltip tooltip-bottom" data-tip="Создать новый отчет">
								<a
									class:btn-primary={$page.url.href.endsWith('prompt')}
									class="btn btn-sm btn-square"
									href="/prompt"
								>
									<Plus />
								</a>
							</div>
						</div>
					{/if}
				</div>

				<div class="flex gap-4">
					<div class="tooltip tooltip-left" data-tip="Выбор LLM модели">
						<div
							class="flex items-center gap-3 bg-primary px-4 py-0.5 rounded-xl cursor-pointer text-primary-content"
						>
							<Robot width="30" height="30" />

							<select bind:value={$model} class="cursor-pointer bg-transparent w-full h-full">
								{#each avaliableModels as value}
									<option {value}>{value}</option>
								{/each}
							</select>
						</div>
					</div>
					<div class="tooltip tooltip-bottom" data-tip="Поменять тему">
						<button
							class="btn btn-square btn-sm flex items-center gap-4 transition hover:text-primary"
							on:click={() => ($theme = $theme === 'light' ? 'dark' : 'light')}
						>
							{#if $theme === 'light'}
								<span in:scale={{ duration: 300 }}>
									<Sun width="24" />
								</span>
							{:else}
								<span in:scale={{ duration: 300 }}>
									<Moon width="24" />
								</span>
							{/if}
						</button>
					</div>
					{#if !data.session}
						<button class="btn btn-primary btn-sm" onclick="signinModal.showModal()">
							<Enter />
							Войти
						</button>
					{:else}
						<div class="ml-7 flex gap-2">
							<div class="flex items-center gap-3">
								<div
									class="tooltip tooltip-left"
									data-tip={`${$page.data.session?.user?.name} - ${$page.data.session?.user?.email}`}
								>
									<div class="w-8 rounded-xl">
										<a href="/user">
											<img
												alt="User avatar"
												src={$page.data?.session?.user?.image ??
													'https://source.boringavatars.com/marble/120'}
												class="avatar rounded-md"
											/>
										</a>
									</div>
								</div>
								<button class="btn btn-outline btn-sm" on:click={() => signOut({ redirect: '/' })}>
									<Exit />
									Выйти
								</button>
							</div>
						</div>
					{/if}
				</div>
			</div>
		</header>

		<main class="grow h-full flex flex-col px-2">
			<slot />
		</main>

		<!--<footer class="footer items-center p-4 bg-neutral text-neutral-content">-->
		<!--  <aside class="items-center grid-flow-col">-->
		<!--    <svg width="36" height="36" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" clip-rule="evenodd" class="fill-current"><path d="M22.672 15.226l-2.432.811.841 2.515c.33 1.019-.209 2.127-1.23 2.456-1.15.325-2.148-.321-2.463-1.226l-.84-2.518-5.013 1.677.84 2.517c.391 1.203-.434 2.542-1.831 2.542-.88 0-1.601-.564-1.86-1.314l-.842-2.516-2.431.809c-1.135.328-2.145-.317-2.463-1.229-.329-1.018.211-2.127 1.231-2.456l2.432-.809-1.621-4.823-2.432.808c-1.355.384-2.558-.59-2.558-1.839 0-.817.509-1.582 1.327-1.846l2.433-.809-.842-2.515c-.33-1.02.211-2.129 1.232-2.458 1.02-.329 2.13.209 2.461 1.229l.842 2.515 5.011-1.677-.839-2.517c-.403-1.238.484-2.553 1.843-2.553.819 0 1.585.509 1.85 1.326l.841 2.517 2.431-.81c1.02-.33 2.131.211 2.461 1.229.332 1.018-.21 2.126-1.23 2.456l-2.433.809 1.622 4.823 2.433-.809c1.242-.401 2.557.484 2.557 1.838 0 .819-.51 1.583-1.328 1.847m-8.992-6.428l-5.01 1.675 1.619 4.828 5.011-1.674-1.62-4.829z"></path></svg> -->
		<!--    <p>Copyright © 2024 - All right reserved</p>-->
		<!--  </aside> -->
		<!--  <nav class="grid-flow-col gap-4 md:place-self-center md:justify-self-end">-->
		<!--    <a><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="fill-current"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"></path></svg>-->
		<!--    </a>-->
		<!--    <a><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="fill-current"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"></path></svg></a>-->
		<!--    <a><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="fill-current"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"></path></svg></a>-->
		<!--  </nav>-->
		<!--</footer>-->
	</div>
{:else}
	<slot />
{/if}


<style>
	:global(.signInButton) {
		@apply btn
	}

	:global(#input-email-for-email-provider) {
		@apply input input-bordered input-sm
	}
</style>