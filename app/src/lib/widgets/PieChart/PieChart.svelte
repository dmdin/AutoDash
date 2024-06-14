<script lang="ts">
	import { Chart } from 'svelte-echarts';

	import { init, use } from 'echarts/core';
	import { color, type EChartsOption } from 'echarts';
	import { BarChart, PieChart } from 'echarts/charts';
	import {
		GridComponent,
		LegendComponent,
		TitleComponent,
		TooltipComponent
	} from 'echarts/components';
	import { CanvasRenderer } from 'echarts/renderers';
	import { SERIES_COLORS } from './constants';

	// now with tree-shaking
	use([PieChart, GridComponent, TooltipComponent, LegendComponent, GridComponent, CanvasRenderer, TitleComponent]);

  export let title = ''

	let options = {
    grid: {
      top: 0,
      left: 0,
      right: 0,
      show: true,
    },
		tooltip: {
			trigger: 'item'
		},
		legend: {
			orient: 'vertical',
			right: '45%',
			top: 'middle',
      icon: 'circle',
		},
		series: [
			{
				name: 'Access From',
				type: 'pie',
				radius: ['30%', '40%'],
				avoidLabelOverlap: false,
				data: [
					{ value: 1048, name: 'Search Engine', color: SERIES_COLORS[0] },
					{ value: 735, name: 'Direct', color: SERIES_COLORS[1] },
					{ value: 580, name: 'Email', color: SERIES_COLORS[2] },
					{ value: 484, name: 'Union Ads', color: SERIES_COLORS[3] },
					{ value: 300, name: 'Video Ads', color: SERIES_COLORS[4] }
				],
        right: '50%',
				label: {
					show: false,
					position: 'center'
				},
				itemStyle: {
					borderRadius: 100,
					color: (o) => {
						return SERIES_COLORS[o.dataIndex];
					}
				},
				emphasis: {
					itemStyle: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.9)'
					}
				}
			}
		]
	};
</script>

<div class="w-[800px] bg-base-200 rounded-[16px] p-[24px]">
  <h3 class="text-base-content text-[16px] font-semibold leading-5">Overview Data</h3>
  <div class="w-[800px] h-[400px]">
    <Chart {init} {options} />
  </div>
</div>
