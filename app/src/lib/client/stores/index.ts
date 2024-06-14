import { writable, derived, type Writable } from 'svelte/store';

export type Themes = 'light' | 'dark'

export const theme: Writable<Themes> = writable();

theme.subscribe(t => {
  if (!t) return
  localStorage.setItem('theme', t)
})