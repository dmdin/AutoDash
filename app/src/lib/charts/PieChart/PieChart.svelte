<script lang="ts">
	import { Chart } from 'svelte-echarts';

	import { init, use } from 'echarts/core';
	import { PieChart } from 'echarts/charts';
	import {
		GridComponent,
		LegendComponent,
		TitleComponent,
		TooltipComponent
	} from 'echarts/components';
	import { CanvasRenderer } from 'echarts/renderers';
	import { PIE_SERIES, PIE_VIEW_CONFIG, SERIES_COLORS } from './constants';
	import type { Series } from '../types';
	import { onMount } from 'svelte';
	import { configureOptions, storable } from '../controller';
	import { CHART_HEIGHT, CHART_WIDTH } from '../constants';
	import type { EChartsType } from 'echarts';
	import { derived, type Writable } from 'svelte/store';
	import { browser } from '$app/environment';

	use([
		PieChart,
		GridComponent,
		TooltipComponent,
		LegendComponent,
		GridComponent,
		CanvasRenderer,
		TitleComponent
	]);

	export let title: string = '';
	export let subtitle: string = '';
	export let category: string[] | null = null;
	export let series: Series[];
	export let svgUrl: string | undefined;

	let self: EChartsType | undefined;
	const initOptions = { renderer: 'svg' };
	let options = null;

	enum Theme {
		Light = 'light',
		Dark = 'dark'
	}

	export const theme: Writable<Theme> = (() => {
		const { set, update, subscribe } = storable(Theme.Light, 'theme');

		function change() {
			update((v) => (v === Theme.Light ? Theme.Dark : Theme.Light));
		}

		return {
			set,
			update,
			subscribe,
			change
		};
	})();

	const themeVariables = derived(theme, ($theme, set) => {
		if (!browser) return;
		const element = document.querySelector('#theme-root');

		if (!element) return;

		setTimeout(() => {
			const style = getComputedStyle(element);

			const p = style.getPropertyValue('--p');
			const pf = style.getPropertyValue('--pf');
			const af = style.getPropertyValue('--af');
			const nf = style.getPropertyValue('--nf');

			const bc = style.getPropertyValue('--bc');
			const pc = style.getPropertyValue('--pc');
			const sc = style.getPropertyValue('--sc');
			const ac = style.getPropertyValue('--ac');
			const nc = style.getPropertyValue('--nc');

			const inc = style.getPropertyValue('--inc');
			const suc = style.getPropertyValue('--suc');
			const wac = style.getPropertyValue('--wac');
			const erc = style.getPropertyValue('--erc');

			const s = style.getPropertyValue('--s');
			const a = style.getPropertyValue('--a');
			const n = style.getPropertyValue('--n');
			const b1 = style.getPropertyValue('--b1');
			const b2 = style.getPropertyValue('--b2');
			const b3 = style.getPropertyValue('--b3');
			const in_ = style.getPropertyValue('--in');
			const su = style.getPropertyValue('--su');
			const wa = style.getPropertyValue('--wa');
			const er = style.getPropertyValue('--er');

			set({
				p,
				pf,
				af,
				nf,
				bc,
				pc,
				sc,
				ac,
				nc,
				inc,
				suc,
				wac,
				erc,
				s,
				a,
				n,
				b1,
				b2,
				b3,
				in_,
				su,
				wa,
				er
			});
		}, 1);
	});

	function getSvgUrl() {
		svgUrl = self?.getSvgDataURL();
	}

	onMount(() => {
		options = configureOptions(PIE_VIEW_CONFIG, PIE_SERIES, title, series?.slice(0, 1), null);

		if (!options?.series?.length) return;
		if (!options.series[0]?.data?.[0]?.name) {
			options.series[0].data = options.series[0].data.map((c, i) => {
				return {
					name: category[i],
					value: c
				};
			});
		}

		const element = document.querySelector('#theme-root');
		if (!element) return;
		console.log(getComputedStyle(element));
		const headerColor = getComputedStyle(element)?.getPropertyValue('--suc');
		options.title.textStyle.color = `lab(${headerColor})`;
		console.log(options);
	});

	themeVariables.subscribe((t) => {
		console.log(t);
	});
</script>

<div
	class="bg-base-200 rounded-2xl p-6"
	style:width="{CHART_WIDTH}px"
	style:height="{CHART_HEIGHT}px"
>
	<div class="w-full h-full">
		{#key options}
			{#if options}
				<Chart x={0} {init} {options} {initOptions} bind:chart={self} on:rendered={getSvgUrl} />
			{/if}
		{/key}
	</div>
</div>
