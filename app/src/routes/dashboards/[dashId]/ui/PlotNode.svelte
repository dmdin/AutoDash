<script lang="ts">
	import { PieChart, Chart } from '$lib/charts';
	import { ChartType } from '$lib/charts/types';
	import { rpc } from '$root/routes';
	import GgChart from '~icons/gg/chart';
	import LucideLineChart from '~icons/lucide/line-chart';
	import MageChartFill from '~icons/mage/chart-fill';
	import { dashboard, nodes, readonly } from '../controller';
	import { getContext } from 'svelte';

	export let id
	export let data: {
		data: object;
		name: string;
		id: string;
    order: number;
	};
	let type = data.data.type;
	export let selected;

	async function changePlot(type) {
		data.data.type = type;
		await rpc.Dashboard.updateWidget(data.id, { data: data.data });
	}

  const node = $nodes.find((n) => n.id === id)
	$: type = data.data.type;
</script>

<div class="border-2 rounded-md p-2 bg-base-100 group {selected ? 'border-primary' : ''}">
	{#if !$readonly}
		<div class="absolute right-0 top-[-32px] hidden group-hover:flex hover:flex text-xs gap-1 py-2">
			<button
				class="bg-primary rounded p-1"
				class:bg-success={type === ChartType.Pie}
				on:click={() => changePlot(ChartType.Pie)}
			>
				<GgChart />
			</button>
			<button
				class="bg-primary rounded p-1"
				class:bg-success={type === ChartType.Line}
				on:click={() => changePlot(ChartType.Line)}
			>
				<LucideLineChart />
			</button>
			<button
				class="bg-primary rounded p-1"
				class:bg-success={type === ChartType.Bar}
				on:click={() => changePlot(ChartType.Bar)}
			>
				<MageChartFill />
			</button>
		</div>
	{/if}
	<Chart chart={data.data} bind:svgUrl={node.svgUrl} />
	{#if data?.data?.sources && data?.data?.sources?.length > 0}
		<a href={data?.data?.sources[0].url} target="_blank">Источник</a>
	{/if}
</div>
