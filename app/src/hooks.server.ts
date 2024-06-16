import { handle as authenticationHandle } from "./routes/auth"
import { redirect, type Handle, error } from '@sveltejs/kit'
import { sequence } from '@sveltejs/kit/hooks'

async function authorizationHandle({ event, resolve }) {

  const session = await event.locals.auth();
  event.locals.user = session?.user
  return resolve(event);
}


// First handle authentication, then authorization
// Each function acts as a middleware, receiving the request handle
// And returning a handle which gets passed to the next function
export const handle: Handle = sequence(authenticationHandle, authorizationHandle)
