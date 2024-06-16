<script lang="ts">
  import {fade} from 'svelte/transition'
  import Person from '~icons/material-symbols/person-outline';
  import Email from '~icons/ic/outline-email';
	export let data;

	const user = data.session?.user;
</script>

<div in:fade class="self-center mt-2 w-full border border-neutral/40 rounded-md p-5 max-w-4xl">
	<h1 class="text-2xl font-[600] mb-4">Мой профиль:</h1>

	{#if !user}
		<h1>Вы не авторизованы!</h1>
	{:else}
		<!-- <p>{JSON.stringify(data)}</p> -->
		<div class="flex gap-10 mt-5">
			<div class="avatar">
				<div class="w-[150px] rounded-xl">
					<img
						alt="User avatar"
						src={user.image ?? 'https://source.boringavatars.com/marble/120'}
						class="avatar"
					/>
				</div>
			</div>
			<div class="flex flex-col gap-4">
				<h2 class="items-center gap-2 text-base-content text-2xl font-[600] flex"><Person/>{user.name}</h2>
				<h2 class="items-center gap-2 text-base-content/90 text-2xl font-[600] flex"><Email/>{user.email}</h2>
			</div>
		</div>
	{/if}
</div>
