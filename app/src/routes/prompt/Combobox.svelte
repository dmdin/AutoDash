<script lang="ts" generics="T">
	import { createCombobox, createSync, melt, type CreateComboboxProps } from '@melt-ui/svelte';

	import Check from '~icons/material-symbols/check';
	import ChevronDown from '~icons/mdi/chevron-down';
	import ChevronUp from '~icons/mdi/chevron-up';

	import { fly } from 'svelte/transition';

	export let value: T | T[];
	export let options: T[] = [];
	export let placeholder = 'Множественный выбор';
	export let multiple = true;
	export let extractor = (option: T) => option?.toString();

	const {
		elements: { menu, input, option, label },
		states: { open, inputValue, touchedInput, selected },
		helpers: { isSelected }
	} = createCombobox({
		forceVisible: true,
		multiple
	});

	// const sync = createSync({ selected });

  if (value && multiple) {
    $selected = value.map(v => {return {value: v, label: extractor(v)}})
  } else if (!multiple) {
    $selected = {value, label: extractor(value)}
  }

  $: value = $selected.map(v => v.value)


  
	// $: sync.selected(value !== null ? { value, label: extractor(value) } : undefined, (v) => {
	// 	console.log('sync', value);
	// 	return v === undefined ? (value = null) : (value = v.value);
	// });

	$: console.log('selected', $selected);
	$: filtered = $touchedInput
		? options.filter((option) => {
				const normalizedInput = $inputValue.toLowerCase();
				return extractor(option).toLowerCase().includes(normalizedInput);
			})
		: options;
</script>

<!-- svelte-ignore a11y-label-has-associated-control - $label contains the 'for' attribute -->
<!-- <label use:melt={$label}>
    <span class="text-sm font-medium text-magnum-900"
      >Choose your favorite manga:</span
    >
  </label> -->

<div class="relative w-full">
	<input
		use:melt={$input}
		class="input input-bordered text-sm
          px-3 pr-12 text-black"
		{placeholder}
	/>
	<div class="absolute right-2 top-1/2 z-10 -translate-y-1/2">
		{#if $open}
			<ChevronUp class="size-4" />
		{:else}
			<ChevronDown class="size-4" />
		{/if}
	</div>
</div>
{#if $open}
	<ul
		class=" z-10 flex max-h-[300px] flex-col overflow-hidden rounded-lg"
		use:melt={$menu}
		transition:fly={{ duration: 150, y: -5 }}
	>
		<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
		<div
			class="flex max-h-full flex-col gap-0 overflow-y-auto bg-base-100 px-2 py-2 border-2 rounded-md"
			tabindex="0"
		>
			{#each filtered as _option, index (index)}
				<li
					use:melt={$option({
						value: _option,
						label: extractor(_option)
					})}
					class="relative cursor-pointer scroll-my-2 rounded-md py-2 pl-4 pr-4
        data-[highlighted]:bg-primary/40 data-[highlighted]:text-primary-content
          data-[disabled]:opacity-50"
				>
					{#if $isSelected(_option)}
						<div class="check absolute left-2 top-1/2 -translate-y-1/2 z-10 text-primary-content">
							<Check width="20" />
						</div>
					{/if}
					<div class="pl-4">
						<span class="font-medium">{extractor(_option)}</span>
					</div>
				</li>
			{:else}
				<li
					class="relative cursor-pointer rounded-md py-1 pl-8 pr-4
        data-[highlighted]:bg-magnum-100 data-[highlighted]:text-magnum-700"
				>
					Не найдено
				</li>
			{/each}
		</div>
	</ul>
{/if}
