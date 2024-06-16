import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async (event) => {
	const session = await event.locals.auth();
	if (!session && event.url.pathname !== '/') throw redirect(302, '/')
	return {
		session
	};
};
