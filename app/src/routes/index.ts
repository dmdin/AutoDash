import { dynamicClient } from '@chord-ts/rpc/client'
import { writable } from 'svelte/store'

import type { Client } from './+server'

export const showLayout = writable(true)
export const rpc = dynamicClient<Client>({ endpoint: '/' })
