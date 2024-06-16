<script>
	import { signIn } from '@auth/sveltekit/client';

	import DeviconGithub from '~icons/devicon/github';
	import FlatColorIconsGoogle from '~icons/flat-color-icons/google';
</script>

<div class="w-fit h-[300px] border rounded-md border-neutral/40 p-10 mx-auto flex flex-col justify-between">
	<h1 class="text-xl font-bold my-4">Войти с помощью SSO</h1>
	<div class="flex flex-col gap-2">
		<button class="btn" on:click={() => signIn('github')}><DeviconGithub /> GitHub</button>
		<button class="btn" on:click={() => signIn('github')}><FlatColorIconsGoogle /> Google</button>
	</div>
</div>
