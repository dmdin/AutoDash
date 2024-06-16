<script>
	let faqs = [
		{
			question: 'Как посмотреть сохраненный отчет?',
			answer:
				'Для того, чтобы посмотреть сохраненные отчет необходимо кликнуть на кнопку "Отчеты" в контекстном меню. Вам отобразятся отчеты, сохраненные другими пользователями.',
			open: false
		},
		{
			question: 'Как создать новый отчет?',
			answer:
				'Необходимо кликнуть на кнопку "+" в контекстном меню. Затем можно указать тему отчета и его структуру. Обратите внимания, что оба поля можно сгенерировать с помощью искусственного интеллекта',
			open: false
		},
    {
			question: 'Как редактировать существующий отчет?',
			answer:
				'Вам предоставлен богатый функционал редактирования отчета. Вы можете уточнять запрос. Для этого кликните на любую точку отчета правой кнопкой мыши и введите запрос. Также вы можете свободно перемещать компоненты.',
			open: false
		},
    {
			question: 'Как экспортировать отчет?',
			answer:
				'Перейдите в любой отчет. Справа расположена панель экспорта. Вы можете выбрать несколько форматов для эскопрта: pdf, word, excel, png.',
			open: false
		}
	];

	const toggleFAQ = (index) => {
		faqs[index].open = !faqs[index].open;
	};
</script>

<div class="w-full flex items-center justify-center">
	<div class="p-4 w-[900px]">
		<h1 class="text-xl font-bold text-center mb-4">FAQ</h1>
		<ul>
			{#each faqs as faq, index}
				<li class="mb-2">
					<button
						class="w-full text-left text-lg font-semibold bg-blue-200 p-2 rounded-md"
						on:click={() => toggleFAQ(index)}
					>
						{faq.question}
					</button>
					{#if faq.open}
						<div class="p-2 text-gray-700 bg-blue-100 rounded-md mt-1">
							{faq.answer}
						</div>
					{/if}
				</li>
			{/each}
		</ul>
	</div>
</div>
