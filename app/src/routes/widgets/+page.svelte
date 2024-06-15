<script lang="ts">
	import { Chart } from '../../lib/charts';
	import { ChartType } from '../../lib/charts/types';
	import Badge from '../../lib/widgets/Badge.svelte';
	import { BADGES } from './constants';


  const chart = {
    title: 'Hello',
    subtitle: '',
    type: ChartType.Custom,
  }

  setTimeout(() => {
    chart.type = ChartType.Pie
  }, 3000)
</script>

<div class="w-10/12 h-[24vh] flex justify-between items-start flex-shrink-0 p-x-24 m-auto flex-wrap">
	{#each BADGES as badge,i}
		<Badge class="{i % 2 ? 'bg-primary' : 'bg-secondary'}" {...badge} />
	{/each}
  <Chart {chart} />
</div>
