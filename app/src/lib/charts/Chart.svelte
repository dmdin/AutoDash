<script lang="ts">
	import type { Chart } from "svelte-echarts";
	import { ChartType } from "./types";
	import PieChart from "./PieChart/PieChart.svelte";
	import BarChart from "./BarChart/BarChart.svelte";
	import LineChart from "./LineChart/LineChart.svelte";

  export let chart: Chart
</script>

{#if chart.type === ChartType.Pie}
  <PieChart {...chart} />
{/if}

{#if chart.type === ChartType.Bar}
  <BarChart {...chart} />
{/if}

{#if chart.type === ChartType.Line}
  <LineChart {...chart} />
{/if}
