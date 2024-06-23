<script lang="ts">
  import {fade} from 'svelte/transition'
  import Person from '~icons/material-symbols/person-outline';
  import Email from '~icons/ic/outline-email';
	export let data;

	const user = data.session?.user;
</script>

<div in:fade class="self-center mt-2 w-full border-neutral/40 rounded-2xl p-5 max-w-4xl bg-base-300">
	<h1 class="text-2xl font-[600] mb-4">Мой профиль:</h1>

	{#if !user}
		<h1>Вы не авторизованы!</h1>
	{:else}
		<!-- <p>{JSON.stringify(data)}</p> -->
		<div class="flex gap-10 mt-5">
			<div class="avatar">
				<div class="w-[150px]">
					<img
						alt="User avatar"
						src={user.image ?? 'https://source.boringavatars.com/marble/120'}
						class="avatar rounded-md"
					/>
				</div>
			</div>
			<div class="flex flex-col gap-4">
				<h2 class="flex items-center items-center gap-2 text-base-content text-xl font-[600] flex"><Person class="text-xl" />{user.name}</h2>
				<h2 class="items-center gap-2 text-base-content/90 text-xl font-[600] flex"><Email/>{user.email}</h2>
			</div>
		</div>
	{/if}
</div>
