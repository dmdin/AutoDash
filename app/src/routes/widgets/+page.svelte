<script lang="ts">
	import { Chart } from '../../lib/charts';
	import { ChartType } from '../../lib/charts/types';
	import Badge from '../../lib/widgets/Badge.svelte';
	import { BADGES } from './constants';

	const barChart = {
		title: 'Traffic by Device',
		subtitle: '',
		type: 'pie',
		categories: null,
		series: [
			{
				name: '',
				unit: '',
				data: [
					{
						name: 'Linux',
						value: '10000000'
					},
					{
						name: 'Mac',
						value: '21000000'
					},
					{
						name: 'IOS',
						value: '20500000'
					},
					{
						name: 'Windows',
						value: '25000000'
					},
					{
						name: 'Android',
						value: '10000000'
					},
					{
						name: 'Other',
						value: '22000000'
					}
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
