import { drizzle } from 'drizzle-orm/postgres-js'
import postgres from 'postgres'

import * as env from '$env/static/private'
// import { env } from '$env/dynamic/private'
import * as schema from '$schema'

export { takeUniqueOrThrow } from './utils'
export const sql = postgres(env.MAIN_DB)
// const client = postgres(`postgres://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/${PGDATABASE}`)

export const db = drizzle(sql, { schema })