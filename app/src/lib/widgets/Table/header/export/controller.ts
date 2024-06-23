// import
import { getTypeFromString } from '../../controller'
import { type Rendered, type Cell, CellTypes } from '../../types'

function round(v) {
  return v
}

function prepareRows(rawRow: string, declaredType: CellTypes): string | number | Date {
  const rowType = getTypeFromString(rawRow as string)

  switch (rowType) {
    case CellTypes.String:
      return rawRow.toString()
    case CellTypes.Number:
      return round(Number(rawRow), 100)
    case CellTypes.Date:
      return new Date(rawRow)
    case CellTypes.Null:
      if (declaredType === CellTypes.Number) return 0

      return "—"
  }
}

export function prepareExport(rendered: Rendered) {
  const header = rendered.head.map((c) => {
    return {
      title: c.title ?? c.name,
      width: c.width || 50,
    }
  })
  const rows: (Cell | undefined)[][] = []

  for (const i of Array(rendered.length).keys()) {
    const row: (Cell | undefined)[] = []

    const columnsData = rendered.head.map((c) => { return { col: c.name, type: c.type } })
    for (let j = 0; j < columnsData.length; j++) {
      const { col, type } = columnsData[j]!

      const rawRow = rendered.body[col]![i] as string
      const preparedRow = prepareRows(rawRow, type as CellTypes)

      row.push(preparedRow)
    }

    rows.push(row)
  }
  return { header, rows }
}

export function triggerDownload({ blob, name = '', extension = 'csv' }: { blob: Blob, name?: string, extension?: string }) {
  const d = new Date()
  name = name || `Выгрузка-${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`
  const filename = `${name}.${extension}`
  saveData(blob, filename)
}

const saveData = (function () {
  if (typeof document === 'undefined') return () => { }
  const a = document.createElement('a')
  document.body.appendChild(a)
  a.setAttribute('style', 'display: none')

  return function (blob, fileName) {
    const url = window.URL.createObjectURL(blob)
    a.href = url
    a.download = fileName
    a.click()
    window.URL.revokeObjectURL(url)
  }
})()
