import { NodeGlobalsPolyfillPlugin } from '@esbuild-plugins/node-globals-polyfill'
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import swc from 'unplugin-swc';
import Icons from 'unplugin-icons/vite';

export default defineConfig({
	plugins: [
		sveltekit(),
		swc.vite(),
		Icons({
			compiler: 'svelte'
		}),
		NodeGlobalsPolyfillPlugin({
			buffer: true
		})
	],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
