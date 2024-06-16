<script>
	import { getContext, onMount, setContext } from 'svelte';
	import { Board } from './index';
	import { writable } from 'svelte/store';
	import { number } from 'echarts';

<<<<<<< HEAD
  export let data = {
    order: -1,
  }

  const blocksImages = getContext('blocksImages')
  const widgetImages = writable([])

  onMount(() => {
    $blocksImages[data.order] = widgetImages
    console.log($widgetImages)
  })

  setContext('widgetsImages', widgetImages)
</script>

<div class="w-[1080px] h-[1500px] p-4 border-x">
	<Board />
</div>
=======
import { SvelteFlowProvider } from '@xyflow/svelte'
import { Board } from './index'
</script>

<div class="w-[1080px] h-full p-4 border-x">
    <SvelteFlowProvider>
        <Board/>
    </SvelteFlowProvider>
</div>
>>>>>>> b00ee1657ffeb9254243dd3bbff3bda0d31370e4
