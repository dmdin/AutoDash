<script lang="ts">
	import { getContext, onMount, setContext } from 'svelte';
	import { writable } from 'svelte/store';
	import { twMerge } from 'tailwind-merge';
	import ArrowDownTray from '~icons/heroicons/arrow-down-tray';
	import { melt } from '@melt-ui/svelte';

	import { getRenderStore } from '../../controller';
	import type { Rendered } from '../../types';

	import CSV from './CSV.svelte';
	import Excel from './Excel.svelte';

	const rendered = getRenderStore();

	export let data: Rendered | null = null;

	const exportData = writable<Rendered>();
	$: $exportData = data ?? $rendered;

	setContext('export', exportData);

	let popover;
</script>

<!-- <div slot="trigger" let:trigger let:open>
	<slot name="button" {open} {trigger}>
		<button
			class={twMerge('btn btn-sm text-xs', $$restProps.class)}
			use:melt={trigger}
			aria-label="Открыть меню"
			on:click={() => open.set(true)}
		>
			<ArrowDownTray />Экспорт данных
		</button>
	</slot>
</div> -->

<div class="flex w-[150px] flex-col gap-2">
	<h3 class="text-sm text-base-content/90">Данные таблицы</h3>
	<div class="flex gap-2">
		<slot>
			<CSV />
			<Excel />
		</slot>
	</div>
</div>
