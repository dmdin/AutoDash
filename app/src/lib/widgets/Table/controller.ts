import { get, writable } from 'svelte/store'
import type { Writable } from 'svelte/store'
import { getContext } from 'svelte'

import {
  CellTypes,
  type Cell,
  type ColData,
  type ColumnsConfig,
  type Controls,
  type DataConfig,
  type Head,
  type Rendered,
  type RowData,
  type TableConfig,
} from './types'
import { ColumnTypes } from './types'
import {
  COL_WIDTH_MULT,
  ENUMERATED_HEAD,
  MIN_COL_WIDTH,
} from './constants'

export const { rendered, controls } = createStores()

export function prepareColumns(data: Record<string, unknown[]>, columns, pinned: number[], config: TableConfig) {
  const prevState = get(rendered)
  let prepared: ColumnsConfig = structuredClone(columns)

  if (!columns) {
    // Handle undefined type

    prepared = Object.keys(data).map((c) => {
      return { name: c }
    })
  } else if (Array.isArray(columns)) {
    // Handle string[] and IColumn[]
    const colSample = columns[0]
    if (typeof colSample === 'string') {
      // Handle string[] type
      prepared = columns.map((c) => {
        return { name: c }
      })
    } else if (!colSample?.name) {
      // if not IColumn[] throw error else use it
      throw TypeError(
        "columns prop: can't process variant with IColumn interface. Values must be {name: string, title?: string, width?: string | number}"
      )
    }
  } else if (typeof columns === 'object') {
    prepared = Object.entries(columns).map(([k, v]) => {
      if (typeof v === 'string') {
        // Handle Record<string, string>. Expected that value is a title
        return { name: k, title: v }
        // @ts-ignore
      } else if (v?.title) {
        // Handle Record<string, IColumn>
        return { name: k, ...v }
      } else {
        throw TypeError(
          "columns prop: can't process variant with Record<string, IColumn> interface. Values must be { name: {title: string, width?: string | number} }"
        )
      }
    })
  }
  prepared = (prepared as Head[]).map((col, i) => {
    const prevWidth = prevState?.head[i]?.width
    const isPrevColCustom = prevState?.head[i]?.isCustom
    if (!prevWidth || isPrevColCustom) {
      if (!col.width) {
        col.width = (col.title?.length ?? col.name?.length) * 20 + COL_WIDTH_MULT
        if (col.width < MIN_COL_WIDTH) {
          col.width = MIN_COL_WIDTH
        }
      }
    } else {
      col.width = prevWidth
    }
    if (!col.title) {
      col.title = col.name
    }
    if (!col.type) {
      let sample: number | null = null,
        i = 0
      while (sample === null && i < data[col.name]!.length) {
        sample = data[col.name]![i] as number
        i++
      }

      if (Array.isArray(sample)) {
        col.type = ColumnTypes.List
      } else if (typeof sample === 'boolean') {
        col.type = ColumnTypes.Boolean
      } else if (typeof sample === 'number') {
        col.type = ColumnTypes.Number
      } else if (!Number.isNaN(Number(sample))) {
        col.type = ColumnTypes.Number
      } else if (
        new Date(sample) !== 'Invalid Date' &&
        !isNaN(new Date(sample))
      ) {
        col.type = ColumnTypes.Date
      } else {
        col.type = ColumnTypes.String
      }
    }
    if (!col.isPinned) {
      const index = config.enumerate ? i + 1 : i
      col.isPinned = pinned.includes(index)
    }
    return col
  })
  return prepared
}

// WARNING: This is used also in ListTable!
export function getSortIndexes(
  column: {
    head: { type?: ColumnTypes }
    data: Cell[]
  },
  params: { asc: boolean }
): number[] {
  const sortIndexes = Array.from(Array(column.data.length).keys())

  sortIndexes.sort((a, b) => {
    if (column.head.type === 'number' || column.head.type === 'boolean') {
      return (
        ((column.data[a] as number) - (column.data[b] as number)) *
        (params.asc ? 1 : -1)
      )
    } else if (column.head.type === 'string') {
      return (
        ((column.data[a] as string) ?? '').localeCompare(
          (column.data[b] as string) ?? ''
        ) * (params.asc ? 1 : -1)
      )
    } else if (column.head.type === 'list') {
      return (
        // @ts-expect-error fields are lists
        (column.data[a].length - column.data[b]?.length) * (params.asc ? 1 : -1)
      )
    } else if (column.head.type === 'date') {
      return (
        // @ts-expect-error fields are date
        (column.data[a] - column.data[b]) * (params.asc ? 1 : -1)
      )
    } else {
      return 0
    }
  })

  return sortIndexes
}

