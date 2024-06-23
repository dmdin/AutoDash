<script lang="ts">
  import Badge from '$lib/widgets/Badge.svelte'
  import { rpc } from '$root/routes'
  import { dashboard, nodes, readonly } from '../controller'

  export let id
  export let data: {
    data: {
      title: string,
      data: string
    },
    name: string
    id: string
    order: number
  }
  let type = data.data.type
  export let selected

  async function changePlot(type) {
    data.data.type = type;
    await rpc.Dashboard.updateWidget(data.id, { data: data.data });
  }

  const node = $nodes.find((n) => n.id === data.id)
  $: type = data.data.type
</script>

<Badge title={data?.data?.title} value={data?.data?.data} />
