/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: '#E3F5FF',
				secondary: '#E5ECF6',
				tertiary: '#95A4FC',
				base: {
					DEFAULT: '#A4A4A4',
          200: '#F7F9FB',
					content: '#1C1C1C'
				},
				success: {
					DEFAULT: '#BAEDBD'
				}
			}
		},
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
	plugins: [
		require('daisyui'),
		require('@tailwindcss/container-queries'),
		require('@tailwindcss/typography')
	]
};
