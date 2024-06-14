<script lang="ts">
  import { client } from '@chord-ts/rpc/client';
  import { onMount } from 'svelte';

  // Import our Contract
  import type { Client } from './+server';

  // Init dynamic client with type checking
  // Use Contract as Generic to get type safety and hints from IDE
  // dynamicClient means that RPC will be created during code execution
  // and executed when the function call statement is found
  const rpc = client<Client>({ endpoint: '/test' });

  let res;
  // Called after Page mount. The same as useEffect(..., [])
  onMount(async () => {
    // Call method defined on backend with type-hinting
    res = await rpc.Say.hello('world');
    console.log(res);
  });
</script>

<h1>Chord call Test</h1>
<p>Result: {res}</p>