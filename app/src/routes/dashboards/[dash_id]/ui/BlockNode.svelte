<script>
  import { Background, BackgroundVariant } from '@xyflow/svelte'

  export let data
  export let selected
</script>

<div class="w-[1080px] h-96 p-4 border-2">
  <p>{data.label}</p>
</div>

