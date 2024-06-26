import { dev } from '$app/environment';
import { SvelteKitAuth } from '@auth/sveltekit';
import Google from '@auth/sveltekit/providers/google';
import GitHub from '@auth/sveltekit/providers/github';
import Nodemailer from '@auth/sveltekit/providers/nodemailer';
import { DrizzleAdapter } from '@auth/drizzle-adapter';
import { db } from '$repo/db';
import {
	EMAIL_SERVER_HOST,
	EMAIL_SERVER_PORT,
	EMAIL_SERVER_USER,
	EMAIL_SERVER_PASSWORD,
	EMAIL_FROM
} from '$env/static/private';

export const { handle, signIn, signOut } = SvelteKitAuth({
	debug: true,
	adapter: DrizzleAdapter(db),
	trustHost: true,
	providers: [
		GitHub,
		// Google,
		Nodemailer({
			server: {
				host: EMAIL_SERVER_HOST,
				port: EMAIL_SERVER_PORT,
				auth: {
					user: EMAIL_SERVER_USER,
					pass: EMAIL_SERVER_PASSWORD
				}
			},
			from: EMAIL_FROM
		})
	],
	callbacks: {
		async session({ session, token }) {
			// console.log('session', session, token)
			return session;
		}
	}
});
