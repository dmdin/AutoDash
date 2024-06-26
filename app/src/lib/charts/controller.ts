import type { SeriesModel } from "echarts";
import type { Series, SeriesData } from "./types";
import { get, writable, type Writable } from "svelte/store";

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
	}

	return viewOptions;
}

export function storable<T>(data: T, storeKey: string): Writable<T> {
  const store = writable(data)
  const { subscribe, set, update } = store
  const isBrowser = typeof window !== 'undefined'

  isBrowser &&
    localStorage[`storable_${storeKey}`] &&
    set(JSON.parse(localStorage[`storable_${storeKey}`]))

  return {
    subscribe,
    set: (n) => {
      isBrowser && (localStorage[`storable_${storeKey}`] = JSON.stringify(n))
      set(n)
    },
    update: (cb) => {
      const updatedStore = cb(get(store))
      isBrowser &&
        (localStorage[`storable_${storeKey}`] = JSON.stringify(updatedStore))
      set(updatedStore)
    },
  }
}
