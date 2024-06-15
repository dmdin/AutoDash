<script lang="ts">
	import type { Chart } from "svelte-echarts";
	import { ChartType } from "./types";
	import PieChart from "./PieChart/PieChart.svelte";
	import CustomChart from "./CustomChart/CustomChart.svelte";

  export let chart: Chart
</script>

{#if chart.type === ChartType.Pie}
  <PieChart {...chart} />
{/if}

{#if chart.type === ChartType.Custom}
  <CustomChart {...chart} />
{/if}
