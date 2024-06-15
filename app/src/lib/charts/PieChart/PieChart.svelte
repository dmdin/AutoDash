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
	import { SERIES_COLORS } from './constants';
	import type { Series } from '../types';

	use([PieChart, GridComponent, TooltipComponent, LegendComponent, GridComponent, CanvasRenderer, TitleComponent]);

  export let title: string = ''
  export let subtitle: string = ''
  export let category: string[] | null = null
  export let series: Series[]

	let options = {
    grid: {
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      show: false,
      borderWidth: 1,
    },
		tooltip: {
			trigger: 'item'
		},
		legend: {
			orient: 'vertical',
			right: '10',
			top: 'middle',
      icon: 'circle',
      textStyle: {
        fontSize: 12,
        fontWeight: 'lighter',
      }
		},
		series: [
			{
        width: 180,
        height: 180,
				name: 'Access From',
				type: 'pie',
        center: ['33%', '38%'],
				radius: ['40%', '50%'],
				avoidLabelOverlap: false,
        position: 'left',
				data: [
					{ value: 1048, name: 'Search Engine', color: SERIES_COLORS[0] },
					{ value: 735, name: 'Direct', color: SERIES_COLORS[1] },
					{ value: 580, name: 'Email', color: SERIES_COLORS[2] },
					{ value: 484, name: 'Union Ads', color: SERIES_COLORS[3] },
					{ value: 300, name: 'Video Ads', color: SERIES_COLORS[4] }
				],
				label: {
					show: false,
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

<div class="w-[400px] bg-base-200 rounded-[16px] p-[24px]">
  <h3 class="text-base-content text-[16px] font-semibold leading-5">Overview Data</h3>
  <div class="w-[350px] h-[120px]">
    <Chart x={0} {init} {options} />
  </div>
</div>
