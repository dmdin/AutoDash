import ExcelJS from 'ExcelJS';
import sharp from 'sharp';

async function changeFormat(encodedSVG: string) {
	const svgData = encodedSVG.split(',')[1];
	const decodedSVG = decodeURIComponent(svgData);
	const svgBuffer = Buffer.from(decodedSVG);

	return sharp(svgBuffer).png().toBuffer();
}

// data
// height
// width
// xPos
// yPos
async function processWidgets(
	workbook: ExcelJS.Workbook,
	blockIndex: number,
	blocksImages: SvelteStore<unknown[]>,
	widgets: unknown[]
) {
	const worksheet = workbook.getWorksheet('Блок 1.');
  console.log(worksheet)
	const widgetsImages = blocksImages[blockIndex];

	await Promise.all(
		widgets.map(async (w, i) => {
			const url = widgetsImages[i];
			if (!url || i > 0) return;

			const buff = await changeFormat(url);
			const imgId = await workbook.addImage({
				buffer: buff,
				extension: 'png'
			});
      console.log(imgId)
			await worksheet?.addImage(imgId, {
        tl: { col: 0, row: 0 },
        ext: { width: 400, height: 200 },
        br: { col: 5, row: 5 },
      });
		})
	);
}

export async function getExcelFile(name: string, blocks: unknown[], blocksImages: unknown[]) {
	const workbook = new ExcelJS.Workbook();

	const blocksPrepared = blocks.slice().sort((a, b) => a.order - b.order);
	workbook.addWorksheet(blocksPrepared[0].name);

	await processWidgets(workbook, 0, blocksImages, blocksPrepared[0].widgets);
	// blocksPrepared.forEach(async (b, i) => {

	// 	// order
	// 	// name
	// 	// widgets
	// });
	return await workbook.xlsx.writeBuffer();
}
