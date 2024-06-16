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
  let focused = true
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

  $: if (data?.data?.text === '') data.data.text = 'Ваш текст'
</script>

<div class="relative box-content {selected ? 'shadow-lg' : ''}" on:dblclick={editText}>
<!--  <textarea bind:value={data.data.text} class="border-l border-neutral pl-2 max-w-[900px] bg-base-100 resize-y"/>-->
  <p class="border-l border-neutral pl-2 pr-5 max-w-[900px] bg-base-100">{@html data.data.text.replaceAll('\n', '<br/>') || 'Ваш текст'}</p>
  {#if focused}
    <textarea use:init class="absolute top-0 left-0 min-h-1 w-full h-full pl-2 resize-none {focused ? 'cursor-text' : 'cursor-grab outline-none select-none'}" rows="1" placeholder='Ваш текст' bind:value={data.data.text} bind:this={textarea} readonly={focused ? '' : 'readonly'}
              on:input={handleInput}
              on:blur={finishEdit}></textarea>
  {/if}
</div>
