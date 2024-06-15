<script lang="ts">
	import { scale, fly } from 'svelte/transition'

	import Dice from '~icons/fad/random-1dice';
	import Spark from '~icons/streamline/ai-generate-variation-spark';

	function randomTopic(params: type) {
		topic = 'Отчет по рынку BI систем';
	}

	let topic = '';
</script>

<div
	in:fly={{x: 50}}
	class="self-center grow mt-2 w-full max-h-[90vh] border border-neutral/40 rounded-md p-5 max-w-4xl"
>
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

	<div class="w-full flex justify-between pr-1.5 items-center">
		<select class="mt-4 select select-bordered w-full max-w-xs text-md">
			<option disabled selected>Шаблон не выбран</option>
			<option>Han Solo</option>
			<option>Greedo</option>
		</select>

		<div class="tooltip" data-tip="Сгенерировать шаблон под тему">
			<button class="btn btn-sm btn-square btn-secondary text-center">
				<Spark height="25" />
			</button>
		</div>
	</div>

	<textarea
		placeholder="Подробное описание плана отчета"
		class="mt-4 textarea textarea-bordered textarea-md w-full min-h-[500px]"
	></textarea>
</div>
