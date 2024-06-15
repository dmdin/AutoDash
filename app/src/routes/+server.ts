import { Prompt } from '$root/routes/prompt/rpc'
import { Composer } from '@chord-ts/rpc'
import { sveltekitMiddleware } from '@chord-ts/rpc/middlewares'
import { json, RequestEvent } from '@sveltejs/kit'

const composer = Composer.init({
  Prompt: new Prompt()
})
export type Client = typeof composer.clientType
composer.use(sveltekitMiddleware())

export async function POST(event: RequestEvent) {
  return json(await composer.exec(event as unknown as Record<string, unknown>))
}
