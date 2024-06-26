import { db, takeUniqueOrThrow } from '$repo/db';
import { blocks, dashboards, templates, savedTemplates, widgets, sources } from '$schema';
import { depends, rpc } from '@chord-ts/rpc';
import axios from 'axios';
export class Prompt {
	@depends()
	ctx!: { user: { id: string } };

	@rpc()
	async saveTemplate({ title, body }: { title: string; body: string }) {
		const authorId = this.ctx.user.id;
		const template = await db
			.insert(savedTemplates)
			.values({ title, authorId, body })
			.returning()
			.then(takeUniqueOrThrow);
		return template;
	}

	@rpc()
	async addSource({ title, link }: { title: string; link: string }) {
		const source = await db
			.insert(sources)
			.values({title, link})
			.returning()
			.then(takeUniqueOrThrow);
		return source
	}

	@rpc()
	async createDashboard(topic: string, description: string) {
		// const blocksData = [
		// 	{
		// 		name: 'Блок 1.',
		// 		widgets: [
		// 			{
		// 				type: 'pie',
		// 				title: 'Traffic by Location',
		// 				subtitle: '',
		// 				category: [],
		// 				series: [
		// 					{
		// 						name: '',
		// 						type: 'pie',
		// 						unit: '%',
		// 						data: [
		// 							{
		// 								name: 'United States',
		// 								value: '38.6'
		// 							},
		// 							{
		// 								name: 'Canada',
		// 								value: '22.5'
		// 							},
		// 							{
		// 								name: 'Mexico',
		// 								value: '30.8'
		// 							},
		// 							{
		// 								name: 'other',
		// 								value: '30.8'
		// 							}
		// 						]
		// 					}
		// 				]
		// 			},
		// 			{
		// 				type: 'pie',
		// 				title: 'Traffic by Location',
		// 				subtitle: '',
		// 				category: [],
		// 				series: [
		// 					{
		// 						name: '',
		// 						type: 'pie',
		// 						unit: '%',
		// 						data: [
		// 							{
		// 								name: 'United States',
		// 								value: '38.6'
		// 							},
		// 							{
		// 								name: 'Canada',
		// 								value: '22.5'
		// 							},
		// 							{
		// 								name: 'Mexico',
		// 								value: '30.8'
		// 							},
		// 							{
		// 								name: 'other',
		// 								value: '30.8'
		// 							}
		// 						]
		// 					}
		// 				]
		// 			},
		// 			{
		// 				type: 'text',
		// 				text: 'Sed gravida fermentum risus vel commodo. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam consectetur accumsan sollicitudin. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sit amet pharetra justo, sed feugiat nulla. Donec dapibus id mi hendrerit congue. Ut mattis et lacus aliquam vehicula. Fusce ullamcorper tempus nunc in tincidunt. Duis in tempus ante, eget laoreet diam. In hac habitasse platea dictumst. Vestibulum magna dui, fringilla eget nunc venenatis, venenatis tristique arcu. Nam facilisis auctor risus malesuada eleifend. Vestibulum pharetra, nunc eget consectetur venenatis, nulla felis ultrices arcu, sit amet varius risus mauris id lorem. Mauris ultricies gravida ex in efficitur. Donec consectetur hendrerit leo, in rhoncus nulla fringilla in. Etiam ultrices metus a lectus sollicitudin accumsan sed ac diam.'
		// 			},
		// 			{
		// 				type: 'pie',
		// 				title: 'Traffic by Location',
		// 				subtitle: '',
		// 				category: [],
		// 				series: [
		// 					{
		// 						name: '',
		// 						type: 'pie',
		// 						unit: '%',
		// 						data: [
		// 							{
		// 								name: 'United States',
		// 								value: '38.6'
		// 							},
		// 							{
		// 								name: 'Canada',
		// 								value: '22.5'
		// 							},
		// 							{
		// 								name: 'Mexico',
		// 								value: '30.8'
		// 							},
		// 							{
		// 								name: 'other',
		// 								value: '30.8'
		// 							}
		// 						]
		// 					}
		// 				]
		// 			},
		// 			{
		// 				type: 'pie',
		// 				title: 'Traffic by Location',
		// 				subtitle: '',
		// 				category: [],
		// 				series: [
		// 					{
		// 						name: '',
		// 						type: 'pie',
		// 						unit: '%',
		// 						data: [
		// 							{
		// 								name: 'United States',
		// 								value: '38.6'
		// 							},
		// 							{
		// 								name: 'Canada',
		// 								value: '22.5'
		// 							},
		// 							{
		// 								name: 'Mexico',
		// 								value: '30.8'
		// 							},
		// 							{
		// 								name: 'other',
		// 								value: '30.8'
		// 							}
		// 						]
		// 					}
		// 				]
		// 			}
		// 		]
		// 	}
		// ]

		// const generatedWidgets = await generateWidgets(topic, description, urls);
		// for (const widget of generatedWidgets) {
		// 	if (widget.type === 'text') {
		// 		let text = '';
		// 		console.log(widget);
		// 		for (const s of widget?.series) {
		// 			for (const val of s.data) {
		// 				text += val.value + '\n';
		// 			}
		// 		}
		// 		widget.text = text;
		// 	}
		// }
		// const blocksData = [
		// 	{
		// 		name: '',
		// 		widgets: generatedWidgets
		// 	}
		// ];

		// const genWidgets = await generateWidgets(topic, description)

		const template = await db
			.insert(templates)
			.values({ topic, description })
			.returning()
			.then(takeUniqueOrThrow);

		const authorId = this.ctx.user.id;
		const dashboard = await db
			.insert(dashboards)
			.values({ templateId: template.id, authorId })
			.returning()
			.then(takeUniqueOrThrow);

		// const insertedBlocks = await db
		// 	.insert(blocks)
		// 	.values(
		// 		blocksData.map((block, ind) => ({
		// 			name: block.name,
		// 			dashboardId: dashboard.id,
		// 			order: ind
		// 		}))
		// 	)
		// 	.returning();
		//
		// const widgetsValues = blocksData
		// 	.map((block, blockInd) =>
		// 		block.widgets.map((widget, widgetInd) => ({
		// 			blockId: insertedBlocks[blockInd].id,
		// 			data: widget,
		// 			order: widgetInd
		// 		}))
		// 	)
		// 	.flat(1);
		//
		// const insertedWidgets = await db.insert(widgets).values(widgetsValues).returning();

		return dashboard
	}
}

async function generateWidgets(topic: string, description: string, urls=[]) {
	return await axios
		.post('http://87.242.103.101:8001/api/llm/create_report?model_name=gpt-4o', {
			urls: {
				urls
			},
			report_item: {
				report_theme: topic,
				report_text: description
			}
		})
		.then((res) => res.data.widgets);
}
