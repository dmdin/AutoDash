<script>
  import { model } from '$client/stores'
  import { env } from '$env/dynamic/public'
  import { rpc } from '$root/routes'
  import { onMount, setContext } from 'svelte'
  import Toolbar from '$root/routes/dashboards/[dashId]/ui/Toolbar.svelte'
  import Block from './ui/Block.svelte'
  import DownloadButton from './ui/DownloadButton.svelte'
  import { dashboard, generatedBlockNumber, readonly } from './controller'
  import { Circle } from 'svelte-loading-spinners'
	import { get, writable } from 'svelte/store';
  import TdesignShare from '~icons/tdesign/share';
  import { dashId, generating } from './controller'
  export let data
  let loading = true
  let ws
  let receiveTimeout
  const blocksImages = writable([])

  onMount(async () => {
    loading = true
    $dashboard = data.dashboard
    if (!$dashboard.generated) {
      $generating = true
      $readonly = true
      initSockets()

      // const parsed = {
      //   block_name: "Блок 1: Основная информация о компании: «Визитная карточка»",
      //   widgets: [
      //     {
      //       type: "text",
      //       title: "Год основания",
      //       sources: [
      //         {
      //           url: "chat.openai.com",
      //           text: "Information was gathered from External Knowledge Base (ChatGPT)"
      //         }
      //       ],
      //       text: "Компания была основана в 2004 году и с тех пор успешно занимается производством и продажей пылесосов по всему миру."
      //     },
      //     {
      //       type: "badge",
      //       title: "Выручка за последний год",
      //       sources: [
      //         {
      //           url: "chat.openai.com",
      //           text: "Information was gathered from External Knowledge Base (ChatGPT)"
      //         }
      //       ],
      //       data: 2500000
      //     },
      //     {
      //       type: "bar",
      //       title: "Объём производства стали за последний год в тоннах",
      //       sources: [
      //         {
      //           url: "chat.openai.com",
      //           text: "Information was gathered from External Knowledge Base (ChatGPT)"
      //         }
      //       ],
      //       categories: [
      //         "Компания A",
      //         "Компания B",
      //         "Компания C",
      //         "Компания D"
      //       ],
      //       unit: "тонн",
      //       data: [
      //         50000,
      //         75000,
      //         60000,
      //         90000
      //       ]
      //     }
      //   ]
      // }
      // parsed.name = parsed.block_name
      // parsed.order = $generatedBlockNumber
      // parsed.widgets = parsed.widgets.map((widget, ind) => ({ order: ind, data: widget, id: ind }))
      // $dashboard.blocks = [...$dashboard.blocks, parsed]
      // $generatedBlockNumber = $generatedBlockNumber + 1
      // console.log($dashboard)
      // await rpc.Dashboard.saveGenerated($dashId, $dashboard.blocks)
    }
    // if ($generating) initSockets()

    loading = false
    console.log($dashboard)
  })

  function initSockets() {
    ws = new WebSocket(env.PUBLIC_REPORT_ENDPOINT);
    ws.onopen = function () {
      console.log('Соединение установлено.')
      ws.send(JSON.stringify({ "report_theme": $dashboard.template.topic.replaceAll('\t', ''),
        "report_text": $dashboard.template.description.replaceAll('\t', ''),
        "model_name": 'gpt-4o',
        "urls": []}))
    };
    ws.onerror = err => {
      alert('Произошла ошибка генерации отчета(')
    }
    ws.onclose = event => {
      console.log('Подключение закрыто')
    }
    ws.onmessage = async function (event) {
      console.log(event)
      if (receiveTimeout) clearInterval(receiveTimeout)
      if (event.data) {
        if (event.data === 'finish') {
          console.log('finish')
          await rpc.Dashboard.saveGenerated($dashId, $dashboard.blocks)
          $generating = false
          $readonly = false
          ws.close()
          return
        }
        const parsed = JSON.parse(event.data)
        console.log(parsed)
        parsed.order = $generatedBlockNumber
        parsed.name = parsed.block_name
        parsed.widgets = parsed.widgets.map((widget, ind) => ({ order: ind, data: widget, id: ind }))
        $dashboard.blocks = [...$dashboard.blocks, parsed]
        $generatedBlockNumber = $generatedBlockNumber + 1
      }

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
    <div class="fixed right-3 bottom-3 p-5 bg-base-100 border rounded-xl flex items-center gap-2 shadow-2xl"><Circle color="oklch(var(--n))" size="25" /> Ожидайте, производится генерация отчета... <br/>(Генерация отчета может занять до 10 минут)</div>
  {/if}
{/if}

