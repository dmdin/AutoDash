<script>
	import { SvelteFlowProvider } from '@xyflow/svelte'
  import { getContext, onMount, setContext } from 'svelte';
	import { Board } from './index';
	import { writable } from 'svelte/store';
	import { number } from 'echarts';

  export let data = {
    order: -1,
  }
</script>

<div class="w-[1080px] h-full p-4 border-x">
	<SvelteFlowProvider>
		<Board />
	</SvelteFlowProvider>
</div>
