<script>
  import { Board } from './ui'
  import Block from './ui/Block.svelte'
  import PhFilePdf from '~icons/ph/file-pdf'
  import PhMicrosoftExcelLogoFill from '~icons/ph/microsoft-excel-logo-fill'
  import PhMicrosoftWordLogoFill from '~icons/ph/microsoft-word-logo-fill'
  import DownloadButton from './ui/DownloadButton.svelte'

  export let data

  console.log(data)
</script>
<div class="w-full h-full grid grid-cols-8">
  <div class="col-span-1"></div>
  <div class="mx-auto h-screen col-span-6">
    <h2>Отчет</h2>
    <Block/>
  </div>
  <div class="col-span-1 pt-4">
    <DownloadButton/>
  </div>
</div>
