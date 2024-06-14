<script lang="ts">
  import { toPng } from 'html-to-image';
  // import html2pdf from 'html2pdf.js'
  import html2canvas from 'html2canvas-pro'
  import { Panel, getNodesBounds, getViewportForBounds, useNodes } from '@xyflow/svelte';
  import { jsPDF } from "jspdf"

  const nodes = useNodes();

  const imageWidth = 1920;
  const imageHeight = 1080;

  async function handleClick() {
    // const module = await import('html2pdf.js')
    // const html2pdf = module.default
    const nodesBounds = getNodesBounds($nodes);
    const viewport = getViewportForBounds(nodesBounds, imageWidth, imageHeight, 0.5, 2.0, 0.2);

    const viewportDomNode = document.querySelector<HTMLElement>('.svelte-flow__viewport')!;

    if (viewport) {
      html2canvas(viewportDomNode).then(canvas => {
        let imgData = canvas.toDataURL("image/jpeg", 1.0)
        let pdf = new jsPDF()

        pdf.addImage(canvas, 'JPEG', 0, 0);
        pdf.save("download.pdf")
      })
      // toPng(viewportDomNode, {
      //   backgroundColor: '#1a365d',
      //   width: imageWidth,
      //   height: imageHeight,
      //   style: {
      //     width: `${imageWidth}px`,
      //     height: `${imageHeight}px`,
      //     transform: `translate(${viewport.x}px, ${viewport.y}px) scale(${viewport.zoom})`
      //   }
      // }).then((dataUrl) => {
      //   let pdf = new jsPDF()
      //     pdf.addImage(dataUrl, 'JPEG', 0, 0, imageWidth, imageHeight);
      //     pdf.save("download.pdf")
      //   const link = document.createElement('a');
      //   link.download = 'svelte-flow.png';
      //   link.href = dataUrl;
      //   link.click();
      // });
    }
  }
</script>

<Panel position="top-right">
  <button on:click={handleClick}>Download Image</button>
</Panel>