<script>

import { SvelteFlowProvider } from '@xyflow/svelte'
import { Board } from './index'
</script>

<div class="w-[1080px] h-full p-4 border-x">
    <SvelteFlowProvider>
        <Board/>
    </SvelteFlowProvider>
</div>