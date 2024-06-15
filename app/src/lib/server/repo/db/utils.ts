export type { InferSelectModel as TableType } from 'drizzle-orm'

export const takeUniqueOrThrow = <T>(values: T[]): T => {
  if (values.length !== 1)
    throw new Error('Записи не существует, либо она не уникальная');
  return values[0]!
}