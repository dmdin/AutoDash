import type { Worksheet } from 'exceljs'


export type Cell = number | string | null | Date

export interface Head {
  title?: string
  name: string
  width?: number
  isPinned?: boolean
  offsetLeft?: number
  type?: ColumnTypes | string
  unit?: string
  skipRender?: boolean
  sortable?: boolean
  element?: HTMLTableCellElement
  isCustom?: boolean
}

export enum ColumnTypes {
  Number = 'number',
  String = 'string',
  Date = 'date',
  Boolean = 'boolean',
  List = 'list'
}

export type Controls = {
  sort: {
    by?: Head['name'] | null
    asc: boolean
  },
}

export interface TableConfig {
  rowHeight: number
  scrollbar: string
  precision: Record<string, number>
  rows: RowsConfig
  enumerate: boolean,
  // TODO
  totals: unknown
  isPinnable: boolean
}

export type totalValues =
  | Array<number | string>
  | Record<string, number | string>


export type RowData = Record<Head['name'], Cell>[]
export type ColData = Record<Head['name'], Cell[]>

export type DataConfig = RowData | ColData
export type ColumnsConfig =
  | Head[]
  | Record<Head['name'], Head>
  | Record<Head['name'], Head['title']>
  | Head['name'][]
  | undefined


export type RowConfig = { class: string; [k: string]: unknown } | undefined
export type RowsConfig = Record<
  number | string, // Row index
  RowConfig // Attrs
> | RowConfig[]

export type SortIndexes = number[]

export type Rendered = {
  head: Head[]
  body: ColData
  sortIndex: number[]
  length: number
  config: TableConfig
  pinned: number[]
}

export enum CellTypes {
  Number = "number",
  String = "string",
  Date = "date",
  Null = "null",
}

export type StyleTableCallback = (worksheet: Worksheet) => void
