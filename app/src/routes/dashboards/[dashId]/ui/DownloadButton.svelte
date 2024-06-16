<script lang="ts">
	import { Packer, Paragraph, TextRun } from 'docx';
	import pkg from 'file-saver';
	const { saveAs } = pkg;
	import * as docx from 'docx';
	import { toPng } from 'html-to-image';
	// import html2pdf from 'html2pdf.js'
	import PhFilePdf from '~icons/ph/file-pdf';
	import PhMicrosoftExcelLogoFill from '~icons/ph/microsoft-excel-logo-fill';
	import PhMicrosoftWordLogoFill from '~icons/ph/microsoft-word-logo-fill';
	import PhExport from '~icons/ph/export';
	import html2canvas from 'html2canvas-pro';
	import { Panel, getNodesBounds, getViewportForBounds, useNodes } from '@xyflow/svelte';
	import { jsPDF } from 'jspdf';
	import { dashboard, nodes } from '../controller';
	import { getContext } from 'svelte';
	import Badge from '$root/lib/widgets/Badge.svelte';
	import { get } from 'svelte/store';
	import { rpc } from '$root/routes';
	import { ExportType } from '../types';

	const imageWidth = 1080 * 2;
	const imageHeight = 662 * 2;

	async function handleClick() {
		// const module = await import('html2pdf.js')
		// const html2pdf = module.default
		const nodesBounds = getNodesBounds($nodes);
		const viewport = getViewportForBounds(nodesBounds, imageWidth, imageHeight, 0.5, 2.0, 0.2);

		const viewportDomNode = document.querySelector<HTMLElement>('.svelte-flow__viewport')!;

		if (viewport) {
			await HTMLtoDOCX(viewportDomNode).then((res) => console.log(res));
			// html2canvas(viewportDomNode).then(canvas => {
			//   let imgData = canvas.toDataURL("image/jpeg", 1.0)
			//   let pdf = new jsPDF('l', 'px', [imageHeight, imageWidth])
			//
			//   pdf.addImage(canvas, 'JPEG', 0, 0, imageWidth, imageHeight);
			//   pdf.save("download.pdf")
			// })
			// toPng(viewportDomNode, {
			//   backgroundColor: '#FFFFFF',
			//   width: imageWidth,
			//   height: imageHeight,
			//   style: {
			//     width: `${imageWidth}px`,
			//     height: `${imageHeight}px`
			//   }
			// }).then((dataUrl) => {
			//   // let pdf = new jsPDF('l', 'px', [imageHeight, imageWidth])
			//   // pdf.addImage(dataUrl, 'PNG', 0, 0, imageWidth, imageHeight);
			//   // pdf.save("download.pdf")
			//   const link = document.createElement('a');
			//   link.download = 'svelte-flow.png';
			//   link.href = dataUrl;
			//   link.click();
			// });
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

	function generateWord() {
		let children = [];
		for (const block of $dashboard.blocks) {
			const paragraph = genTextNode(block.name);
			children = [...children, paragraph];
			for (const widget of block.widgets) {
				if (widget.data.type === 'text') {
					children = [...children, genTextNode(widget.data.text)];
				}
			}
		}
		const doc = new docx.Document({
			sections: [
				{
					properties: {},
					children
				}
			]
		});

		docx.Packer.toBlob(doc).then(async (blob) => {
			saveAs(blob, 'example.docx');
		});
	}

	function genTextNode(text) {
		return new Paragraph({ children: [new TextRun({ text })] });
	}
</script>

<details class="dropdown">
	<summary class="m-1 btn btn-secondary"><PhExport /> Экспорт</summary>
	<div class="w-full mx-auto p-2 shadow bg-base-100 rounded-box flex gap-0.5">
		<button class="btn btn-sm text-lg" on:click={handleClick}><PhFilePdf /></button>
		<button class="btn btn-sm text-lg" on:click={downloadExcel}><PhMicrosoftExcelLogoFill /></button
		>
		<button class="btn btn-sm text-lg" on:click={generateWord}><PhMicrosoftWordLogoFill /></button>
	</div>
</details>
