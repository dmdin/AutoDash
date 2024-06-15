import { pgTable, text, uuid } from 'drizzle-orm/pg-core'

export const templates = pgTable('templates', {
  id: uuid('id').primaryKey().defaultRandom(),
  topic: text('topic').notNull(),
  description: text('description').notNull()
})