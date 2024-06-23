<script>
  import { model } from '$client/stores'
  import { env } from '$env/dynamic/public'
  import { onMount, setContext } from 'svelte'
  import Toolbar from '$root/routes/dashboards/[dashId]/ui/Toolbar.svelte'
  import { Board } from './ui'
  import Block from './ui/Block.svelte'
  import PhFilePdf from '~icons/ph/file-pdf'
  import PhMicrosoftExcelLogoFill from '~icons/ph/microsoft-excel-logo-fill'
  import PhMicrosoftWordLogoFill from '~icons/ph/microsoft-word-logo-fill'
  import DownloadButton from './ui/DownloadButton.svelte'
  import { dashboard } from './controller'
  import { Circle } from 'svelte-loading-spinners'
	import { get, writable } from 'svelte/store';
  import TdesignShare from '~icons/tdesign/share';
  import { dashId, generating } from './controller'

  export let data
  let loading = true
  let ws
  let receiveTimeout
  const blocksImages = writable([])

  onMount(() => {
    loading = true
    $dashboard = data.dashboard
    $generating = !$dashboard.generated
    initSockets()
    loading = false
    console.log($dashboard)
  })

  function initSockets() {
    ws = new WebSocket(env.PUBLIC_REPORT_ENDPOINT);
    ws.onopen = function () {
      console.log('Соединение установлено.')
      // ws.send(JSON.stringify({ "report_theme": "Анализ рынка пылесосов",
      //   "report_text": "Проанализируй рынок ",
      //   "model_name": "gpt-4o",
      //   "urls": {
      //     "urls": []
      //   }}))
    };

    ws.onmessage = function (event) {
      console.log(event)
      if (receiveTimeout) clearInterval(receiveTimeout);

      // receiveTimeout = setTimeout(() => {
      //   generating = false;
      // }, 300000);
      // description += event.data;
    }

    ws.onerror = err => {
      console.log(err)
    }
  }
</script>


{#if loading}
  <div class="absolute w-full h-full flex justify-center items-center">
    <Circle color="oklch(var(--p))" size="80" />
  </div>
{:else}
  <div class="w-full flex-1 grid grid-cols-8">
    <div class="col-span-1"><Toolbar/></div>
    <div class="mx-auto h-full col-span-6">
      <Block />
    </div>
    <div class="col-span-1 pt-4 flex flex-col gap-3 w-40">
      <a class="btn btn-secondary" target="_blank" href={`/dashboards/${$dashId}/share`}><TdesignShare/> Поделиться</a>
      <DownloadButton/>
    </div>
  </div>

  {#if $generating}
    <div class="fixed right-3 bottom-3 p-5 bg-base-100 border rounded-xl flex items-center gap-2 shadow-2xl"><Circle color="oklch(var(--n))" size="25" /> Ожидайте, производится генерация отчета...</div>
  {/if}
{/if}

