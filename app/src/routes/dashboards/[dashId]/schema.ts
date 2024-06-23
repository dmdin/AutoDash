import { relations, sql } from 'drizzle-orm'
import {
  boolean,
  pgTable,
  pgEnum,
  primaryKey,
  text,
  timestamp,
  uuid,
  unique,
  numeric,
  integer,
  json
} from 'drizzle-orm/pg-core'
import { templates, users } from '$schema'

export const dashboards = pgTable('dashboards', {
  id: uuid('id').primaryKey().defaultRandom(),
  templateId: uuid('templateId').references(() => templates.id).notNull(),
  createdAt: timestamp('createdAt').defaultNow(),
  authorId: text('authorId').references(() => users.id).notNull(),
  generated: boolean('generated').default(false)
})

export const dashboardsRelations = relations(dashboards, ({ one, many }) => ({
  template: one(templates, {fields: [dashboards.templateId], references: [templates.id]}),
  blocks: many(blocks),
  author: one(users, {fields: [dashboards.authorId], references: [users.id]})
}))

export const blocks = pgTable('blocks', {
  id: uuid('id').primaryKey().defaultRandom(),
  dashboardId: uuid('dashboardId').references(() => dashboards.id).notNull(),
  order: integer('order').notNull(),
  name: text('name')
})

export const blocksRelations = relations(blocks, ({ many, one }) => ({
  dashboard: one(dashboards, { fields: [blocks.dashboardId], references: [dashboards.id]}),
  widgets: many(widgets)
}))

export const widgets = pgTable('widgets', {
  id: uuid('id').primaryKey().defaultRandom(),
  blockId: uuid('blockId').references(() => blocks.id).notNull(),
  data: json('data').notNull(),
  order: integer('order'),
  xPos: integer('xPos'),
  yPos: integer('yPos'),
  width: integer('width'),
  height: integer('height')
})

export const widgetsRelations = relations(widgets, ({ many, one}) => ({
  block: one(blocks, { fields: [widgets.blockId], references: [blocks.id]}),
  prompts: many(prompts)
}))

export const prompts = pgTable('prompts', {
  id: uuid('id').primaryKey().defaultRandom(),
  widgetId: uuid('widgetId').references(() => widgets.id).notNull(),
  text: text('text')
})

export const promptsRelations = relations(prompts, ({ one }) => ({
  widget: one(widgets, {fields: [prompts.widgetId], references: [widgets.id]})
}))