export function rows2cols(rows: RowData) {
  const cols = Object.keys(rows[0]!)
  const colBased = Object.fromEntries(cols.map((c) => [c, []]))

  for (const row of rows) {
    for (const [k, v] of Object.entries(row)) {
      colBased[k]!.push(v as never)
    }
  }

  return colBased
}

// TODO refactor to SpreadSheet based structure of DataTable
// export function cols2rows(cols: ColData) {
//   const cols = Object.keys(rows[0]!)
//   const colBased = Object.fromEntries(cols.map((c) => [c, []]))

//   for (const row of cols) {
//     for (const [k, v] of Object.entries(row)) {
//       colBased[k]!.push(v as never)
//     }
//   }

//   return colBased
// }
export function getPinnedColumns(columns: ColumnsConfig) {
  if (!columns) return []

  const pastState = get(rendered)
  if (pastState?.pinned?.length) return pastState.pinned

  const isArray = Array.isArray(columns)

  if (!isArray) {
    const pinned: number[] = []
    Object.entries(columns).forEach(([k, v], i) => {
      if (v?.isPinned) pinned.push(i)
    })
   return pinned
  }

  return columns.reduce((prevVal, currentVal, i) => {
    if (currentVal?.isPinned) {
      return [...prevVal, i]
    }

    return prevVal
  }, [])
}

export function renderTable({
  data,
  columns,
  controls,
  config,
}: {
  data: DataConfig
  columns: ColumnsConfig
  controls: Controls
  config: TableConfig
}): Rendered {
  // Expensive operation for huge data, check it
  let body = structuredClone(data)
  if (Array.isArray(data)) {
    body = rows2cols(data)
  }
  const pinned = getPinnedColumns(columns) as number[]
  const head = prepareColumns(body as ColData, columns, pinned, config)
  const length = body[head[0]!.name].length as number
  let sortIndex = Array.from(Array(length).keys())

  // if (totalValues) renderedTotalValues = prepareTotalValues(totalValues)

  const sortBy = head.find((h) => h.name === controls.sort.by)
  if (sortBy) {
    sortIndex = getSortIndexes(
      { head: sortBy, data: body[sortBy.name] },
      { asc: controls.sort.asc }
    )
  }

  if (config.enumerate) {
    const enumerationIndex = config.totals ? 1 : 0
    const enumeratedValues = getEnumerateArray(length, enumerationIndex)
    appendColumns(head, ENUMERATED_HEAD, body, enumeratedValues, 0)
    if (ENUMERATED_HEAD.isPinned) {
      pinned.splice(0, 0, 0)
    }
  }
  // update rows config indexes after sorting
  return {
    head,
    body,
    sortIndex,
    length,
    config,
    pinned,
  } as Rendered
}

export function createStores() {
  const rendered = writable<Rendered>()

  const controls = writable<Controls>({
    sort: {
      asc: false,
    },
  })
  return { rendered, controls }
}

export function getRenderStore(): Writable<Rendered> {
  return getContext('rendered')
}

export function getTypeFromString(string: string): CellTypes {
  if (!isNaN(parseFloat(string)) && isFinite(Number(string))) {
    return CellTypes.Number
  }

  if (string === null) {
    return CellTypes.Null
  }

  const date = new Date(string)
  if (!isNaN(date.getTime()) && string.match(ISO_STRING_REGEX)) {
    return CellTypes.Date
  }

  return CellTypes.String
}

function getEnumerateArray(length, startIndex = 0) {
  const arr: Array<number | null> = []
  let counter = 1
  for (let i = 0; i < length; i++) {
    if (i < startIndex) {
      arr.push('Итого:')
      continue
    }

    arr.push(counter)
    counter++
  }

  return arr
}

export function insertRow(value: Cell[], position: number) {
  const store = get(rendered)

  const body = Object.fromEntries(
    Object.entries(store.body).map(([k, v], i) => {
      const val = value[i] || null
      v.splice(position, 0, val)
      return [k, v]
    })
  )

  rendered.set({
    ...store,
    body,
  })
}

// !!!!! Функция работает с указателями
function appendColumns(
  head: Head[],
  column: Head,
  body: ColData,
  data: Cell[],
  position: number
) {
  head.splice(position, 0, column)
  body[column.name] = data
}

export function insertColumn(column: Head, data: Cell[], position: number) {
  const store = get(rendered)
  if (!store) return

  const { head, body } = store
  appendColumns(head, column, body, data, position)

  rendered.set({
    ...store,
    head,
    body,
  })
}
