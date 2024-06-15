<script lang="ts">
  import {fade} from 'svelte/transition'

  export let data;

  console.log(data.dashboards)

</script>

<div 
  in:fade
  class="self-center grow mt-2 w-full border border-neutral/40 rounded-md p-5 max-w-4xl"
>
	<h1 class="text-2xl font-[600] mb-4">Сохраненные отчеты:</h1>
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