import { relations } from 'drizzle-orm'
import { pgTable, text, uuid } from 'drizzle-orm/pg-core'
import { dashboards } from '../dashboards/[dash_id]/schema'

export const templates = pgTable('templates', {
  id: uuid('id').primaryKey().defaultRandom(),
  topic: text('topic').notNull(),
  description: text('description').notNull()
})

export const templatesRelations = relations(templates, ({ many }) => ({
  dashboard: many(dashboards)
}))