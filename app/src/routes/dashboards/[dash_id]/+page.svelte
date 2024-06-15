<script>
  import { Board } from './ui'
  import Block from './ui/Block.svelte'

  export let data

  console.log(data)
</script>
<div class="w-full h-full">
  <div class="mx-auto max-w-[1080px] h-screen">
    <h2>Отчет</h2>
    <Block/>
  </div>
</div>
