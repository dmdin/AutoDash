import { dev } from '$app/environment';
import { SvelteKitAuth } from "@auth/sveltekit"
import Google from "@auth/sveltekit/providers/google"
import GitHub from "@auth/sveltekit/providers/github"

export const { handle, signIn, signOut } = SvelteKitAuth({
  debug: dev,
  providers: [
    GitHub
  ],
})
