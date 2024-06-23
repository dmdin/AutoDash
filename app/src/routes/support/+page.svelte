<script>
	let faqs = [
		{
			question: 'Как посмотреть сохраненный отчет?',
			answer: [
				{
					type: 'text',
					text: 'Для того, чтобы посмотреть сохраненные отчет необходимо кликнуть на кнопку "Отчеты" в контекстном меню. Вам отобразятся отчеты, сохраненные другими пользователями. Нажмите на кнопку просмотра отчета'
				},
				{
					type: 'image',
					src: 'https://i.ibb.co/Zm94DkT/Screenshot-2024-06-24-at-00-41-32.png',
					alt: 'Кнопка для просмотра отчета - иконка "глаза"'
				}
			],
			open: false
		},
		{
			question: 'Как создать новый отчет?',
			answer: [
				{
					type: 'text',
					text: 'Сначала необходимо кликнуть на кнопку "+" в контекстном меню. Затем можно указать тему отчета и его структуру. Обратите внимания, что оба поля можно сгенерировать с помощью искусственного интеллекта'
				},
				{
					type: 'image',
          height: 100,
					src: 'https://i.ibb.co/qYBQ1cj/Screenshot-2024-06-24-at-00-53-21.png',
					alt: 'Кнопка "+" располагается в панели справа от лого'
				},
				{
					type: 'text',
					text: 'Следующий шаг - определение параметров отчета. Вы можете выбрать тему отчета, ввести шаблон и указать источники поиска'
				},
				{
					type: 'image',
          height: 800,
					src: 'https://i.ibb.co/L60q1Sx/Screenshot-2024-06-24-at-00-56-46.png',
					alt: 'Если сомневаетесь с темой или структурой отчета - не беда. Мы можем сгенерировать их при помощи искусственного интеллекта. Обратите внимание на кнопки, расположенные слева от поля ввода'
				},
			],
			open: false
		},
		{
			question: 'Как редактировать существующий отчет?',
			answer: [
				{
					type: 'text',
					text: `Есть несколько функций для редактирования отчета:`
				},
				{
					type: 'list',
					items: [
						'Добавление или редактирование текстовых блоков',
						'Изменение типа графика',
						'Перемещение элементов'
					]
				},
				{
					type: 'image',
          height: 100,
					src: 'https://i.ibb.co/3sq9hYr/Screenshot-2024-06-24-at-01-13-05.png',
					alt: 'Для добавления текстового блока достаточно кликнуть на кнопку в панели инструментов слева'
				},
        {
					type: 'text',
					text: 'Для редактирования имеющегося текста кликните два раза на него'
				},
        {
					type: 'image',
          height: 100,
					src: 'https://i.ibb.co/3sq9hYr/Screenshot-2024-06-24-at-01-13-05.png',
					alt: 'Вы можете изменить тип графика, выбрав отображение на верхней панели редактирования графика'
				},
        {
					type: 'text',
					text: 'Компоненты можно перемещать по холсту. Просто кликните на компонент, удерживайте левую кнопку мыши и перемещайте'
				},
			],
			open: false
		},
		{
			question: 'Как экспортировать отчет?',
			answer: [
        {
          type: 'text',
          text: 'Экспорт отчетов доступен в нескольких форматах',
        },
        {
          type: 'list',
          items: [
            'pdf',
            'docx',
            'xlsx',
            'png'
          ],
        },
        {
					type: 'image',
          width: 200,
					src: 'https://i.ibb.co/r6zRjY2/Screenshot-2024-06-24-at-01-56-36.png',
					alt: 'Кнопка экспорта отчета располагается на панели инструментов справа'
				},
        {
          type: 'text',
          text: 'Вы можете экспортировать как весь отчет, так и таблицу отдельно',
        },
        {
					type: 'image',
          height: 100,
					src: 'https://i.ibb.co/z4GTJbC/Screenshot-2024-06-24-at-01-32-39.png',
					alt: 'Для экспорта таблицы нажмите на кнопку "Экспорт" и выберите нужный формат'
				},
      ],
			open: false
		}
	];

	const toggleFAQ = (index) => {
		faqs[index].open = !faqs[index].open;
	};
</script>

<div class="w-full flex items-center justify-center">
	<div class="p-6 w-[900px] bg-base-300 shadow-lg rounded-2xl">
		<h1 class="text-2xl font-bold text-center text-base-content mb-6">FAQ</h1>
		<ul>
			{#each faqs as faq, index}
				<li class="mb-4 last:mb-0">
					<button
						class="w-full text-left text-lg font-medium bg-base-200 p-4 rounded-lg hover:bg-base-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-400 transition-all"
						on:click={() => toggleFAQ(index)}
					>
						<div class="flex justify-between items-center text-base-content">
							<span>{faq.question}</span>
							<svg
								class="w-6 h-6 transform"
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M19 9l-7 7-7-7"
								/>
							</svg>
						</div>
					</button>
					{#if faq.open}
						<div class="p-4 text-base-content bg-base-200 rounded-lg mt-2">
							{#each faq.answer as answer}
								{#if answer.type === 'text'}
									<span>
										{answer.text}
									</span>
								{:else if answer.type === 'list'}
									<ul class="pl-5 py-3">
										{#each answer.items as l}
											<li class="text-base-content list-disc">{l}</li>
										{/each}
									</ul>
								{:else if answer.type === 'image'}
									<div class="w-fit flex items-center justify-center py-6">
										<div class="rounded-lg bg-base-100 overflow-hidden shadow-lg">
											<img src={answer.src} alt={answer.alt} style:width="{answer.width}px" style:height="{answer.height}px" />
											<div class="p-4 bg-base-100">
												<p class="text-base-content">{answer.alt}</p>
											</div>
										</div>
									</div>
								{/if}
							{/each}
						</div>
					{/if}
				</li>
			{/each}
		</ul>
	</div>
</div>
