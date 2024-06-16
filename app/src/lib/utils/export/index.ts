import { rpc } from '@chord-ts/rpc';
import { text } from '@sveltejs/kit';
import ExcelJS from 'exceljs';
import sharp from 'sharp';

export async function changeFormat(encodedSVG: string) {
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
	const worksheet = workbook?.getWorksheet(1);
	console.log(blocksImages);
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
			console.log(imgId);
			await worksheet?.addImage(imgId, {
				tl: { col: 0, row: 0 },
				ext: { width: 400, height: 200 },
				br: { col: 5, row: 5 }
			});
		})
	);
}

function styleHeading(heading: any) {
	heading.font = {
		name: 'Calibri',
		size: 18,
		bold: true
	};

	heading.alignment = {
		horizontal: 'center',
		vertical: 'middle'
	};

	heading.border = {
		top: { style: 'thin', color: { argb: 'FF000000' } },
		left: { style: 'thin', color: { argb: 'FF000000' } },
		bottom: { style: 'thin', color: { argb: 'FF000000' } },
		right: { style: 'thin', color: { argb: 'FF000000' } }
	};
}

const WIDGET_TOP_OFFSET = 5;
const PLOT_GAP = 1;
const PLOT_WIDTH = [
	['B', 'F'],
	['H', 'L'],
  ['N', 'R'],
  ['T', 'X']
];
const PLOT_HEIGHT = 10;
const TEXT_HEIGHT = 3

export async function getExcelFile(fileName: string = 'Название отчета', nodes: unknown[]) {
	const workbook = new ExcelJS.Workbook();
	const sheet = workbook.addWorksheet(fileName);

	sheet.mergeCells('B2:X2');
	const heading = sheet.getCell('B2');
	heading.value = fileName;
	styleHeading(heading);

	let widgetsInLine = 0;
	let currentRowNumber = 5;
	for (const n of nodes) {
		if (n.svgUrl) {
			if (widgetsInLine > 3) {
				currentRowNumber += PLOT_HEIGHT + widgetsInLine;
				widgetsInLine = 0;
			}

			const startCell = `${PLOT_WIDTH[widgetsInLine][0]}${currentRowNumber}`;
			const endCell = `${PLOT_WIDTH[widgetsInLine][1]}${currentRowNumber + PLOT_HEIGHT}`;
      console.log(startCell, endCell, `\n\n\n`)
			sheet.mergeCells(`${startCell}:${endCell}`);

			const file = await changeFormat(n.svgUrl);
			const imgId = workbook.addImage({
				buffer: file,
				extension: 'png'
			});
			sheet.addImage(imgId, `${startCell}:${endCell}`);
			widgetsInLine += 1;
		}

		if (n.type === 'text-node') {
      if (widgetsInLine > 0) {
        widgetsInLine = 0
        currentRowNumber += PLOT_HEIGHT + PLOT_GAP * 2
      }
      console.log(`B${currentRowNumber}:X${currentRowNumber}`)
      sheet.mergeCells(`B${currentRowNumber}:X${currentRowNumber}`)
      const textCell = sheet.getCell(`B${currentRowNumber}`)
      textCell.value = n.data?.data?.text
      currentRowNumber += TEXT_HEIGHT * 2
		}
	}

	return await workbook.xlsx.writeBuffer();
}
