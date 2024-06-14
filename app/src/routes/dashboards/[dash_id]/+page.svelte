<script lang="ts">
  import { writable } from 'svelte/store';
  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    MiniMap
  } from '@xyflow/svelte';

  // 👇 this is important! You need to import the styles for Svelte Flow to work
  import '@xyflow/svelte/dist/style.css';
  import { PlotNode } from './ui'

  // We are using writables for the nodes and edges to sync them easily. When a user drags a node for example, Svelte Flow updates its position.
  const nodes = writable([
    {
      id: '1',
      type: 'plot-node',
      data: { label: 'Input Node' },
      position: { x: 0, y: 0 }
    },
    {
      id: '2',
      type: 'plot-node',
      data: { label: 'Node' },
      position: { x: 0, y: 150 }
    }
  ]);

  // same for edges
  const edges = writable([]);

  const snapGrid = [25, 25];

  const nodeTypes = {
    'plot-node': PlotNode
  }
</script>
<div class="w-full h-full">
  <div class="mx-auto max-w-[1080px] h-screen">
    <SvelteFlow
      {nodes}
      {edges}
      {snapGrid}
      {nodeTypes}
      fitView
      on:nodeclick={(event) => console.log('on node click', event.detail.node)}
      on:selectionclick={() => console.log('on:selectionclick')}
      on:selectioncontextmenu={e => console.log(e)}
    >
      <Controls />
      <Background variant={BackgroundVariant.Dots} />
      <MiniMap />
    </SvelteFlow>
  </div>
</div>
