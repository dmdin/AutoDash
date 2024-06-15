import { dynamicClient } from '@chord-ts/rpc/client'
import type { Client } from './+server'

export const rpc = dynamicClient<Client>({ endpoint: '/' })
