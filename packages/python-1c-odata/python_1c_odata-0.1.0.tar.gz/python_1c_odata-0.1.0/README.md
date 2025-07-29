# python-1c-odata

Библиотека для работы с 1С через протокол OData. Поддерживает асинхронные операции с документами, справочниками и регистрами.

## Установка

```bash
pip install python-1c-odata
```

## Основные возможности

- Асинхронная работа с документами (создание, чтение, проведение)
- Работа со справочниками (создание, чтение, изменение)
- Работа с регистрами сведений и накопления
- Поддержка фильтрации, выборки и расширения данных

## Примеры использования

```python
import asyncio
from odata.core import Infobase
from odata.document import Document
from odata.catalog import Catalog
from odata.informationregister import InformationRegister

async def main():
    # Подключение к 1С
    infobase = Infobase(
        server="http://your-server",
        infobase="your-infobase",
        username="your-username",
        password="your-password"
    )

    # Работа с документами
    doc = Document(infobase, "Документ")
    docs = await doc.query(
        top=10,
        select="Ref_Key,Number,Date",
        odata_filter="Date ge datetime'2024-01-01T00:00:00'"
    )

    # Работа со справочником
    catalog = Catalog(infobase, "Справочник")
    items = await catalog.query(
        top=100,
        select="Ref_Key,Description"
    )

    # Работа с регистром
    register = InformationRegister(infobase, "Регистр")
    data = await register.slice_last(
        period="2024-03-20T00:00:00",
        select="Period,RecordKey,Value"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

## Требования

- Python 3.7+
- aiohttp

## Лицензия

MIT
