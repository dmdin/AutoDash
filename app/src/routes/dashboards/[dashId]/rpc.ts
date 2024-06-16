<<<<<<< HEAD
import { db } from '$repo/db';
import type { TableType } from '$repo/db/utils';
import { blocks, dashboards, widgets } from '$schema';
import { rpc } from '@chord-ts/rpc';
import { asc, desc, eq } from 'drizzle-orm';
import { ExportType, type ExportData } from './types';
import { getExcelFile } from '$root/lib/utils/export';
=======
import { db, takeUniqueOrThrow } from '$repo/db'
import type { TableType } from '$repo/db/utils'
import { blocks, dashboards, widgets } from '$schema'
import { rpc } from '@chord-ts/rpc'
import { asc, desc, eq } from 'drizzle-orm'
>>>>>>> b00ee1657ffeb9254243dd3bbff3bda0d31370e4

export class Dashboard {
	@rpc()
	async get(dashId: string) {
		return await db.query.dashboards.findFirst({
			where: eq(dashboards.id, dashId),
			with: {
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
	async updateWidget(
		id: string,
		data: { data?: object; xPos?: number; yPos?: number; width?: number; height?: number }
	) {
		await db.update(widgets).set(data).where(eq(widgets.id, id));
	}

<<<<<<< HEAD
	@rpc()
	async exportFile(type: ExportType, data: ExportData) {
		if (type === ExportType.Excel) {
      return await getExcelFile('Test', data.blocks, data.images)
		}

		if (type === ExportType.Word) {

		}

		if (type === ExportType.Pdf) {

		}
	}
}
=======
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
}
>>>>>>> b00ee1657ffeb9254243dd3bbff3bda0d31370e4
