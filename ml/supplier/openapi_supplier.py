from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from shared.settings import app_settings


@dataclass
class OpenAISupplier:
    def __post_init__(self):
        self.embeddings: OpenAIEmbeddings = OpenAIEmbeddings(
            base_url=app_settings.openai_api_url,
            api_key=app_settings.openai_api_key,
            model='text-embedding-3-large',
        )

    def get_model(self, model_name: str = 'gpt-4o'):
        chat = ChatOpenAI(
            base_url=app_settings.openai_api_url,
            api_key=app_settings.openai_api_key,
            temperature=0.575,
            model=model_name,
        )
        return chat

    @property
    def get_few_shot(self):
        return {
            'line_chart': """
{
  "title": "Total Users",
  "subtitle": "",
  "type": "line",
  "categories": [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul"
  ],
  "series": [
    {
      "name": "Current Year",
      "unit": "",
      "data": [
        {
          "name": "",
          "value": "15000000"
        },
        {
          "name": "",
          "value": "10000000"
        },
        {
          "name": "",
          "value": "10500000"
        },
        {
          "name": "",
          "value": "11200000"
        },
        {
          "name": "",
          "value": "19000000"
        },
        {
          "name": "",
          "value": "20000000"
        },
        {
          "name": "",
          "value": "20300000"
        }
      ]
    },
    {
      "name": "Previous Year",
      "unit": "",
      "data": [
        {
          "name": "",
          "value": "10000000"
        },
        {
          "name": "",
          "value": "19000000"
        },
        {
          "name": "",
          "value": "18500000"
        },
        {
          "name": "",
          "value": "11200000"
        },
        {
          "name": "",
          "value": "12500000"
        },
        {
          "name": "",
          "value": "13300000"
        },
        {
          "name": "",
          "value": "20300000"
        }
      ]
    }
  ]
}
""",
            'pie_chart': """
{
  "type": "pie",
  "title": "Traffic by Location",
  "subtitle": "",
  "category": [],
  "series": [
    {
      "name": "",
      "unit": "%",
      "data": [
        {
          "name": "United States",
          "value": "38.6"
        },
        {
          "name": "Canada",
          "value": "22.5"
        },
        {
          "name": "Mexico",
          "value": "30.8"
        },
        {
          "name": "other",
          "value": "30.8"
        }
      ]
    }
  ]
}
""",
            'bar_chart': """{
  "title": "Traffic by Device",
  "subtitle": "",
  "type": "bar",
  "categories": [],
  "series": [
    {
      "name": "",
      "unit": "",
      "data": [
        {
          "name": "Linux",
          "value": "20000000"
        },
        {
          "name": "Mac",
          "value": "21000000"
        },
        {
          "name": "IOS",
          "value": "20500000"
        },
        {
          "name": "Windows",
          "value": "25000000"
        },
        {
          "name": "Android",
          "value": "10000000"
        },
        {
          "name": "Other",
          "value": "22000000"
        }
      ]
    }
  ]
}""",
            'theme_example': 'особенности в сфере цифровизации и новых технологических нововведениях',
            'template_example': """
Анализируем конкурентов в сфере металлургии в мире на их развитие в разных направлениях, в особенности в сфере цифровизации и новых технологических нововведениях.
Для реализации данной задачи необходима обработка/выжимка релевантной информации о металлургических компаниях.
1. Необходимо определиться с компанией-конкурентом
2. Информация должна быть изложена по разделам/блокам:

Блок 1: Основная информация о компании: «Визитная карточка»
1) головной офис,
2) Год основания,
3) количество сотрудников
4) Общая выручка за последний год в долларах/евро,
5) Объём производства стали за последний год в тоннах,

Блок 2: Обзор выручки с продаж и EBITDA по годам за последние 10 лет
1) объяснение причины релевантных роста и падения продаж

Блок 3: Обзор объёма производства стали в тоннах по годам за последние 10 лет
1) если имеется, также добычи железной руды в тоннах по годам за последние 10 лет;
2) объяснения причин релевантного падения или увеличения объёма производства

Блок 4: Структура компании
1) Разделение на девизионы внутри компании
2) Рынки сбыта компании по регионам/странам, уровень продаж
3) Рынки сбыта и уровень продаж компании по отраслям

Блок 5: Цифровизация компании
1) Цифровая стратегия и трансформация в компании
2) цифровые решения для улучшения производства, цепочек поставок, логистики, любые другие цифровые внедрения.
3) Цифровые продукты компании для продажи клиентам или оказываемый сервис («умная сталь») – по возможности с картинками

Блок 6: Тенденции будущего развития помимо цифровизации
1) например, декарбонизация;
2) введение новых технологий и продуктов, повышающих EBITDA;
3) открытие новых заводов и направлений производства;
4) выход на новые ниши рынка и т.д.

Блок 7: Технология производства
1) интересные, нестандартные, новые технологии производства и (конечной) обработки стали (напр. производство сверхдлинных рельсов, производство безуглеродной стали)

Блок 8: Исследования, разработки и образование
1) патенты,
2) исследовательские центры,
3) структуры образования,
4) сотрудничество с университетами,
5) собственные внутренние образовательные программы,
6) квалификационные программы,
7) инновационные проекты и т.д.
""",
        }

    async def generate_template(self, input_theme: str, model_name: str = 'gpt-4o'):
        chat = ChatOpenAI(
            base_url=app_settings.openai_api_url,
            api_key=app_settings.openai_api_key,
            model=model_name,
            streaming=True,
        )
        prompt_template = ChatPromptTemplate.from_messages([
            (
                'system',
                'Ты - умный помощник в составлении шаблонов отчётов по выбранной тематике. ПИШИ ВСЮ ИНФОРМАЦИЮ НА РУССКОМ ЯЗЫКЕ!',
            ),
            (
                'user',
                'Изучи данный шаблон и используй его как пример для построения своих шаблонов. Тема:\n{few_shot_theme}\n, сам текст шаблона:\n{few_shot_text}\n.',
            ),
            (
                'ai',
                'Хорошо, я внимательно изучил шаблон и буду стараться следовать ему, а именно придумывать правильные направления по изучения выбранной тематики, описывать детально и полноценно каждый из блоков и выделать 5-8 блоков для каждой тематики, используя по 3-4 пункта в каждом блоке! Я не буду повторять идеи, описанные в шаблоне дословно, а буду придумывать только релевантные идеи для выбранной темы!',
            ),
            (
                'user',
                'Подготовь, пожалуйста, для меня шаблон по выбранной теме:\n{input_theme}\n, напиши только шаблон, не отвечай мне никак, не пиши ничего лишнего, только сам шаблон!',
            ),
        ])
        prompt = prompt_template.format_messages(
            few_shot_theme=self.get_few_shot['theme_example'],
            few_shot_text=self.get_few_shot['template_example'],
            input_theme=input_theme,
        )
        async for chunk in chat.astream(prompt):
            yield chunk
