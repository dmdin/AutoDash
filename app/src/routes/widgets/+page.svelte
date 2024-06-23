<script lang="ts">
	import Table from '$root/lib/widgets/Table/Table.svelte';

	// import Table from '$root/lib/widgets/Table/Table.svelte';
	import { Chart } from '../../lib/charts';
	import { ChartType } from '../../lib/charts/types';
	import Badge from '../../lib/widgets/Badge.svelte';
	import { BADGES } from './constants';

	const barChart = {
		type: 'table',
		title: '',
		categories: ['Название компании', 'Доля на рынке', 'Продажи'],
		rows: [
			['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
			['HOWO', '4.3', '6900'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
      ['KAMAZ', '21.5', '31010'],
			['SITRAK', '16.4', '23633'],
			['SHACMAN', '14.4', '20760'],
			['FAW', '11', '15804'],
		]
	};
</script>

<div
	class="w-10/12 h-[24vh] flex justify-between items-start flex-shrink-0 p-x-24 m-auto flex-wrap"
>
	{#each BADGES as badge, i}
		<Badge class={i % 2 ? 'bg-primary' : 'bg-secondary'} {...badge} />
	{/each}
	<!-- <Chart chart={barChart} /> -->
	<Table table={barChart} />
</div>
