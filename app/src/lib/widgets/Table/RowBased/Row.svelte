<script lang="ts">
  import type {RowConfig} from '../types'
  import {getRenderStore} from '../controller'
  export let config: RowConfig = undefined
  export let virtualIndex: number
  const rendered = getRenderStore()
</script>

<tr
  on:click
  class="
    border-t border-base-200/80
    font-arial
    {$$restProps.class}
    {config?.class}
    {!config?.class && !$$restProps.class ? (virtualIndex % 2 === 0 ? 'bg-base-200/40': '') : ''}
  "
  style="height: {$rendered.config.rowHeight}px; {$$restProps.style}"
  >
  <slot />
</tr>
