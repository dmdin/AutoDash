<script>
  export let data
  export let selected
  $: console.log(selected)
  $: console.log($$props)
</script>

<div class="border-2 rounded-md p-2 bg-base-100 {selected ? 'border-primary' : 'border-neutral'}">
  Графичек тут__)
  {data.selected}
</div>