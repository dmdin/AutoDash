<script lang="ts">
	import { setContext, getContext, onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { createVirtualizer } from '@tanstack/svelte-virtual';

	import type {
		Head,
		Controls,
		RowsConfig,
		ColumnsConfig,
		DataConfig,
		Cell as ICell
	} from '../types';
	import { createStores, getRenderStore, renderTable } from '../controller';

	import HeadCell from './HeadCell.svelte';
	import Row from './Row.svelte';
	import Cell from './Cell.svelte';

	const rendered = getRenderStore();
	let virtualListEl: HTMLDivElement;

	function extractRow(index): { head: Head; value: ICell }[] {
		return $rendered.head.map((c) => {
			return { head: c, value: $rendered.body[c.name]![index]! };
		});
	}

	function extractConfig(index) {
		return $rendered.config.rows[index];
	}

	$: virtualizer = createVirtualizer<HTMLDivElement, HTMLTableRowElement>({
		count: $rendered.length,
		getScrollElement: () => virtualListEl,
		estimateSize: () => $rendered.config.rowHeight,
		overscan: 20
	});

	function handleCopy(e) {
		const selection = document.getSelection();
		if (!selection) return;

		if (!parseFloat(selection.toString())) return;

		const text = selection.toString().replaceAll(' ', '');
		e.clipboardData.setData('text/plain', text);
		e.preventDefault();
	}

  $: console.log($virtualizer.getVirtualItems())
</script>

<div
	on:copy={handleCopy}
	bind:this={virtualListEl}
	class="
    h-full w-full overflow-auto rounded-xl border border-base-200 bg-base-300 pb-4
    {$rendered.config.scrollbar}
    {$$restProps.class}
  "
>
	<div class="w-full" style="height: {$virtualizer.getTotalSize() + $rendered.config.rowHeight}px;">
		<table class="w-full table-fixed border-collapse p-2 text-xs">
			<slot name="thead">
				<thead
					class="relative z-[100] rounded-md text-center text-base-content/70 after:border-b-2"
				>
					<slot name="theadCells" head={$rendered.head}>
						<tr>
							<!-- {#if $rendered.config.enumerate}
                <HeadCell index={0} class="text-right" head={enumHead} />
              {/if} -->
							{#each $rendered.head as head, i}
								<HeadCell index={i} {head} />
							{/each}
						</tr>
					</slot>
				</thead>
			</slot>
			<slot name="colgroup" head={$rendered.head}>
				<colgroup>
					<!-- {#if $rendered.config.enumerate}
            <col style="" class="w-12" />
          {/if} -->
					{#each $rendered.head as head, i (`${head.name}_${i}`)}
						<col style="width: {head.width ? `${head.width}px` : 'auto'}" />
					{/each}
				</colgroup>
			</slot>
			<tbody class="w-full">
				<slot name="start" rendered={$rendered} />
				{#each $virtualizer.getVirtualItems() as r, idx (r.index)}
					{@const index = $rendered.sortIndex[r.index]}
					<!-- {#each $rendered.sortIndex as index, i} -->
					{@const row = extractRow(index)}
					{@const config = extractConfig(index)}
					{@const style = `
            height: ${r.size}px;
            transform: translateY(${r.start - idx * r.size}px);`}
					<slot name="row" {row} {index} rendered={$rendered} {enumHead} {style}>
						<Row virtualIndex={r.index} {config} {style}>
							<!-- {#if $rendered.config.enumerate}
                <Cell class="text-right" head={enumHead} value={r.index + 1} />
              {/if} -->
							<slot name="cells" {row} {config} {index} rendered={$rendered}>
								{#each row as cell, i}
									<Cell {...cell} {config} />
								{/each}
							</slot>
						</Row>
					</slot>
				{/each}
				<slot name="end" rendered={$rendered} />
			</tbody>
		</table>
	</div>
</div>
