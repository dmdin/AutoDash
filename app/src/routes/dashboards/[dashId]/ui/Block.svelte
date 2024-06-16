<script>
	import { getContext, onMount, setContext } from 'svelte';
	import { Board } from './index';
	import { writable } from 'svelte/store';
	import { number } from 'echarts';
	import { SvelteFlowProvider } from '@xyflow/svelte';
</script>

<div class="w-[1080px] h-full p-4 border-x">
	<SvelteFlowProvider>
		<Board />
	</SvelteFlowProvider>
</div>
