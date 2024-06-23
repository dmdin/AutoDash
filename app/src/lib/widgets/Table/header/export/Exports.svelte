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

<div class="dropdown dropdown-bottom z-[1000]">
	<div tabIndex={0} role="button" class="flex justify-end btn m-1 bg-secondary">Экспорт</div>
	<ul
		tabIndex={0}
		class="dropdown-content menu bg-base-100 rounded-box z-[1] p-2 shadow flex w-[150px] flex-col gap-2"
	>
		<h3 class="text-sm text-center text-base-content/90">Данные таблицы</h3>
		<div class="flex justify-center gap-2">
			<slot>
				<CSV />
				<Excel />
			</slot>
		</div>
	</ul>
</div>

