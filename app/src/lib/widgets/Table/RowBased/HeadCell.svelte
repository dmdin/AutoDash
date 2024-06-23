<script lang="ts">
	import type { Writable } from 'svelte/store';
	import { SvelteComponent, createEventDispatcher, getContext } from 'svelte';

	import type { Controls, Head } from '../types';
	import { getRenderStore, getSortIndexes } from '../controller';

	export let head: Head | null = null;
	export let index = -1;
	export let disabled = false;
	export let isResizable = true;
	export const comparator = getSortIndexes;

	let self: HTMLTableCellElement | null = null;
	let box;
	const controls = getContext<Writable<Controls>>('controls');
	const dispatch = createEventDispatcher();
	const rendered = getRenderStore();
	let isPinned = false,
		pinnedStyle = '';
	let isResizing = false;

	$: if (head && $rendered.head[index] !== head) $rendered.head[index] = head;
	$: actualClass = $$restProps.class ?? 'bg-base-300 font-medium text-base-content/60';
	$: pinnedStyle = head!.isPinned ? `left: ${head?.offsetLeft}px; z-index: 21` : '';

	console.log();

	function handleSort(by) {
		if (by === $controls.sort.by) {
			$controls.sort.asc = !$controls.sort.asc;
		} else {
			$controls.sort = {
				by,
				asc: true
			};
		}
		dispatch('sort', $controls.sort);
	}
</script>

<th class="sticky top-0 z-20 border-r {actualClass}" style={pinnedStyle} bind:this={self}>
	<button
		disabled={!head || disabled}
		class="group flex w-full items-center gap-1 p-2 pr-0.5 transition-colors hover:text-base-content"
		on:click={() => handleSort(head?.name)}
	>
		{#if head}
			<span class=" truncate">{head.title ?? ''}</span>
			{#if head.sortable}
				<span class="text-base-content/40 transition-colors group-hover:text-base-content">
					{#if !disabled}
						{#if head.name === $controls.sort?.by && $controls.sort.asc}
							<!-- <ChevronUpIcon class="h-[16px]" /> -->
						{:else if head.name === $controls.sort?.by && !$controls.sort.asc}
							<!-- <ChevronDownIcon class="h-[16px]" /> -->
						{:else}
							<!-- <ChevronUpDown height="22" /> -->
						{/if}
					{/if}
				</span>
			{/if}
		{/if}
	</button>
</th>

<style lang="postcss">
	th:after,
	th:before {
		content: '';
		position: absolute;
		left: 0;
		width: 100%;
	}

	/* th:before {
    top: -1px;
    @apply border
  } */

	th:after {
		bottom: -1px;
		@apply border;
	}
</style>
