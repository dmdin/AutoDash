<script lang="ts">
	import { fade } from 'svelte/transition';
	import {rpc} from '$root/routes'

	import Trash from '~icons/ph/trash';
	import Edit from '~icons/lucide/edit';
	import Eye from '~icons/mdi/eye-outline';

	export let data;
	let {
		dashboards,
		session: { user }
	} = data;

	let search = '';
	let deleteId: string | undefined;

	$: filteredDashboards = dashboards.filter(d => (d.template.topic + d.template.description).toLowerCase().includes(search.toLowerCase()))
	async function deleteDash() {
		if (!deleteId) return
		const res = await rpc.Dashboard.delete(deleteId).catch(e => console.error(e))
		console.log(res)
		deleteId = undefined
	}


</script>

<div in:fade class="self-center grow mt-2 w-full border border-neutral/40 rounded-md p-5 max-w-4xl">
	<div class="flex justify-between mb-2">
		<h1 class="text-2xl font-[600] mb-4">Сохраненные отчеты:</h1>
		<label class="input input-bordered flex items-center gap-2">
			<input type="text" class="grow" placeholder="Поиск по отчетам" bind:value={search}/>
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
					<th>Время создания</th>
					<th>Действия</th>
				</tr>
			</thead>
			<colgroup>
				<col style="width: 10px;" />
				<col style="width: 20%;" />
				<col style="width: auto;" />
				<col style="width: 50px;" />
				<col style="width: 200px;" />
				<col style="width: 100px;" />
			</colgroup>
			<tbody>
				{#each filteredDashboards as dash, i}
					<tr>
						<th>{i + 1}</th>
						<td>{dash.template.topic}</td>
						<td><p class="truncate max-w-[300px] truncate">{dash.template.description}</p> </td>
						<td>
							<div
								class="tooltip tooltip-top"
								data-tip={`${dash.author.name} - ${dash.author.email}`}
							>
								<div class="avatar">
									<div class="w-8 rounded-xl">
										<a href="/user">
											<img
												alt="User avatar"
												src={dash.author.image ?? 'https://source.boringavatars.com/marble/120'}
												class="avatar"
											/>
										</a>
									</div>
								</div>
							</div>
						</td>
						<td>
							<span
								>{dash.createdAt?.toLocaleString()}</span
							>
						</td>
						<td>
							<div class="flex gap-2">
								{#if user.id === dash.author.id}
									<button
										class="btn btn-sm btn-square transition-colors hover:text-error"
										onclick="deleteDashboard.showModal()" on:click={() => deleteId = dash.id}><Trash /></button
									>
								{/if}
								<a
									class="btn btn-sm btn-square transition-colors hover:text-info"
									href="/dashboards/{dash.id}"><Eye /></a
								>
							</div>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

<dialog id="deleteDashboard" class="modal">
	<div class="modal-box">
		<h3 class="font-bold text-lg">Подтвердите действие</h3>
		<p class="py-4">Вы уверены, что хотите удалить отчет?</p>
		<div class="modal-action">
			<form method="dialog" class=" flex gap-4">
				<!-- if there is a button in form, it will close the modal -->
				<button class="btn " on:click={() => deleteId = undefined}>Отмена</button>
				<button class="btn btn-error btn-outline" on:click={deleteDash}>Удалить</button>
			</form>
		</div>
	</div>
</dialog>
