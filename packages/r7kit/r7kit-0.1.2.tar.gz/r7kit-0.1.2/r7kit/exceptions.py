# === ПУТЬ К ФАЙЛУ: r7kit/exceptions.py ===
class TaskNotFoundError(ValueError):
    """Задача не найдена или уже удалена."""

class TaskAlreadyExistsError(ValueError):
    """Повторная попытка создать задачу с тем же UUID."""

class TemporalNotConnected(RuntimeError):
    """Не удалось подключиться к Temporal при submit_workflow."""
