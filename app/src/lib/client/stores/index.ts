import { writable, derived, type Writable } from 'svelte/store';

export type Themes = 'light' | 'dark'

export const theme: Writable<Themes> = writable();

theme.subscribe(t => {
  if (!t) return
  localStorage.setItem('theme', t)
})

export type Models = 'ChatGPT 3.5' | 'ChatGPT 4o' 
export const model = writable<Models>('ChatGPT 3.5')
