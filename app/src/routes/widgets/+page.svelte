<script lang="ts">
	import { Chart } from '../../lib/charts';
	import { ChartType } from '../../lib/charts/types';
	import Badge from '../../lib/widgets/Badge.svelte';
	import { BADGES } from './constants';

	const barChart = {
		type: 'bar',
		title: 'Smartphone Revenue Growth Q1 2024',
		subtitle: 'Year-on-Year Revenue Growth by Vendor',
		category: ['Samsung', 'Apple', 'Xiaomi', 'TRANSSION', 'OPPO'],
		series: [
			{
				name: 'Revenue Growth',
				unit: '%',
				data: [
					{ name: 'Samsung', value: 5 },
					{ name: 'Apple', value: 21 },
					{ name: 'Xiaomi', value: 33 },
					{ name: 'TRANSSION', value: 86 },
					{ name: 'OPPO', value: 10 }
				]
			}
		]
	};

	// setTimeout(() => {
	//   barChart.type = 'bar'
	// }, 3000)

	// setTimeout(() => {
	//   barChart.type = 'line'
	// }, 7000)
</script>

<div
	class="w-10/12 h-[24vh] flex justify-between items-start flex-shrink-0 p-x-24 m-auto flex-wrap"
>
	{#each BADGES as badge, i}
		<Badge class={i % 2 ? 'bg-primary' : 'bg-secondary'} {...badge} />
	{/each}
	<Chart chart={barChart} />
</div>
