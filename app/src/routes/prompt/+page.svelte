<script lang="ts">
	import { onMount, onDestroy, beforeUpdate, afterUpdate, tick } from 'svelte';
	import { Circle } from 'svelte-loading-spinners';
	import { scale, fly, fade } from 'svelte/transition';

	import { env } from '$env/dynamic/public';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import Dice from '~icons/fad/random-1dice';
	import Spark from '~icons/streamline/ai-generate-variation-spark';
	import Play from '~icons/solar/play-broken';
	import Save from '~icons/material-symbols/save-outline';
	import MagnifyingGlass from '~icons/heroicons/magnifying-glass-plus-20-solid';

	import { rpc } from '$root/routes';
	import { model } from '$client/stores/index.js';

	import { topics } from './topics';
	import Combobox from './Combobox.svelte';

	export let data;

	let templates = data.templates;
	let sources = data.sources;
	console.log(sources)
	let template;
	let topic = '';
	let description = '';
	let templateName = '';
	let ws: WebSocket;
	let textarea: HTMLTextAreaElement;
	let autoscroll = false;
	let loading = false;
	let generating = false;
	let selectedSources = sources;

	let sourceTemplate = {
		title: '',
		link: '',
	}
	let newSource = {...sourceTemplate}


	let receiveTimeout;

	$: selectTemplate(template);
	beforeUpdate(() => {
		if (textarea) {
			const scrollableDistance = textarea.scrollHeight - textarea.offsetHeight;
			autoscroll = textarea.scrollTop > scrollableDistance - 20;
		}
	});

	afterUpdate(() => {
		if (autoscroll) {
			textarea.scrollTo(0, textarea.scrollHeight);
		}
	});

	onDestroy(() => {
		// ws.close()
	});
	onMount(async () => {
		ws = new WebSocket(env.PUBLIC_CHAT_ENDPOINT);
		ws.onopen = function () {
			console.log('Соединение установлено.');
		};

		ws.onmessage = function (event) {
			clearInterval(receiveTimeout);

			receiveTimeout = setTimeout(() => {
				generating = false;
			}, 3000);
			description += event.data;
		};
	});

	function generateTemplate() {
		generating = true;
		description += '';
		ws.send(JSON.stringify({ input_theme: topic, model_name: $model }));
	}

	async function generateDashboard() {
		loading = true;
		await rpc.Prompt.createDashboard(topic, description, selectedSources.map(s => s.link)).then((dashboard) => {
			window.location.href = '/dashboards/' + dashboard.id;
		});
		loading = false;
	}

	function randomTopic() {
		const index = Math.floor(Math.random() * topics.length);
		topic = topics[index];
	}

	async function selectTemplate(template) {
		if (!template?.body) return;
		description = template.body;
	}

	async function createTemplate() {
		const newTemplate = await rpc.Prompt.saveTemplate({ title: templateName, body: description });
		templates = templates.concat(newTemplate);
		templateName = '';
	}

	async function addSource() {
		sources = sources.concat(await rpc.Prompt.addSource(newSource))
		newSource = {...sourceTemplate}
	}
</script>

<div in:fade class="self-center grow mt-2 w-full border border-neutral/40 rounded-md p-5 max-w-4xl">
	<h1 class="text-2xl font-[600] mb-4">План отчета:</h1>
	<label class="input input-bordered flex items-center gap-2 pr-1.5 text-md">
		Тема:
		<input
			bind:value={topic}
			class="grow"
			type="text"
			placeholder="Отчет по состоянию российского рынка эквайринга"
		/>
		<div class="tooltip" data-tip="Случайная тема">
			<button class="btn btn-sm btn-square btn-accent" on:click={randomTopic}>
				<Dice width="25" height="25" />
			</button>
		</div>
	</label>

	<div class="w-full flex justify-between pr-1.5 items-center mt-4">
		<div class="flex gap-5">
			<select
				class=" select select-bordered w-full max-w-xs text-md"
				on:change={selectTemplate}
				bind:value={template}
			>
				{#each templates as template}
					<option value={template}>{template.title}</option>
				{/each}
				<option disabled selected>Шаблон не выбран</option>
			</select>
			<Combobox
				bind:value={selectedSources}
				options={sources}
				extractor={(o) => o.title}
				placeholder="Источники информации"
			/>
			<div>
				<div class="tooltip" data-tip="Добавить новый источник">
					<button class="btn btn-primary btn-square" onclick="addSource.showModal()">
						<MagnifyingGlass width="20" height="20" />
					</button>
				</div>
			</div>
		</div>
		<div class="tooltip" data-tip="Сгенерировать шаблон под тему">
			<button
				disabled={!topic || generating}
				class="btn btn-sm btn-square btn-success text-center"
				on:click={generateTemplate}
			>
				<Spark height="25" />
			</button>
		</div>
	</div>

	<textarea
		bind:this={textarea}
		placeholder="Подробное описание плана отчета"
		class="mt-4 textarea textarea-bordered textarea-md w-full min-h-[500px]"
		bind:value={description}
	></textarea>

	<div class="flex gap-5">
		<button
			class="self-end btn text-md btn-primary mt-4"
			disabled={loading}
			on:click={generateDashboard}
		>
			{#if loading}
				<Circle size="20" />
			{:else}
				<Play />
			{/if}
			Сгенерировать отчет
		</button>

		<button class="self-end btn text-md btn-secondary mt-4" onclick="saveTemplateModal.showModal()">
			<Save width="20" height="20" />
			Сохранить шаблон
		</button>
	</div>
</div>

<dialog id="saveTemplateModal" class="modal">
	<div class="modal-box flex flex-col gap-4">
		<h3 class="font-bold text-lg text-neutral">Создать новый шаблон</h3>
		<label class="form-control w-full">
			<div class="label">
				<span class="label-text">Название шаблона</span>
			</div>
			<input
				type="text"
				placeholder="Новый шаблон"
				class="input input-bordered w-full"
				bind:value={templateName}
			/>
		</label>

		<div class="modal-action">
			<form method="dialog">
				<!-- if there is a button in form, it will close the modal -->
				<button class="btn btn-outline">Отмена</button>
				<button class="btn btn-primary  ml-4" on:click={createTemplate}>Сохранить</button>
			</form>
		</div>
	</div>
</dialog>

<dialog id="addSource" class="modal">
	<div class="modal-box flex flex-col gap-4">
		<h3 class="font-bold text-lg text-neutral">Добавить новый источник</h3>
		<label class="form-control w-full">
			<div class="label">
				<span class="label-text">Название источника</span>
			</div>
			<input
				type="text"
				placeholder="RBC"
				class="input input-bordered w-full"
				bind:value={newSource.title}
			/>
		</label>
		<label class="form-control w-full">
			<div class="label">
				<span class="label-text">Ссылка на источник</span>
			</div>
			<input
				type="text"
				placeholder="https://www.rbc.ru/"
				class="input input-bordered w-full"
				bind:value={newSource.link}
			/>
		</label>
		<div class="modal-action">
			<form method="dialog">
				<!-- if there is a button in form, it will close the modal -->
				<button class="btn btn-outline">Отмена</button>
				<button class="btn btn-primary ml-4" on:click={addSource} disabled={!newSource.link || !newSource.title}>Сохранить</button>
			</form>
		</div>
	</div>
</dialog>
