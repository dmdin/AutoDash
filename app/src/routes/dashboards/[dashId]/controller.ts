import { page } from '$app/stores'
import { WIDGET_SHIFT_X, WIDGET_SHIFT_Y } from '$root/routes/dashboards/[dashId]/constants'
import { derived, Readable, writable } from 'svelte/store'

export const dashId = derived<Readable<object>[], string>(
  [page],
  ([$page]) => {
    return $page.params.dashId
  }
)
export const dashboard = writable()
export const nodes = writable([])

export const edges = writable([])
export const reservedPlace = writable({ x: WIDGET_SHIFT_X, y: 0})
