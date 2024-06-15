<script>
  import { rpc } from '$root/routes'
  import { WIDGET_SHIFT_X, WIDGET_SHIFT_Y } from '$root/routes/dashboards/[dashId]/constants'
  import { theme } from '$stores'
  import { onMount } from 'svelte'
  import { writable } from 'svelte/store';
  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    MiniMap
  } from '@xyflow/svelte';

  import '@xyflow/svelte/dist/style.css';
  import BlockNode from './BlockNode.svelte'
  import ContextMenu from './ContextMenu.svelte'
  import PlotNode from './PlotNode.svelte'
  import { nodes, edges, dashboard, reservedPlace, dashId } from '../controller'

  let menu
  let boardDom
  let height
  let width

  const snapGrid = [25, 25];

  const nodeTypes = {
    'plot-node': PlotNode,
    'block-node': BlockNode
  }

  onMount(() => {
    createNodes()
  })

  function createNodes() {
    if (!$dashboard) return

    for (const block of $dashboard.blocks) {
      for (const widget of block.widgets) {
        let position = { x: WIDGET_SHIFT_X, y: WIDGET_SHIFT_Y }
        if (widget.xPos && widget.yPos) {
          position = { x: widget.xPos, y: widget.yPos }
        } else {
          position = { x: $reservedPlace.x, y: $reservedPlace.y + WIDGET_SHIFT_Y}
        }

        const node = {
          id: widget.id,
          type: 'plot-node',
          position: position,
        }

        $reservedPlace = { x: position.x, y: position.y + 200 }
        $nodes = [...$nodes, node]
      }
    }
  }

  function calcPosition() {

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

  async function saveWidget({ detail: { event, nodes }}) {
    await rpc.batch(
      ...nodes.map(node => rpc.Dashboard.updateWidget.batch(node.id, { xPos: node.position.x, yPos: node.position.y }))
    )
  }
</script>

<div class="w-full h-full relative" bind:clientWidth={width} bind:clientHeight={height} bind:this={boardDom}>
  <SvelteFlow
    {nodes}
    {edges}
    {snapGrid}
    {nodeTypes}
    preventScrolling={false}
    colorMode={$theme}
    on:nodeclick={(event) => console.log('on node click', event.detail.node)}
    on:selectionclick={() => console.log('on:selectionclick')}
    on:selectioncontextmenu={handleContextMenu}
    on:nodecontextmenu={handleContextMenu}
    on:paneclick={handlePaneClick}
    on:nodedragstop={saveWidget}
  >
    <Background variant={BackgroundVariant.Dots} />
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