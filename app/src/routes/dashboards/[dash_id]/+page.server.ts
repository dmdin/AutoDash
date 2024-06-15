import { db } from '$repo/db'
import { blocks, dashboards, widgets } from '$schema'
import { error, json } from '@sveltejs/kit'
import { eq } from 'drizzle-orm'

export async function load({ params }) {
  const dashboard = await db.query.dashboards.findFirst({
    where: eq(dashboards.id, params.dash_id),
    with: {
      blocks: {
        with: {
          widgets: true
        }
      }
    }
  })

  // if (!dashboard) throw error(404, 'Такой отчет не найден(')

  return dashboard
}