<script lang="ts">
  import UilPlus from '~icons/uil/plus';
  const onDragStart = (event: DragEvent, nodeType: string) => {
    if (!event.dataTransfer) {
      return null;
    }

    event.dataTransfer.setData('application/svelteflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };
</script>

<div class="w-full pt-4">
  <button class="btn flex btn-secondary mx-auto cursor-grab"
    on:dragstart={(event) => onDragStart(event, 'text-node')}
    draggable={true}
  >
    <UilPlus/>
    Текстовый блок
  </button>
</div>
