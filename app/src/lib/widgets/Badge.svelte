<script lang="ts">
	import { formatNumber } from '$lib/utils/utils';
	import Icon from '@iconify/svelte';

	export let title;
	export let value;
	export let unit;
	export let delta;
</script>

<button
	class="max-w-[200px] max-h-[120px] h-full flex-shrink-0 p-[24px] rounded-[16px] bg-base-200 shadow-xl cursor-grab {$$props.class}" title={`${title}\n${value}`}
>
	<h3 class="text-primary-content font-semibold text-[14px] mb-[8px] truncate">{title}</h3>

	<div class="flex gap-10 justify-between items-center">
		<p class="text-primary-content font-semibold text-[24px]">{formatNumber(value)}&nbsp;{unit ? unit : ''}</p>
		<p class="text-primary-content text-[12px] gap-[4px] flex justify-center items-center">
			{#if delta}
				{#if delta > 0}
					<Icon icon="ep:plus" width="8px" height="8px" style="color: black" />
				{/if}
				{delta}
				{#if delta > 0}
					<Icon icon="ant-design:rise-outlined" width="20px" height="20px" style="color: black" />
				{:else if delta < 0}
					<Icon icon="ant-design:fall-outlined" width="20px" height="20px" style="color: black" />
				{/if}
			{/if}
		</p>
	</div>
</button>
