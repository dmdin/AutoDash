<script lang="ts">
  import { afterUpdate, getContext, onMount } from 'svelte'
  import type { Writable } from 'svelte/store'
  import FileExcel from '~icons/ph/microsoft-excel-logo-light'
  import Excel from 'exceljs'

  import { triggerDownload, prepareExport } from './controller'
  import type { Rendered, StyleTableCallback } from '../../types'

  const data = getContext<Writable<Rendered>>('export')
  export let styleTable: StyleTableCallback | null = getContext('styleTable')

  export const download = async function () {
    const { header, rows } = prepareExport($data)
    const workbook = new Excel.Workbook()
    const worksheet = workbook.addWorksheet('table-export')
    worksheet.columns = header.map((head) => {
      return {
        header: head.title,
        width: head.width / 6.6,
        key: head.title.toLowerCase(),
      }
    })
    worksheet.addRows(rows)

    if (styleTable) {
      styleTable(worksheet)
    }

    const buffer = await workbook.xlsx.writeBuffer()
    const blob = new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    triggerDownload({ blob, extension: 'xlsx' })
  }
</script>

<button
  on:click={download}
  type="button"
  title="Скачать таблицу в XLSX"
  class="btn h-fit w-fit rounded-md bg-base-100 px-2 py-1 transition-colors hover:bg-neutral/60 hover:text-neutral-content {$$props.class}">
  <FileExcel width="30" />
</button>
