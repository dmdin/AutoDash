<script lang="ts">
	import { SERIES_COLORS } from '../PieChart/constants';
	import { init, use } from 'echarts/core';
	import { Axis, color, format, type EChartsOption } from 'echarts';
	import { BarChart, LineChart } from 'echarts/charts';
	import {
		GridComponent,
		LegendComponent,
		TitleComponent,
		TooltipComponent
	} from 'echarts/components';
	import { CanvasRenderer } from 'echarts/renderers';
	import { Chart } from 'svelte-echarts';
	import { formatNumber } from '../../utils/utils';

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

	export let title = '';

	let options = {
		xAxis: {
			type: 'category',
			data: ['Linux', 'Mac', 'iOS', 'Windows', 'Android', 'Other'],
			axisLabel: {
				color: '#888'
			},
			axisTick: {
				show: false
			}
		},
		yAxis: {
			type: 'value',
			interval: 5000000,
			axisLabel: {
        formatter: (v) => formatNumber(v),
				color: '#888'
			}
		},
		series: [
			{
				data: [20000000, 22000000, 20000000, 24000000, 10000000, 22000000],
				type: 'bar',
				width: 200,
				height: 500,
				itemStyle: {
					color: function (params) {
						return SERIES_COLORS[params.dataIndex];
					},
					borderRadius: [4, 4, 0, 0]
				},
				barWidth: '50%'
			},
      {
				data: [20000000, 22000000, 20000000, 24000000, 10000000, 22000000],
				type: 'line',
				width: 200,
				height: 500,
				itemStyle: {
					color: function (params) {
						return SERIES_COLORS[params.dataIndex];
					},
					borderRadius: [4, 4, 0, 0]
				},
				barWidth: '50%'
			}
		],
		grid: {
			left: '3%',
			right: '4%',
			bottom: '3%',
      top: '30',
			containLabel: true
		},
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			}
		}
	};
</script>

<div class="w-[500px] h-[280px] bg-base-200 rounded-[16px] p-[24px] box-border">
	<h3 class="text-base-content text-[16px] font-semibold leading-5">Traffic Device</h3>
	<div class="w-full h-full">
		<Chart x={0} {init} {options} />
	</div>
</div>
