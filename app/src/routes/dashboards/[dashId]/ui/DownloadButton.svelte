<script lang="ts">
  import { toPng } from 'html-to-image';
  // import html2pdf from 'html2pdf.js'
  import PhFilePdf from '~icons/ph/file-pdf'
  import PhMicrosoftExcelLogoFill from '~icons/ph/microsoft-excel-logo-fill'
  import PhMicrosoftWordLogoFill from '~icons/ph/microsoft-word-logo-fill'
  import PhExport from '~icons/ph/export';

  import html2canvas from 'html2canvas-pro'
  import { Panel, getNodesBounds, getViewportForBounds, useNodes } from '@xyflow/svelte';
  import { jsPDF } from "jspdf"
  import { nodes } from '../controller'

  const imageWidth = 3600;
  const imageHeight = 2080;

  async function handleClick() {
    // const module = await import('html2pdf.js')
    // const html2pdf = module.default
    const nodesBounds = getNodesBounds($nodes)
    const viewport = getViewportForBounds(nodesBounds, imageWidth, imageHeight, 0.5, 2.0, 0.2)

    const viewportDomNode = document.querySelector<HTMLElement>('.svelte-flow__viewport')!

    if (viewport) {
      // html2canvas(viewportDomNode).then(canvas => {
      //   let imgData = canvas.toDataURL("image/jpeg", 1.0)
      //   let pdf = new jsPDF()
      //
      //   pdf.addImage(canvas, 'JPEG', 0, 0);
      //   pdf.save("download.pdf")
      // })
      toPng(viewportDomNode, {
        backgroundColor: '#FFFFFF',
        width: imageWidth,
        height: imageHeight,
        style: {
          width: `${imageWidth}px`,
          height: `${imageHeight}px`,
          transform: `translate(${viewport.x}px, ${viewport.y}px) scale(${viewport.zoom})`
        }
      }).then((dataUrl) => {
        // let pdf = new jsPDF()
        //   pdf.addImage(dataUrl, 'JPEG', 0, 0, imageWidth, imageHeight);
        //   pdf.save("download.pdf")
        const link = document.createElement('a');
        link.download = 'svelte-flow.png';
        link.href = dataUrl;
        link.click();
      });
    }
  }
</script>

<details class="dropdown">
  <summary class="m-1 btn btn-secondary"><PhExport/> Экспорт</summary>
  <div class="w-full mx-auto p-2 shadow bg-base-100 rounded-box flex gap-0.5">
    <button class="btn btn-sm text-lg" on:click={handleClick}><PhFilePdf/></button>
    <button class="btn btn-sm text-lg"><PhMicrosoftExcelLogoFill/></button>
    <button class="btn btn-sm text-lg"><PhMicrosoftWordLogoFill/></button>
  </div>
</details>