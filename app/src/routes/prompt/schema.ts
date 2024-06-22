import { relations } from 'drizzle-orm'
import { pgTable, text, uuid } from 'drizzle-orm/pg-core'
import { dashboards } from '../dashboards/[dashId]/schema'
import {users} from '$root/schema'

export const templates = pgTable('templates', {
  id: uuid('id').primaryKey().defaultRandom(),
  topic: text('topic').notNull(),
  description: text('description').notNull()
})

export const templatesRelations = relations(templates, ({ many }) => ({
  dashboard: many(dashboards)
}))


export const savedTemplates = pgTable('savedTemplates', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: text('title').notNull(),
  body: text('body').notNull(),
  authorId: text('authorId').references(() => users.id).notNull()
})

export const sources = pgTable('sources', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: text('title').notNull(),
  link: text('link').notNull(),
})