import type { SeriesModel } from "echarts";
import type { Series, SeriesData } from "./types";

export function getSeries(data: Array<SeriesData>, series: SeriesModel) {
	return {
		...series,
		data
	};
}

export function configureOptions(viewConfig: unknown, seriesSample: SeriesModel, name: string, series: Series[], category: string[] | null) {
	const viewOptions = JSON.parse(JSON.stringify(viewConfig));

  viewOptions.title.text = name
	series.forEach((s) => {
    const series = getSeries(s.data, seriesSample)
		viewOptions!.series.push(series);
	});

	if (category && category.length) {
		viewOptions.xAxis.data = category;
	} else {
    const category = series[0]?.data?.map((n) => {
      return n.name
    })
    viewOptions.xAxis.data = category
  }

	return viewOptions;
}
