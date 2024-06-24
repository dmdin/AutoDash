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
	import type { EChartsType } from 'echarts';

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
  export let svgUrl: string | undefined

  let self: EChartsType | undefined
  const initOptions = { renderer: 'svg' }
	let options = null;

  function getSvgUrl() {
    svgUrl = self?.getSvgDataURL()
  }

	onMount(() => {
		options = configureOptions(PIE_VIEW_CONFIG, PIE_SERIES, title, series?.slice(0, 1), null)

    if (!options?.series?.length) return
    console.log(options.series[0].data)
    options.series[0].data = options.series[0].data.map((c, i) => {
      return {
        name: category[i],
        value: c,
      }
    })
    options = options
	});
</script>

<div
	class="bg-base-200 rounded-2xl p-6"
	style:width="{CHART_WIDTH}px"
	style:height="{CHART_HEIGHT}px"
>
	<div class="w-full h-full">
		{#key options}
			{#if options}
				<Chart x={0} {init} {options} {initOptions} bind:chart={self} on:rendered={getSvgUrl} />
			{/if}
		{/key}
	</div>
</div>
