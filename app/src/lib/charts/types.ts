export enum ChartType {
  Pie = 'pie',
  Bar = 'bar',
  Line = 'line',
}

export interface SeriesData {
  name: string,
  value: string | number,
}

export interface Series {
  name: string,
  unit: string,
  data: SeriesData[],
}

export interface Chart {
  type: ChartType,
  title: string,
  subtitle: string,
  category: string[],
  series: Series[],
}
