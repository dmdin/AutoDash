<script>
  import { rpc } from '$root/routes'
  import { WIDGET_SHIFT_X, WIDGET_SHIFT_Y } from '$root/routes/dashboards/[dashId]/constants'
  import TextNode from '$root/routes/dashboards/[dashId]/ui/TextNode.svelte'
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

  const PLOT_SIZE = { width: 400, height: 200 }
  const TEXT_NODE_SIZE = { height: 25 }

  let menu
  let boardDom
  let height
  let width

  const snapGrid = [25, 25];

  const nodeTypes = {
    'plot-node': PlotNode,
    'text-node': TextNode,
    'block-node': BlockNode
  }

  onMount(() => {
    createNodes()
  })

  async function createNodes() {
    if (!$dashboard) return

    for (const block of $dashboard.blocks) {
      let position = { x: WIDGET_SHIFT_X, y: WIDGET_SHIFT_Y }
      if ($reservedPlace) {
        position = { x: WIDGET_SHIFT_X, y: $reservedPlace.y + TEXT_NODE_SIZE.height + WIDGET_SHIFT_Y }
      }
      const textNode = {
        id: block.id,
        type: 'text-node',
        position: position,
        data: block
      }
      $nodes = [...$nodes, textNode]
      // endX: width - Это хак, чтобы после ноды с текстом, все переходило на новую строку
      $reservedPlace = { x: 0, y: position.y, endX: width, endY: position.y + TEXT_NODE_SIZE.height}

      for (const widget of block.widgets) {
        let position
        position = calcPos()
        // if (widget.xPos === null || widget.yPos === null) {
        //   position = calcPos()
        //   await rpc.Dashboard.updateWidget(widget.id, { xPos: position.x, yPos: position.y })
        // } else {
        //   position = { x: widget.xPos, y: widget.yPos }
        // }

        const node = {
          id: widget.id,
          type: 'plot-node',
          position: position,
          data: widget
        }

        $reservedPlace = { x: position.x, y: position.y, endX: position.x + PLOT_SIZE.width, endY: position.y + PLOT_SIZE.height }
        $nodes = [...$nodes, node]
      }
    }
  }

  function calcPos() {
    if (!$reservedPlace) return { x: WIDGET_SHIFT_X, y: 0 }

    if ($reservedPlace.endX + PLOT_SIZE.width > width)
      return { x: WIDGET_SHIFT_X, y: $reservedPlace.endY + WIDGET_SHIFT_Y }
    else
      return { x: $reservedPlace.endX + WIDGET_SHIFT_X, y: $reservedPlace.y }
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
    panOnScroll={true}
    colorMode={$theme}
    translateExtent={[[47, 0], [1000, 10000]]}
    initialViewport={{x: 0, y: 0, zoom: 1}}
    minZoom="1"
    maxZoom="1"
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