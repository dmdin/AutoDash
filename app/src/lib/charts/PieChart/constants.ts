export const SERIES_COLORS = ['#95A4FC', '#BAEDBD', '#1C1C1C', '#B1E3FF', '#A8C5DA', '#E3A1CB'];

export const PIE_SERIES = {
  width: 350,
  height: 350,
	type: 'pie',
	center: ['25%', '35%'],
	radius: ['40%', '50%'],
	avoidLabelOverlap: false,
	position: 'left',
	label: {
		show: false
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
};

export const PIE_VIEW_CONFIG = {
	grid: {
		top: 0,
		left: 0,
		right: 0,
		bottom: 0,
		show: false,
		borderWidth: 1
	},
	tooltip: {
		trigger: 'item'
	},
  series: [],
	legend: {
		orient: 'vertical',
		top: 'middle',
    right: 100,
		icon: 'circle',
		textStyle: {
			fontSize: 12,
			fontWeight: 'lighter'
		}
	}
};
