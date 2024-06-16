<script lang="ts">
	import { CHART_HEIGHT, CHART_WIDTH } from '$lib/charts/constants'
	import { ImageRun, Packer, Paragraph, TextRun } from 'docx';
	import pkg from 'file-saver';
	const { saveAs } = pkg;
	import * as docx from 'docx';
	import { toPng } from 'html-to-image';
	// import html2pdf from 'html2pdf.js'
	import PhFilePdf from '~icons/ph/file-pdf';
	import PhMicrosoftExcelLogoFill from '~icons/ph/microsoft-excel-logo-fill';
	import PhMicrosoftWordLogoFill from '~icons/ph/microsoft-word-logo-fill';
	import PhExport from '~icons/ph/export';
	import PhFilePng from '~icons/ph/file-png'
	import html2canvas from 'html2canvas-pro';
	import { Panel, getNodesBounds, getViewportForBounds, useNodes } from '@xyflow/svelte';
	import { jsPDF } from 'jspdf';
	import { dashboard, nodes } from '../controller';
	import { getContext } from 'svelte';
	import Badge from '$root/lib/widgets/Badge.svelte';
	import { get } from 'svelte/store';
	import { rpc } from '$root/routes';
	import { ExportType } from '../types';
	import { Buffer } from 'buffer'

	let imageWidth = 900 * 2;
	let imageHeight = 662 * 3 * 2

	async function handleClick() {
		// const module = await import('html2pdf.js')
		// const html2pdf = module.default
		const nodesBounds = getNodesBounds($nodes);
		const viewport = getViewportForBounds(nodesBounds, nodesBounds.width, nodesBounds.height, 0.5, 2, 0.2);
		const viewportDomNode = document.querySelector<HTMLElement>('.svelte-flow__viewport')!;
		imageWidth = nodesBounds.width
		imageHeight = nodesBounds.height
    if (viewport) {
      // html2canvas(viewportDomNode).then(canvas => {
      //   let imgData = canvas.toDataURL("image/jpeg", 1.0)
      //   let pdf = new jsPDF('l', 'px', [imageHeight, imageWidth])
      //
      //   pdf.addImage(canvas, 'JPEG', 0, 0, imageWidth, imageHeight);
      //   pdf.save("download.pdf")
      // })
      toPng(viewportDomNode, {
        backgroundColor: '#FFFFFF',
				quality: 1,
        width: imageWidth,
        height: imageHeight,
        style: {
          width: `${imageWidth}px`,
          height: `${imageHeight}px`,
					transform: `scale(${viewport.zoom})`
        }
      }).then((dataUrl) => {
        let pdf = new jsPDF('p', 'px', [imageWidth, imageHeight])
        pdf.addImage(dataUrl, 'PNG', 0, 0, imageWidth, imageHeight);
        pdf.save("download.pdf")
      });
    }
  }

  function sortByCords(points) {
    return points.sort((a, b) => {
      const distanceA = Math.sqrt(a.position.x ** 2 + a.position.y ** 2);
      const distanceB = Math.sqrt(b.position.x ** 2 + b.position.y ** 2);
      return distanceA - distanceB;
    });
}

	async function downloadExcel() {
    const sortedNodes = sortByCords(structuredClone($nodes))
		const file = await rpc.Dashboard.exportFile(ExportType.Excel, sortedNodes);
		const unit8 = new Uint8Array(file.data);
		const url = URL.createObjectURL(new Blob([unit8], { type: 'application/vnd.ms-excel' }));
		const a = document.createElement('a');
		a.href = url;
		a.download = 'example.xlsx';
		document.body.appendChild(a);
		a.click();

		// Очистка
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}

  async function generateWord() {
    let children = []
		for (const node of $nodes) {
			if (node.type === 'text-node')
				children = [...children, genTextNode(node.data.data.text)]
			else if (node.type === 'block-node') {
				console.log(node)
				children = [...children, genTextNode(node.data.name, true, 30)]
			}
			else if (node.type === 'plot-node' && node.svgUrl) {
				children = [...children, await genPlotNode(node.svgUrl)]
			}

		}
    const doc = new docx.Document({
      sections: [
        {
          properties: {},
          children
        }]
    });

		docx.Packer.toBlob(doc).then(async (blob) => {
			saveAs(blob, 'report.docx')
		});
	}

	function genTextNode(text, bold = false, size=20) {
		return new Paragraph({ alignment: 'both', children: [ new TextRun({text, bold, size})]})
  }

	async function genPlotNode(svgUrl) {
		const buffer = await rpc.Dashboard.getImageBuffer(svgUrl)
		return new Paragraph({ alignment: 'center', children: [
				new ImageRun({
					data: buffer.data,
					transformation: {
						width: 276,
						height: 186,
					},
				})
			]});
	}

	function generateImage() {
		const nodesBounds = getNodesBounds($nodes);
		console.log(nodesBounds)
		const viewport = getViewportForBounds(nodesBounds, nodesBounds.width, nodesBounds.height, 0.5, 2, 0.2);
		console.log(viewport)
		const viewportDomNode = document.querySelector<HTMLElement>('.svelte-flow__viewport')!;
		imageWidth = nodesBounds.width
		imageHeight = nodesBounds.height
		if (viewport) {
			toPng(viewportDomNode, {
				backgroundColor: '#FFFFFF',
				quality: 1,
				width: imageWidth,
				height: imageHeight,
				style: {
					width: `${imageWidth}px`,
					height: `${imageHeight}px`,
					transform: `scale(${viewport.zoom})`
				}
			}).then((dataUrl) => {
				const a = document.createElement('a');
				a.href = dataUrl;
				a.download = 'report.png';
				document.body.appendChild(a);
				a.click();
			});
		}
	}
</script>

<details class="dropdown">
	<summary class="btn btn-secondary w-full"><PhExport /> Экспорт</summary>
	<div class="mx-auto p-2 shadow bg-base-100 rounded-box grid grid-cols-2 grid-rows-2 gap-2">
		<button class="btn btn-sm text-lg" on:click={generateImage}><PhFilePng/></button>
		<button class="btn btn-sm text-lg" on:click={handleClick}><PhFilePdf /></button>
		<button class="btn btn-sm text-lg" on:click={downloadExcel}><PhMicrosoftExcelLogoFill /></button>
		<button class="btn btn-sm text-lg" on:click={generateWord}><PhMicrosoftWordLogoFill /></button>
	</div>
</details>
