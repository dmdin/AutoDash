<script>
  import Toolbar from '$root/routes/dashboards/[dashId]/ui/Toolbar.svelte'
  import { onMount } from 'svelte'
  import { Board } from '../ui'
  import Block from '../ui/Block.svelte'
  import PhFilePdf from '~icons/ph/file-pdf'
  import PhMicrosoftExcelLogoFill from '~icons/ph/microsoft-excel-logo-fill'
  import PhMicrosoftWordLogoFill from '~icons/ph/microsoft-word-logo-fill'
  import DownloadButton from '../ui/DownloadButton.svelte'
  import { dashboard, readonly } from '../controller'
  import { Circle } from 'svelte-loading-spinners'
  import { showLayout } from '$root/routes'

  export let data
  let loading = true
  console.log(data)

  onMount(() => {
    $showLayout = false
    $readonly = true
    loading = true
    $dashboard = data.dashboard
    loading = false
  })
</script>


{#if loading}
  <div class="absolute w-full h-full flex justify-center items-center">
    <Circle color="oklch(var(--p))" size="80" />
  </div>
{:else}
  <div class="w-full flex-1 grid grid-cols-8">
    <div class="col-span-1"></div>
    <div class="mx-auto h-full col-span-6">
      <Block/>
    </div>
    <div class="col-span-1 pt-4">
      <DownloadButton/>
    </div>
  </div>
{/if}

