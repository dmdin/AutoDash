<script lang="ts">
	import type { Chart } from "svelte-echarts";
	import { ChartType } from "./types";
	import PieChart from "./PieChart/PieChart.svelte";
	import BarChart from "./BarChart/BarChart.svelte";
	import LineChart from "./LineChart/LineChart.svelte";

  export let chart
  export let svgUrl = ''
  let parsedChart
  function parseChart() {
    if (chart.series) return // Совместимость со старым форматом)

    parsedChart = {
      "type": chart.type,
      "title": chart.title,
      "subtitle": "",
      "category": chart.categories || chart.data.map(el => el.name) || [],
      "series": [
        {
          "name": "",
          "unit": "",
          "data": chart.data
        }
      ]
    }
  }

  $: if (chart) parseChart()
</script>

{#if chart.type === ChartType.Pie}
  <PieChart {...parsedChart} bind:svgUrl />
{/if}

{#if chart.type === ChartType.Bar}
  <BarChart {...parsedChart} bind:svgUrl />
{/if}

{#if chart.type === ChartType.Line}
  <LineChart {...parsedChart} bind:svgUrl />
{/if}
