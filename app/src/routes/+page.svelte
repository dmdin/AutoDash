<script>
  import { page } from '$app/stores';
import {fade} from 'svelte/transition'
  import StartUp from '~icons/hugeicons/start-up-02';
</script>

<section in:fade class="grow w-full flex flex-col items-center justify-center mb-40">
  <h1 class="font-black text-4xl text-center">Добро пожаловать<br>
    в <i class="bg-gradient-to-r from-accent to-secondary inline-block text-transparent bg-clip-text text-4xl font-black">AutoDash</i>
  </h1>
  {#if $page.data.session}
    <a href="/prompt" class="btn btn-xl h-16 text-xl btn-accent my-6"><StartUp/>Начать</a>
  {:else}
    <button 
      onclick="signinModal.showModal()" 
      class="btn btn-xl h-16 text-xl btn-accent my-6">
      <StartUp/>Начать
    </button>
  {/if}
</section>