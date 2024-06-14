import { drizzle } from 'drizzle-orm/postgres-js';
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import postgres from 'postgres';
import {DB} from '$env/static/private'
// for migrations
// const migrationClient = postgres(DB, { max: 1 });
// migrate(drizzle(migrationClient), {})

// for query purposes
const queryClient = postgres(DB);
export const db = drizzle(queryClient);

