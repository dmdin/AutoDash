/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		screens: {
			xl: { max: '1279px' },
			// => @media (max-width: 1279px) { ... }

			lg: { max: '1023px' },
			// => @media (max-width: 1023px) { ... }

			md: { max: '767px' },
			// => @media (max-width: 767px) { ... }

			sm: { max: '639px' }
			// => @media (max-width: 639px) { ... }
		}
	},

	daisyui: {
		themes: [
			{
				light: {
					primary: '#E3F5FF',
					secondary: '#E5ECF6',
					accent: '#95A4FC',
					'base-100': '#ffffff',
					'base-200': '#f7f9fb',
					'base-300': '#e5ecf6',
					neutral: '#474848',
          success: '#BAEDBD',
				}
			},
			{
				dark: {
					primary: '#E3F5FF',
					secondary: '#E5ECF6',
					accent: '#95A4FC',
					'base-100': '#1c1c1c',
					'base-200': '#282828',
					'base-300': '#e5ecf6',
					neutral: '#e5ecf6',
          success: '#BAEDBD',
				}
			}
		]
	},
	plugins: [
		require('daisyui'),
		require('@tailwindcss/container-queries'),
		require('@tailwindcss/typography')
	]
};
