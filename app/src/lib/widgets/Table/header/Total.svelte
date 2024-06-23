<script lang="ts">
  import {getRenderStore} from '../controller' 

  export let length = null

  const rendered = getRenderStore()
</script>

<span class="mx-1 text-xs order-first {$$props.class}">Всего: {length ?? $rendered.length}</span>
