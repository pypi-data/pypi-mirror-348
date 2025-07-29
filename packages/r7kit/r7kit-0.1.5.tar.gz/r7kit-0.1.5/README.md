# r7kit

**R7kit** — это лёгкий, модульный фреймворк для управления задачами (tasks) и воркфлоу (workflows) с использованием [Temporal](https://temporal.io/) и [Redis](https://redis.io/).

Он упрощает реализацию pipeline-процессов и сохранение состояний, с полной поддержкой асинхронных activity и потоковых логов.

---

## 🚀 Быстрый старт

### Создание задачи и запуск workflow:

```python
from r7kit.workflow_utils import submit_workflow

handle = await submit_workflow(
    "my_pipeline.HelloPipeline",
    payload={"user": "Ann"},
)
print("Workflow started:", handle.id)
```

### Получение и обновление задачи:

```python
from r7kit.tasks import get_task, patch_task

task = await get_task(task_id)
await patch_task(task_id, {"status": "running"})
```

---

## 📦 Основные возможности

- ✅ Создание, обновление, удаление задач в Redis
- 🔁 Версионирование и TTL ключей
- 🧠 Поддержка `BaseWorkflow` и `StatefulWorkflow` для управления логикой
- 🔌 Простая интеграция с Temporal SDK (Python)
- 📜 Сериализация `payload` с `orjson`, совместимость и безопасность
- ⚙️ Конфигурация через переменные окружения или `configure()`

---

## 📁 Структура модулей

| Модуль | Назначение |
|--------|------------|
| `activities.py` | Temporal Activity (создание, патчинг, удаление задач) |
| `tasks.py` | API для запуска и получения задач |
| `workflow_utils.py` | Утилиты для запуска и управления воркфлоу |
| `base_workflow.py` | Базовый класс с task API |
| `stateful_workflow.py` | Автоматическое сохранение `state` |
| `redis_client.py` | Singleton Redis-клиент с reconnect |
| `temporal_client.py` | Singleton Temporal-клиент |
| `serializer.py` | Безопасная сериализация payload-ов |
| `config.py` | Конфигурация (Redis, Temporal адреса) |
| `exceptions.py` | Исключения: NotFound, Conflict, AlreadyExists |

---

## 🧪 Пример pipeline

```python
from temporalio import workflow
from r7kit.base_task_workflow import BaseTaskWorkflow

@workflow.defn
class HelloPipeline(BaseTaskWorkflow):
    @workflow.run
    async def run(self, task_id: str):
        await self._run_impl(task_id)

    async def handle(self) -> None:
        await self.patch_task({"status": "started"})
        await workflow.sleep(3)
        await self.patch_task({"status": "done"})
```

---

## 📝 Лицензия

MIT
