export interface Badge {
	title: string;
	value: number;
	delta: number;
	unit: string;
}

export const BADGES: Badge[] = [
		{
			title: 'Total Shipments 2022',
			value: 2002,
			delta: -6,
			unit: ''
		},
		{
			title: 'Total Shipments 2023',
			value: 10000,
			delta: -3,
			unit: ''
		},
		{
			title: 'Apple Market Share Q4 2022',
			value: 23,
			delta: 1,
			unit: '%'
		},
		{
			title: 'Apple Market Share Q4 2023',
			value: 24,
			delta: 1,
			unit: '%'
		},
		{
			title: 'Samsung Market Share Q4 2022',
			value: 19,
			delta: -2,
			unit: '%'
		},
		// {
		// 	title: 'Samsung Market Share Q4 2023',
		// 	value: 17,
		// 	delta: -2,
		// 	unit: '%'
		// },
		// {
		// 	title: 'Xiaomi Market Share Q4 2022',
		// 	value: 11,
		// 	delta: 2,
		// 	unit: '%'
		// },
		// {
		// 	title: 'Xiaomi Market Share Q4 2023',
		// 	value: 13,
		// 	delta: 2,
		// 	unit: '%'
		// },
		// {
		// 	title: 'TRANSSION Market Share Q4 2022',
		// 	value: 6,
		// 	delta: 3,
		// 	unit: '%'
		// },
		// {
		// 	title: 'TRANSSION Market Share Q4 2023',
		// 	value: 9,
		// 	delta: 3,
		// 	unit: '%'
		// }
]
