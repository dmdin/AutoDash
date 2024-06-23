<script lang="ts">
	import Table from '$root/lib/widgets/Table/Table.svelte';

	// import Table from '$root/lib/widgets/Table/Table.svelte';
	import { Chart } from '../../lib/charts';
	import Badge from '../../lib/widgets/Badge.svelte';
	import { BADGES } from './constants';

	const barChart = {
		type: 'pie',
		title: 'Объем рынка смартфонов',
		categories: ['2020', '2021', '2022', '2023', '2024'],
		data: [800, 1400, 1450, 1300, 1500]
	};
</script>

<div
	class="w-10/12 h-[24vh] flex justify-between items-start flex-shrink-0 p-x-24 m-auto flex-wrap"
>
	{#each BADGES as badge, i}
		<Badge class={i % 2 ? 'bg-primary' : 'bg-secondary'} {...badge} />
	{/each}
	<Chart chart={barChart} />
	<!-- <Table table={barChart} /> -->
</div>
