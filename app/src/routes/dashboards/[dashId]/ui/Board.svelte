<script>
  import { CHART_HEIGHT, CHART_WIDTH } from '$lib/charts/constants'
  import { ChartType } from '$lib/charts/types'
  import { rpc } from '$root/routes'
  import { WIDGET_SHIFT_X, WIDGET_SHIFT_Y } from '$root/routes/dashboards/[dashId]/constants'
  import BadgeNode from '$root/routes/dashboards/[dashId]/ui/BadgeNode.svelte'
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
  import {
    nodes,
    edges,
    dashboard,
    reservedPlace,
    dashId,
    readonly,
    generatedBlockNumber,
    generating,
  } from '../controller'
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
    'block-node': BlockNode,
    'badge-node': BadgeNode
  }

  onMount(() => {
    // createNodes()
  })

  $: if ($generatedBlockNumber) createNodes()

  async function createNodes() {
    console.log('here')
    if (!$dashboard) return
    console.log($dashboard)

    if ($dashboard.template.topic) {
      const topicNode = {
        id: $dashboard.template.id,
        type: 'block-node',
        position: { x: WIDGET_SHIFT_X, y: WIDGET_SHIFT_Y },
        data: { name: $dashboard.template.topic}
      }
      await addNode(topicNode, width)
    }
    const blocksToCreate = $generating ? [$dashboard.blocks[$generatedBlockNumber - 2]] : $dashboard.blocks
    for (const block of blocksToCreate.sort((a, b) => a.order - b.order)) {
      const blockId = $generating || !block.id ? (await rpc.Dashboard.createBlock($dashId, block)).id : block.id
      if (block?.name && block?.name !== '') {
        let position = { x: WIDGET_SHIFT_X, y: WIDGET_SHIFT_Y }
        if ($reservedPlace) {
          position = { x: WIDGET_SHIFT_X, y: $reservedPlace.endY + TEXT_NODE_SIZE.height + WIDGET_SHIFT_Y }
        }
        const textNode = {
          id: blockId,
          type: 'block-node',
          position: position,
          data: block
        }
        console.log(textNode)
        await addNode(textNode, width) // Тут добавляем extra bound, чтобы виджеты не заходили на эту же линию
      }
      for (const widget of block.widgets.sort((a, b) => a.order - b.order)) {
        let position
        // position = calcPos()
        if ($generating) {
          position = calcPos()
          widget.xPos = position.x
          widget.yPos = position.y
          console.log(widget)
          $dashboard = $dashboard
          console.log(position)
          // await rpc.Dashboard.updateWidget(widget.id, { xPos: position.x, yPos: position.y })
        } else {
          position = { x: widget.xPos, y: widget.yPos }
        }

        const widgetId = $generating || !widget.id ? (await rpc.Dashboard.saveWidget(blockId, widget)).id : widget.id
        let nodeType = 'text-node'
        switch (widget.data.type) {
          case 'text':
            nodeType = 'text-node'
            break
          case 'badge':
            nodeType = 'badge-node'
            break
          default:
            nodeType = 'plot-node'
        }
        const node = {
          id: widgetId,
          type: nodeType,
          position: position,
          data: widget,
          svgUrl: '',
        }
        console.log(node)
        console.log(node)
        await addNode(node, nodeType === 'plot-node' ? 0 : width) // 🤪🤪🤪🤪🤪
      }
    }

    console.log($nodes)
  }

  async function addNode(node, extraBoundX = 0, extraBoundY = 0) {
    $nodes = [...$nodes, node]
    const bounds = await getNodeBounds($nodes.length - 1)
    if ($reservedPlace) {
      $reservedPlace = { x: bounds.x, y: bounds.y > $reservedPlace.y ? bounds.y : $reservedPlace.y,
        endX: bounds.x + bounds.width + extraBoundX,
        endY: bounds.y + bounds.height + extraBoundY > $reservedPlace.endY ? bounds.y + bounds.height + extraBoundY : $reservedPlace.endY }
    } else
      $reservedPlace = { x: bounds.x, y: bounds.y,
        endX: bounds.x + bounds.width + extraBoundX,
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
