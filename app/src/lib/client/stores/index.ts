import { writable, derived, type Writable } from 'svelte/store';

export type Themes = 'light' | 'dark';

export const theme: Writable<Themes> = writable();

theme.subscribe((t) => {
	if (!t) return;
	localStorage.setItem('theme', t);
});

// export const avaliableModels = {
// 	'GPT-4o': 'gpt-4o',
// 	'GPT-4 turbo': 'gpt-4-turbo',
// 	'GPT-4': 'gpt-4',
// 	'GPT-3.5 turbo': 'gpt-3.5-turbo'
// };

export const avaliableModels = [
	'gpt-4o',
	'gpt-4-turbo',
	'gpt-4',
	'gpt-3.5-turbo'
];

export const model = writable<string>('gpt-4-turbo');
