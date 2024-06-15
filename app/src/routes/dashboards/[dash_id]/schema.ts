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
import { templates } from '$schema'

export const dashboards = pgTable('dashboards', {
  id: uuid('id').primaryKey().defaultRandom(),
  templateId: uuid('templateId').references(() => templates.id).notNull()
})

export const blocks = pgTable('blocks', {
  id: uuid('id').primaryKey().defaultRandom(),
  dashboardId: uuid('dashboardId').references(() => dashboards.id).notNull(),
  order: integer('order').notNull(),
  name: text('name')
})

export const widgets = pgTable('widgets', {
  id: uuid('id').primaryKey().defaultRandom(),
  blockId: uuid('blockId').references(() => blocks.id).notNull(),
  data: json('data').notNull(),
  xPos: integer('xPos'),
  yPos: integer('yPos'),
  width: integer('width'),
  height: integer('height')
})

export const prompts = pgTable('prompts', {
  id: uuid('id').primaryKey().defaultRandom(),
  widgetId: uuid('widgetId').references(() => widgets.id).notNull(),
  text: text('text')
})