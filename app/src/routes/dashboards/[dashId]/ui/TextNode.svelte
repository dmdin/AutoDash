<script lang="ts">
  export let data: {
    data: {
      text: string
    }
  }
  export let selected

  $: console.log(data)
</script>

<div class="py-2 pr-2 {selected ? 'shadow-lg' : ''}">
  <p class="border-l border-neutral  pl-2 max-w-[900px] bg-base-100">{data.data.text}</p>
</div>
