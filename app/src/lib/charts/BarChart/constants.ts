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
	barWidth: '50%'
};

export const BAR_VIEW_CONFIGURATION = {
	title: {
    left: 0,
    right: 0,
		textStyle: {
			fontSize: 16,
			color: '#1C1C1C',
			fontFamily: 'system-ui',
      width: 520, // Максимальная ширина текста в пикселях
      overflow: 'truncate', // Указание на усечение текста
      ellipsis: '...' // Символы, добавляемые в конец усечённого текста
		},
    overflow: 'truncate',
	},
	xAxis: {
		type: 'category',
		axisLabel: {
			fontWeight: 'Lighter',
			color: '#888'
		},
		axisTick: {
			show: false
		},
    data: [],
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
		top: '50',
		containLabel: true
	},
	tooltip: {
		trigger: 'axis',
		axisPointer: {
			type: 'shadow'
		}
	}
};
