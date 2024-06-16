import { redirect } from '@sveltejs/kit';


export async function load({locals}) {
  const session = await locals.auth();
  if (!session) throw redirect(302, '/')
}