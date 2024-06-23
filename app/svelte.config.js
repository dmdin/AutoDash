import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

import { preprocessMeltUI, sequence } from '@melt-ui/pp';

/** @type {import('@sveltejs/kit').Config}*/
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: sequence([vitePreprocess(), preprocessMeltUI()]),
	kit: {
		// adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
		// If your environment is not supported or you settled on a specific environment, switch out the adapter.
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter(),
		csrf: {
			checkOrigin: false
		},

		alias: {
			$root: 'src',
			$schema: 'src/schema',
			$stores: 'src/lib/client/stores',
			$repo: 'src/lib/server/repo',
			$client: 'src/lib/client',
			$server: 'src/lib/server',

			$auth: 'src/routes/auth',
			$user: 'src/routes/user',
			$module: 'src/routes/test',
		}
	},
};
export default config;
