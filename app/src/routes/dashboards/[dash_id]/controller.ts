import { writable } from 'svelte/store'

export const nodes = writable([
  {
    id: '1',
    type: 'plot-node',
    data: { label: 'Input Node' },
    position: { x: 0, y: 0 }
  },
  {
    id: '2a',
    type: 'plot-node',
    position: { x: 0, y: 150 },
  }
])

export const edges = writable([])
