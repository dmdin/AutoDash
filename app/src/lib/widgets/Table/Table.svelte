<script>
	import { CHART_HEIGHT, CHART_WIDTH } from '$root/lib/charts/constants';
	import DataTable from './DataTable.svelte';
	import { Body, HeadCell } from './RowBased';
	import Exports from './header/export/Exports.svelte';

	export let table = null;
	let columns, data;

	function getTableData(table) {
    const head = []
		const data = {}

		try {
      table?.categories?.forEach((c, i) => {
        head.push({ name: c })
        const row = table.rows.reduce((prev, cur) => {
          return [ ...prev, cur[i] ]
        }, [])

        if (!data[c]) data[c] = {}
        data[c] = row
      })
		} catch (e) {
			console.log(e);
		}

		return [head, data];
	}

	const rowHeight = 20;

	$: if (table) {
		[columns, data] = getTableData(table);
	}
</script>

{#if table}
	<div class="mb-1 mt-6" style:height="{CHART_HEIGHT}px">
		{#if columns && data}
			<DataTable {data} {columns} download {rowHeight}>
				<svelte:fragment slot="controlsTop">
					<Exports
						class="mb-[16px] flex h-full items-center justify-center border-0 bg-white p-[12px]"
					/>
				</svelte:fragment>

				<Body slot="table" class="max-h-[700px]">
					<tr slot="theadCells" let:head class="h-[50px]">
						{#each head as hc, i}
							<HeadCell
								index={i}
								head={hc}
								class="bg-base-300 p-1 text-center text-[14px] font-semibold text-[#0F172A]"
							/>
						{/each}
					</tr>
				</Body>
			</DataTable>
		{/if}
	</div>
{/if}
