<script lang="ts">
  import { nodes } from '$root/routes/dashboards/[dashId]/controller'
  import { rpc} from '$root/routes'

  export let data: {
    data: {
      text: string
    }
  }
  export let selected
  export let id
  export let dragHandle
  let focused = false
  let textarea
  $: console.log(data)
  $: console.log(focused)

  function init(el) {
    textarea = el
    textarea.style.height = '1px'
    textarea.style.height = `${textarea.scrollHeight}px`
    el.focus()
  }

  async function handleInput() {
    textarea.style.height = '1px'
    textarea.style.height = `${textarea.scrollHeight}px`
    await rpc.Dashboard.updateWidget(id, { data: data.data })
  }

  function editText() {
    focused = true
    const node = $nodes?.find(node => node.id === id)
    node.draggable = false
    $nodes = $nodes
    textarea?.focus()
  }

  function finishEdit() {
    const node = $nodes?.find(node => node.id === id)
    node.draggable = true
    $nodes = $nodes
    focused = false
  }
</script>

<div class="flex py-2 {selected ? 'shadow-lg' : ''}" on:dblclick={editText}>
<!--  <textarea bind:value={data.data.text} class="border-l border-neutral pl-2 max-w-[900px] bg-base-100 resize-y"/>-->
  <p class="border-l border-neutral pl-2 max-w-[900px] bg-base-100">{@html data.data.text.replaceAll('\n', '<br/>')}</p>
  {#if focused}
    <textarea use:init class="absolute top-0 left-0 w-full h-full pl-2 {focused ? 'cursor-text' : 'cursor-grab outline-none select-none'}" bind:value={data.data.text} bind:this={textarea} unselectable="on" readonly={focused ? '' : 'readonly'}
              on:input={handleInput}
              on:blur={finishEdit}></textarea>
  {/if}
</div>
