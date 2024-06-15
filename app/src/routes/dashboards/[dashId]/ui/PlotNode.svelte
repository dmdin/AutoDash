<script lang="ts">
  import { PieChart } from '$lib/charts'
  import { onMount, SvelteComponent } from 'svelte'
  import GgChart from '~icons/gg/chart'
  import LucideLineChart from '~icons/lucide/line-chart'
  import MageChartFill from '~icons/mage/chart-fill'

  export let data: {
    component: typeof SvelteComponent,
    name: string,
    id: string
  }
  export let selected
</script>

<div class="border-2 rounded-md p-2 bg-base-100 group {selected ? 'border-primary' : ''}">
  <div class="absolute right-0 top-[-32px] hidden group-hover:flex hover:flex text-xs gap-1 py-2">
    <button class="bg-primary rounded p-1"><GgChart/></button>
    <button class="bg-primary rounded p-1"><LucideLineChart/></button>
    <button class="bg-primary rounded p-1"><MageChartFill/></button>
  </div>
  <PieChart />
</div>