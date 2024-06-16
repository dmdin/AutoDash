import { dev } from '$app/environment';
import { SvelteKitAuth } from '@auth/sveltekit';
import Google from '@auth/sveltekit/providers/google';
import GitHub from '@auth/sveltekit/providers/github';
import { DrizzleAdapter } from '@auth/drizzle-adapter';
import { db } from '$repo/db';

export const { handle, signIn, signOut } = SvelteKitAuth({
	debug: dev,
	adapter: DrizzleAdapter(db),
	trustHost: true,
	providers: [GitHub, Google],
	callbacks: {
		async session({ session, token }) {
			// console.log('session', session, token)
			return session;
		}
	}
});
