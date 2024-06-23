<script>
  import { CHART_HEIGHT, CHART_WIDTH } from '$lib/charts/constants'
  import { ChartType } from '$lib/charts/types'
  import { rpc } from '$root/routes'
  import { WIDGET_SHIFT_X, WIDGET_SHIFT_Y } from '$root/routes/dashboards/[dashId]/constants'
  import TextNode from '$root/routes/dashboards/[dashId]/ui/TextNode.svelte'
  import { theme } from '$stores'
  import { onMount, tick } from 'svelte'
  import { writable } from 'svelte/store';
  import {
    SvelteFlow,
    Controls,
    Background,
    BackgroundVariant,
    MiniMap, getNodesBounds,
  } from '@xyflow/svelte'
  import '@xyflow/svelte/dist/style.css';
  import BlockNode from './BlockNode.svelte'
  import ContextMenu from './ContextMenu.svelte'
  import PlotNode from './PlotNode.svelte'
  import { nodes, edges, dashboard, reservedPlace, dashId, readonly } from '../controller'
  import { useNodesInitialized } from '@xyflow/svelte'
  import { useSvelteFlow } from '@xyflow/svelte'

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

    if ($dashboard.template.topic) {
      const topicNode = {
        id: $dashboard.template.id,
        type: 'block-node',
        position: { x: WIDGET_SHIFT_X, y: WIDGET_SHIFT_Y },
        data: { name: $dashboard.template.topic}
      }
      await addNode(topicNode, width)
    }

    for (const block of $dashboard.blocks) {
      if (block.name !== '') {
        let position = { x: WIDGET_SHIFT_X, y: WIDGET_SHIFT_Y }
        if ($reservedPlace) {
          position = { x: WIDGET_SHIFT_X, y: $reservedPlace.y + TEXT_NODE_SIZE.height + WIDGET_SHIFT_Y }
        }
        const textNode = {
          id: block.id,
          type: 'block-node',
          position: position,
          data: block
        }

        await addNode(textNode, width) // Тут добавляем extra bound, чтобы виджеты не заходили на эту же линиюy
      }

      for (const widget of block.widgets.sort((a, b) => a.order - b.order)) {
        let position
        if (widget.xPos === null || widget.yPos === null) {
          position = calcPos()
          await rpc.Dashboard.updateWidget(widget.id, { xPos: position.x, yPos: position.y })
        } else {
          position = { x: widget.xPos, y: widget.yPos }
        }

        const nodeType = widget.data.type === 'text' ? 'text-node' : 'plot-node'
        const node = {
          id: widget.id,
          type: nodeType,
          position: position,
          data: widget,
          svgUrl: '',
        }

        await addNode(node, nodeType === 'text-node' ? width : 0) // 🤪🤪🤪🤪🤪
      }
    }

    console.log($nodes)
  }

  async function addNode(node, extraBoundX = 0, extraBoundY = 0) {
    $nodes = [...$nodes, node]
    const bounds = await getNodeBounds($nodes.length - 1)
    $reservedPlace = { x: bounds.x, y: bounds.y, endX: bounds.x + bounds.width + extraBoundX,
      endY: bounds.y + bounds.height + extraBoundY }
  }

  async function getNodeBounds(ind) {
    return new Promise((resolve) => {
      const timer = setInterval(() => {
        const bounds = getNodesBounds([$nodes[ind]])
        if (bounds.width !== 0) {
          clearInterval(timer)
          resolve(bounds)
        }
      }, 10)
    })

  }

  function calcPos() {
    if (!$reservedPlace) return { x: WIDGET_SHIFT_X, y: 0 }

    if ($reservedPlace.endX + CHART_WIDTH > width)
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

  const { screenToFlowPosition } = useSvelteFlow()
  const onDragOver = (event) => {
    event.preventDefault();

    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = 'move';
    }
  };

  const onDrop = async (event) => {
    event.preventDefault();

    if (!event.dataTransfer) {
      return null;
    }

    const type = event.dataTransfer.getData('application/svelteflow');

    const position = screenToFlowPosition({
      x: event.clientX,
      y: event.clientY
    });

    const widget = await rpc.Dashboard.createWidget({ blockId: $dashboard?.blocks[0].id, data: { type: 'text', text: 'Введите текст'},
    xPos: position.x, yPos: position.y, order: 100000})
    const newNode = {
      id: widget.id,
      type,
      position,
      data: { data: { type: 'text', text: 'Введите текст' }},
    }

    $nodes.push(newNode);
    $nodes = $nodes;
  }

  async function deleteNode(params) {
    for (const node of params.nodes) {
      await rpc.Dashboard.deleteWidget(node.id)
    }
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
    nodesDraggable={!$readonly}
    minZoom="1"
    maxZoom="1"
    on:dragover={onDragOver} on:drop={onDrop}
    on:selectioncontextmenu={handleContextMenu}
    on:nodecontextmenu={handleContextMenu}
    on:paneclick={handlePaneClick}
    on:nodedragstop={saveWidget}
    ondelete={deleteNode}
  >
    {#if !$readonly}
      <Background variant={BackgroundVariant.Dots} />
    {/if}
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
