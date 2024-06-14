<script lang="ts">
	import Badge from '$lib/widgets/Badge.svelte';
	import PieChart from '$lib/widgets/PieChart/PieChart.svelte';
	import { BADGES } from './constants';
</script>

<div class="w-10/12 h-[24vh] flex justify-between items-start flex-shrink-0 p-x-24 m-auto">
	{#each BADGES as badge,i}
		<Badge class="{i % 2 ? 'bg-primary' : 'bg-secondary'}" {...badge} />
	{/each}
</div>

<PieChart />
