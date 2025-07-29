# r7kit

**R7kit** — это лёгкий фреймворк для управления задачами (tasks) и воркфлоу (workflows) с использованием Temporal и Redis.

## Особенности

- Поддержка task lifecycle: создание, патчинг, удаление
- Асинхронные activities с Lua-сценариями для Redis
- Удобная сериализация и retry-политики
- Базовые и stateful workflow-классы
- Готов к production: singleton-клиенты, TTL, логгинг

## Установка

```bash
pip install /path/to/r7kit-0.1.0-py3-none-any.whl
```

Или, если ты собрал `.tar.gz`:

```bash
pip install /path/to/r7kit-0.1.0.tar.gz
```

## Пример: запуск воркфлоу

```python
from r7kit.workflow_utils import submit_workflow

handle = await submit_workflow(
    "your_pipeline.HelloPipeline",
    payload={"user": "Ann"},
)
print("Started workflow:", handle.id)
```

## Структура

| Модуль | Назначение |
|--------|------------|
| `r7kit.activities` | Activities для Temporal |
| `r7kit.tasks`      | Хелперы для работы с Redis-задачами |
| `r7kit.workflow_utils` | Запуск воркфлоу (submit, child) |
| `r7kit/base_workflow.py` | Базовая логика `get_task`, `patch_task` и т.д. |
| `r7kit/stateful_workflow.py` | Автосохранение состояния между активациями |
| `r7kit/config.py` | Конфигурация (Redis, Temporal) |
| `r7kit/serializer.py` | Безопасная сериализация payload-ов |

## Лицензия

MIT
