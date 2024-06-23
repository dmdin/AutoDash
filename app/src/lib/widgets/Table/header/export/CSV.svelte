<script lang="ts">
  // import FileCSV from '~icons/ph/file-csv'
  import FileCSV from '~icons/bi/filetype-csv';
  import {getContext} from 'svelte'
  import type {Writable} from 'svelte/store'
  import { triggerDownload, prepareExport } from './controller'
  import type { Rendered } from '../../types'

  const data = getContext<Writable<Rendered>>('export')

  function download() {
    let { header, rows } = prepareExport($data)
    const joined = [
      header.join(';'),
      ...rows.map((r) => {
        return r.join(';')
      }),
    ].join('\n')

    const blob = new Blob([joined], { type: 'plain/text' })
    triggerDownload({ blob, extension: 'csv' })
  }
</script>

<button
  on:click={download}
  type="button"
  title="Скачать таблицу в CSV"
  class="btn w-fit h-fit rounded-md bg-base-100 py-1 px-2 transition-colors hover:bg-neutral/60 hover:text-neutral-content {$$props.class}">
  <FileCSV width="30" />
</button>
