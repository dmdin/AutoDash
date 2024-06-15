<script lang="ts">
	import { fade } from 'svelte/transition';

	export let data;

	console.log(data.dashboards);
</script>

<div in:fade class="self-center grow mt-2 w-full border border-neutral/40 rounded-md p-5 max-w-4xl">
	<div class="flex justify-between mb-2">
		<h1 class="text-2xl font-[600] mb-4">Сохраненные отчеты:</h1>
		<label class="input input-bordered flex items-center gap-2">
			<input type="text" class="grow" placeholder="Поиск по отчетам" />
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 16 16"
				fill="currentColor"
				class="w-4 h-4 opacity-70"
				><path
					fill-rule="evenodd"
					d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
					clip-rule="evenodd"
				/></svg
			>
		</label>
	</div>
	<div class="overflow-x-auto">
		<table class="table table-zebra">
			<!-- head -->
			<thead>
				<tr>
					<th>№</th>
					<th>Тема</th>
					<th>Описание</th>
					<th>Автор</th>
					<th>Дата</th>
				</tr>
			</thead>
			<tbody>
				<!-- row 1 -->
				<tr>
					<th>1</th>
					<td>Cy Ganderton</td>
					<td>Quality Control Specialist</td>
					<td>Blue</td>
				</tr>
				<!-- row 2 -->
				<tr>
					<th>2</th>
					<td>Hart Hagerty</td>
					<td>Desktop Support Technician</td>
					<td>Purple</td>
				</tr>
				<!-- row 3 -->
				<tr>
					<th>3</th>
					<td>Brice Swyre</td>
					<td>Tax Accountant</td>
					<td>Red</td>
				</tr>
			</tbody>
		</table>
	</div>
</div>
