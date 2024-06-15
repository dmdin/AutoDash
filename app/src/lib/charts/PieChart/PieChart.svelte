<script lang="ts">
	import { Chart } from 'svelte-echarts';

	import { init, use } from 'echarts/core';
	import { PieChart } from 'echarts/charts';
	import {
		GridComponent,
		LegendComponent,
		TitleComponent,
		TooltipComponent
	} from 'echarts/components';
	import { CanvasRenderer } from 'echarts/renderers';
	import { PIE_SERIES, PIE_VIEW_CONFIG, SERIES_COLORS } from './constants';
	import type { Series } from '../types';
	import { onMount } from 'svelte';
	import { configureOptions } from '../controller';
	import { CHART_HEIGHT, CHART_WIDTH } from '../constants';

	use([
		PieChart,
		GridComponent,
		TooltipComponent,
		LegendComponent,
		GridComponent,
		CanvasRenderer,
		TitleComponent
	]);

	export let title: string = '';
	export let subtitle: string = '';
	export let category: string[] | null = null;
	export let series: Series[];

	let options = null;

	onMount(() => {
		options = configureOptions(PIE_VIEW_CONFIG, PIE_SERIES, series.slice(0, 1), null);
	});
</script>

<div
	class="bg-base-200 rounded-2xl p-6"
	style:width="{CHART_WIDTH}px"
	style:height="{CHART_HEIGHT}px"
>
	<h3 class="text-base-content text-[16px] font-semibold leading-5">{title}</h3>
	<div class="w-full h-full">
		{#key options}
			{#if options}
				<Chart x={0} {init} {options} />
			{/if}
		{/key}
	</div>
</div>
