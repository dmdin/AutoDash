import { drizzle } from "drizzle-orm/postgres-js"
import { migrate } from "drizzle-orm/postgres-js/migrator"
import postgres from "postgres"

import 'dotenv/config'

console.log('MIGRATION STARTED')
const sql = postgres(process.env.MAIN_DB as string, { max: 1 })
const db = drizzle(sql)
await migrate(db, { migrationsFolder: './drizzle' })
sql.end()
console.log('MIGRATION FINISHED')
