<script lang="ts">
	import { init, use } from 'echarts/core';
	import { BarChart, LineChart } from 'echarts/charts';
	import {
		GridComponent,
		LegendComponent,
		TitleComponent,
		TooltipComponent
	} from 'echarts/components';
	import { CanvasRenderer } from 'echarts/renderers';
	import { Chart } from 'svelte-echarts';
	import { CHART_HEIGHT, CHART_WIDTH } from '../constants';
	import type { SeriesData } from 'echarts/types/dist/shared.js';
	import { BAR_SERIES, BAR_VIEW_CONFIGURATION } from './constants';
	import { onMount } from 'svelte';
	import { configureOptions } from '../controller';
	import type { EChartsType } from 'echarts';

	export let title = '';
	export let subtitle = '';
	export let series: SeriesData[] = [];
	export let category: string[] | null = null;
  export let svgUrl: string | undefined

	let self: EChartsType | undefined;
	const initOptions = { renderer: 'svg' };
	let options = null;

	function getSvgUrl() {
		svgUrl = self?.getSvgDataURL();
	}

	onMount(() => {
		options = configureOptions(BAR_VIEW_CONFIGURATION, BAR_SERIES, title, series, category);
	});

	use([
		BarChart,
		LineChart,
		GridComponent,
		TooltipComponent,
		LegendComponent,
		GridComponent,
		CanvasRenderer,
		TitleComponent
	]);
</script>

<div
	class="bg-base-200 rounded-2xl p-6 box-border"
	style:width="{CHART_WIDTH}px"
	style:height="{CHART_HEIGHT}px"
>
	{#key options}
		{#if options}
			<div class="w-full h-full">
				<Chart {init} {options} {initOptions} bind:chart={self} on:rendered={getSvgUrl} />
			</div>
		{/if}
	{/key}
</div>
