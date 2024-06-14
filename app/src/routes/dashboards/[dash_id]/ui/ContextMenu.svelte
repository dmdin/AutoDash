<script lang="ts">
  import { useEdges, useNodes } from '@xyflow/svelte';

  export let onClick: () => void;
  export let id: string;
  export let top: number | undefined;
  export let left: number | undefined;
  export let right: number | undefined;
  export let bottom: number | undefined;

  const nodes = useNodes();
  const edges = useEdges();

  function duplicateNode() {
    const node = $nodes.find((node) => node.id === id);
    if (node) {
      $nodes.push({
        ...node,
        // You should use a better id than this in production
        id: `${id}-copy${Math.random()}`,
        position: {
          x: node.position.x,
          y: node.position.y + 50
        }
      });
    }
    $nodes = $nodes;
  }

  function deleteNode() {
    $nodes = $nodes.filter((node) => node.id !== id);
    $edges = $edges.filter((edge) => edge.source !== id && edge.target !== id);
  }
</script>

<div
  style="top: {top}px; left: {left}px;"
  class="absolute w-80 h-32 bg-base-100 flex gap-1.5 p-2 rounded-md flex-col z-50 border-2 shadow-xl">
  <textarea class="flex-1 outline-0 border border-neutral/20 rounded-md px-2 py-1" placeholder="Уточните запрос"/>
  <button class="btn btn-sm">Перегенерировать</button>
</div>