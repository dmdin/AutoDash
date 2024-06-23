import { db } from '$repo/db';
import { desc } from 'drizzle-orm'
import { dashboards } from '$schema'

export async function load() {
	return {
		dashboards: await db.query.dashboards.findMany({
			with: {template: true, author: true},
			orderBy: desc(dashboards.createdAt)
		})
	};
}
