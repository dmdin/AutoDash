import { db, takeUniqueOrThrow } from '$repo/db'
import { blocks, dashboards, templates, widgets } from '$schema'
import { rpc } from '@chord-ts/rpc'

export class Prompt {

  @rpc()
  async createDashboard(topic: string, description: string){
    //   Тут какая то логика обращенния к LLM

    //   Пока мокаю данные
    const blocksData = [
      {
        name: 'Блок 1.',
        widgets: [
          {
            "type":
              "pie"
            ,
            "title":
              "Traffic by Location"
            ,
            "subtitle":
              ""
            ,
            "category": [],
            "series": [
              {
                "name":
                  ""
                ,
                "type":
                  "pie"
                ,
                "unit":
                  "%"
                ,
                "data": [
                  {
                    "name":
                      "United States"
                    ,
                    "value":
                      "38.6"
                  },
                  {
                    "name":
                      "Canada"
                    ,
                    "value":
                      "22.5"
                  },
                  {
                    "name":
                      "Mexico"
                    ,
                    "value":
                      "30.8"
                  },
                  {
                    "name":
                      "other"
                    ,
                    "value":
                      "30.8"
                  }
                ]
              }
            ]
          },
          {
            "type":
              "pie"
            ,
            "title":
              "Traffic by Location"
            ,
            "subtitle":
              ""
            ,
            "category": [],
            "series": [
              {
                "name":
                  ""
                ,
                "type":
                  "pie"
                ,
                "unit":
                  "%"
                ,
                "data": [
                  {
                    "name":
                      "United States"
                    ,
                    "value":
                      "38.6"
                  },
                  {
                    "name":
                      "Canada"
                    ,
                    "value":
                      "22.5"
                  },
                  {
                    "name":
                      "Mexico"
                    ,
                    "value":
                      "30.8"
                  },
                  {
                    "name":
                      "other"
                    ,
                    "value":
                      "30.8"
                  }
                ]
              }
            ]
          }
        ]
      }
    ]

    const template = await db
      .insert(templates)
      .values({ topic, description })
      .returning()
      .then(takeUniqueOrThrow)

    const dashboard = await db
      .insert(dashboards)
      .values({ templateId: template.id})
      .returning()
      .then(takeUniqueOrThrow)

    const insertedBlocks = await db
      .insert(blocks)
      .values(blocksData.map((block, ind) =>
        ({ name: block.name, dashboardId: dashboard.id, order: ind})))
      .returning()

    const widgetsValues = blocksData.map((block, blockInd) =>
      block.widgets.map((widget, widgetInd) => ({
        blockId: insertedBlocks[blockInd].id,
        data: widget,
        order: widgetInd
      }))).flat(1)

    const insertedWidgets = await db
      .insert(widgets)
      .values(widgetsValues)
      .returning()

    return dashboard
  }
}