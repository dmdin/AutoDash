import type { SeriesModel } from "echarts";
import type { Series, SeriesData } from "./types";

export function getSeries(data: Array<SeriesData>, series: SeriesModel) {
	return {
		...series,
		data
	};
}

export function configureOptions(viewConfig: unknown, seriesSample: SeriesModel, series: Series[], category: string[] | null) {
	const viewOptions = viewConfig;

	series.forEach((s) => {
    const series = getSeries(s.data, seriesSample)
		viewOptions!.series.push(series);
	});

	if (category && category.length) {
		viewOptions.yAxis.data = category;
	}

	return viewOptions;
}
