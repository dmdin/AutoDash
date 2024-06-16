export const LINE_SERIES_COLORS = [
	'#A8C5DA',
	'#1C1C1C',
	'#E3A1CB',
	'#A1D3E3',
	'#D1E3A1',
	'#CBA1E3'
];

export const LINE_SERIES = {
	type: 'line',
	smooth: true,
	itemStyle: {
		color: 'black'
	},
	lineStyle: {
		width: 2,
		type: 'solid'
	}
};

export const LINE_VIEW_CONFIG = {
	title: {
		textStyle: {
			fontSize: 16,
			color: '#1C1C1C',
			fontFamily: 'system-ui',
			width: 520, // Максимальная ширина текста в пикселях
			overflow: 'truncate', // Указание на усечение текста
			ellipsis: '...' // Символы, добавляемые в конец усечённого текста
		},
		overflow: 'truncate'
	},
	xAxis: {
		type: 'category',
		boundaryGap: false,
		axisTick: {
			show: false
		},
		axiosLabel: {
			fontWeight: 'Lighter'
		}
	},
	yAxis: {
		type: 'value'
	},
	series: [],
	grid: {
		left: '3%',
		right: '4%',
		bottom: '3%',
		containLabel: true
	},
	legend: {
		right: 10
	},
	tooltip: {
		trigger: 'axis'
	}
};
