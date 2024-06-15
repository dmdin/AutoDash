import * as dotenv from 'dotenv';
import type { Config } from 'drizzle-kit';

dotenv.config();

export default {
	driver: 'pg',
	out: './drizzle',
	schema: './src/schema.ts',
	schemaFilter: 'prisma',
	dbCredentials: {
		url: process.env.MAIN_DB,
	},
	// Print all statements
	verbose: true,
	// Always ask for confirmation
	strict: true
} as Config;
