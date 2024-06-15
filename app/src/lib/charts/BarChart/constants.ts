import { formatNumber } from '$root/lib/utils/utils';
import { SERIES_COLORS } from '../PieChart/constants';


export const BAR_SERIES = {
	type: 'bar',
	width: 200,
	height: 500,
	axisLabel: {
		fontWeight: 'Lighter'
	},
	itemStyle: {
		color: function (params) {
			return SERIES_COLORS[params.dataIndex];
		},
		borderRadius: [4, 4, 0, 0]
	},
	barWidth: '50%',
};

export const BAR_VIEW_CONFIGURATION = {
	xAxis: {
		type: 'category',
		axisLabel: {
			fontWeight: 'Lighter',
			color: '#888'
		},
		axisTick: {
			show: false
		}
	},
	yAxis: {
		type: 'value',
		// TODO: вычисление интервала
		axisLabel: {
			fontWeight: 'Lighter',
			formatter: (v) => formatNumber(v),
			color: '#888'
		}
	},
	series: [],
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