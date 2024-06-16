<script>
  import { onMount, setContext } from 'svelte'
  import { Board } from './ui'
  import Block from './ui/Block.svelte'
  import PhFilePdf from '~icons/ph/file-pdf'
  import PhMicrosoftExcelLogoFill from '~icons/ph/microsoft-excel-logo-fill'
  import PhMicrosoftWordLogoFill from '~icons/ph/microsoft-word-logo-fill'
  import DownloadButton from './ui/DownloadButton.svelte'
  import { dashboard } from './controller'
  import { Circle } from 'svelte-loading-spinners'
	import { get, writable } from 'svelte/store';

  export let data
  let loading = true
  console.log(data)
  const blocksImages = writable([])

  onMount(() => {
    loading = true
    $dashboard = data.dashboard
    loading = false
  })

  setContext('blocksImages', blocksImages)
</script>


{#if loading}
  <div class="absolute w-full h-full flex justify-center items-center">
    <Circle color="oklch(var(--p))" size="80" />
  </div>
{:else}
  <div class="w-full flex-1 grid grid-cols-8">
    <div class="col-span-1"></div>
    <div class="mx-auto h-full col-span-6">
      {#each $dashboard.blocks as block}
        <Block data={block} />
      {/each}
    </div>
    <div class="col-span-1 pt-4">
      <DownloadButton/>
    </div>
  </div>
{/if}

