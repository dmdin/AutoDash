<script>
  import { writable } from 'svelte/store';
  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    MiniMap
  } from '@xyflow/svelte';

  import '@xyflow/svelte/dist/style.css';
  import ContextMenu from './ContextMenu.svelte'
  import PlotNode from './PlotNode.svelte'

  let menu
  let boardDom
  let height
  let width

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

  function handleContextMenu({ detail }) {
    const node = detail.nodes ? detail.nodes[0] : detail.node
    const event = detail.event
    event.preventDefault()

    const boardRect = boardDom.getBoundingClientRect()

    menu = {
      id: node.id,
      top: event.clientY - boardRect.y,
      left: event.clientX - boardRect.x,
    };
  }

  function handlePaneClick() {
    menu = null;
  }
</script>

<div class="mx-auto max-w-[1080px] h-screen relative" bind:clientWidth={width} bind:clientHeight={height} bind:this={boardDom}>
  <SvelteFlow
    {nodes}
    {edges}
    {snapGrid}
    {nodeTypes}
    fitView
    on:nodeclick={(event) => console.log('on node click', event.detail.node)}
    on:selectionclick={() => console.log('on:selectionclick')}
    on:selectioncontextmenu={handleContextMenu}
    on:nodecontextmenu={handleContextMenu}
    on:paneclick={handlePaneClick}
  >
    <Controls />
    <Background variant={BackgroundVariant.Dots} />
    <MiniMap />

    {#if menu}
      <ContextMenu
        onClick={handlePaneClick}
        id={menu.id}
        top={menu.top}
        left={menu.left}
        right={menu.right}
        bottom={menu.bottom}
      />
    {/if}

  </SvelteFlow>
</div>