<script lang="ts">
	import { SvelteComponent, getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import { ColumnTypes, type Head, type Cell } from '../types';
	import { getRenderStore } from '../controller';

	export let value: any = null;
	export let head: Head | null = null;
	export let precision: number | null | undefined = null;
	export let autoSelect = true;
  const MAIN_LOCALE = "RU-ru"

	const tooltipBoxComponent = getContext<Writable<SvelteComponent | null>>('tooltipBoxComponent');
	let pinnedStyle = '';
	// const index = getContext('index')

	const rendered = getRenderStore();

	precision = precision ?? $rendered.config.precision[head?.unit ?? 0];

	$: {
		if (head?.type === ColumnTypes.Number) {
			const rounded = value;
			if (!Number.isNaN(rounded)) value = rounded;
		}
		if (head?.type === ColumnTypes.Number && value)
			value = value
				.toLocaleString(MAIN_LOCALE, {
					minimumFractionDigits: precision,
					maximumFractionDigits: precision
				})
				.replaceAll('\u00a0', ' '); // White spaces are different in chrome
		// if (column?.unit) console.log(column.unit, value)
		if (head?.unit && value) value = value + ' ' + head.unit;
		if ((value === null || value === undefined) && head && !$$slots.default) value = '—';
	}

	$: if (head?.isPinned) {
		pinnedStyle = `left: ${head.offsetLeft}px`;
	} else {
		pinnedStyle = '';
	}

	function selectCell(e) {
		if (!autoSelect) return;
		const range = document.createRange();
		range.selectNodeContents(e.target);
		const sel = window.getSelection()!;
		sel.removeAllRanges();
		sel.addRange(range);
	}
</script>

{#if head && !head.isPinned}
	<td
		class="border-x border-base-200/80 transition-colors hover:bg-info/5 {$$restProps.class} {head?.type ===
		ColumnTypes.Number
			? 'text-right'
			: ''} "
		on:click={selectCell}
	>
		{#if !$$slots.default}
			{value}
			<!-- {cellConfig?.class} {$$restProps.class} -->
		{:else}
			<div
				class="
      truncate px-1 text-xs tabular-nums text-neutral {$$restProps.class}
      "
			>
				<!-- {cellConfig?.class} {$$restProps.class} -->
				<slot />
			</div>
		{/if}
	</td>
{/if}
