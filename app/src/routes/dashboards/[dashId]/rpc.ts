import { db, takeUniqueOrThrow } from '$repo/db';
import type { TableType } from '$repo/db/utils';
import { blocks, dashboards, widgets } from '$schema';
import { depends, rpc } from '@chord-ts/rpc';
import { asc, desc, eq } from 'drizzle-orm';
import { ExportType, type ExportData } from './types';
import { getExcelFile, changeFormat } from '$root/lib/utils/export';

interface DashboardType {
	blocks: { widgets: { data: object }[] }[]
}

interface Block {
	name: string,
	widgets: Widget[]
}

interface Widget {
	data: object
}
export class Dashboard {
	@depends()
	ctx!: { user: { id: string } };

	@rpc()
	async saveGenerated(dashId: string, blocksData: Block[]) {
		// console.log(blocksData)
		// const insertedBlocks = await db
		// 	.insert(blocks)
		// 	.values(
		// 		blocksData.map((block, ind) => ({
		// 			name: block.name,
		// 			dashboardId: dashId,
		// 			order: ind
		// 		}))
		// 	)
		// 	.returning();
		//
		// const widgetsValues = blocksData
		// 	.map((block, blockInd) =>
		// 		block.widgets.map((widget, widgetInd) => ({
		// 			blockId: insertedBlocks[blockInd].id,
		// 			data: widget.data,
		// 			order: widgetInd,
		// 			xPos: widget.xPos,
		// 			yPos: widget.yPos
		// 		}))
		// 	)
		// 	.flat(1);
		// await db.insert(widgets).values(widgetsValues).returning()
		await db.update(dashboards).set({ generated: true }).where(eq(dashboards.id, dashId))
	}

	@rpc()
	async createBlock(dashId, block) {
		return db
			.insert(blocks)
			.values({
					name: block.name,
					dashboardId: dashId,
					order: block.order
				})
			.returning()
			.then(takeUniqueOrThrow)
	}

	@rpc()
	async saveWidget(blockId, widget) {
		return db.insert(widgets).values({
			blockId: blockId,
			data: widget.data,
			order: widget.order,
			xPos: widget.xPos,
			yPos: widget.yPos})
			.returning()
			.then(takeUniqueOrThrow)
	}

	@rpc()
	async get(dashId: string) {
		return await db.query.dashboards.findFirst({
			where: eq(dashboards.id, dashId),
			with: {
				template: true,
				blocks: {
					with: {
						widgets: true
					}
				}
			},
			orderBy: [desc(blocks.order), desc(widgets.order)]
		});
	}

	@rpc()
	async delete(dashId: string) {
		return db.delete(dashboards).where(eq(dashboards.id, dashId)).returning()
	}

	@rpc()
	async deleteWidget(id: string) {
		await db.delete(widgets).where(eq(widgets.id, id))
	}

	@rpc()
	async exportFile(type: ExportType, nodes: unknown[]) {
		if (type === ExportType.Excel) {
			return await getExcelFile('Test', nodes);
		}

		if (type === ExportType.Word) {
		}

		if (type === ExportType.Pdf) {
		}
	}

  @rpc()
  async updateWidget(id: string, data: {data?: object, xPos?: number, yPos?: number, width?:number, height?: number}) {
    await db
      .update(widgets)
      .set(data)
      .where(eq(widgets.id, id))
  }

  @rpc()
  async createWidget({blockId, data, order, xPos, yPos, width, height}: {blockId: string, data: object, order: number, xPos?: number, yPos?: number, width?:number, height?: number} ) {
    return await db
      .insert(widgets)
      .values({blockId, data, order, xPos, yPos, width, height})
      .returning()
      .then(takeUniqueOrThrow)
  }

	@rpc()
	async getImageBuffer(svgUrl: string) {
		return changeFormat(svgUrl)
	}
}
