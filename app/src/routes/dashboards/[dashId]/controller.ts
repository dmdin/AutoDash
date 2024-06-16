import ExcelJS from 'exceljs';
import { page } from '$app/stores';
import { WIDGET_SHIFT_X, WIDGET_SHIFT_Y } from '$root/routes/dashboards/[dashId]/constants';
import { derived, get, Readable, writable } from 'svelte/store';
import { getContext } from 'svelte';
import sharp from 'sharp';

export const dashId = derived<Readable<object>[], string>([page], ([$page]) => {
	return $page.params.dashId;
});
export const dashboard = writable();
export const nodes = writable([]);

export const edges = writable([]);
export const reservedPlace = writable<{ x: number; y: number; endX: number; endY: number }>();
export const readonly = writable(false)