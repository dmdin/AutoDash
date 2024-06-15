import { db } from '$repo/db'
import type { TableType } from '$repo/db/utils'
import { dashboards, widgets } from '$schema'
import { rpc } from '@chord-ts/rpc'
import { eq } from 'drizzle-orm'

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
      }
    })
  }

  @rpc()
  async updateWidget(id: string, data: {data?: object, xPos?: number, yPos?: number, width?:number, height?: number}) {
    await db
      .update(widgets)
      .set(data)
      .where(eq(widgets.id, id))
  }
}