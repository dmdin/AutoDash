<script lang="ts">
  import { SvelteComponent, setContext } from 'svelte'
  import { writable, type Writable } from 'svelte/store'

  import type {
    DataConfig,
    ColumnsConfig,
    RowsConfig,
  } from './types'

  import RowBased from './RowBased/Body.svelte'

  import { rendered, controls, renderTable } from './controller'

  // can handle [{col1: row1, col2: row2}, {...},]
  // and {col1: [...rows1], col2: [...rows2] }
  // Use ColData as main type for component
  export let data: DataConfig

  // We can make custom order if set Array
  // Use IColumn[] as main type for component
  export let columns: ColumnsConfig

  export let isPinnable = false
  export let enumerate = false
  export let rows: RowsConfig = {}
  export let rowHeight = 30
  export let scrollbar = 'scrollbar-thin'
  export let precision = { '0': 0, '%': 1, '₽': 2 }
  export let totals = true

  $: config = {
    rowHeight,
    scrollbar,
    precision,
    totals,
    rows,
    enumerate,
    isPinnable,
  }
  $: console.log($rendered)

  $: $rendered = renderTable({ data, columns, controls: $controls, config })
  setContext('rendered', rendered)
  setContext('controls', controls)
</script>

<div>
  {#if $$slots.controlsTop}
    <div
      class="mb-1 flex w-full items-center justify-between text-base-content/60">
      <slot name="controlsTop" />
    </div>
  {/if}
  {#if $$slots.header}
    <div class="py-1">
      <slot name="header" />
    </div>
  {/if}
</div>
{#if $rendered}
  <slot name="table">
    <RowBased {...$$restProps} />
  </slot>
{/if}

{#if $$slots.controlsBottom}
  <div
    class="mt-3 flex w-full items-center justify-between text-base-content/60">
    <slot name="controlsBottom" />
  </div>
{/if}
