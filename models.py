from dataclasses import dataclass
from typing import Optional


@dataclass
class Habit:
    """Модуль 1: Менеджер привычек"""
    id: int
    name: str
    description: str
    frequency: str       # 'daily' или 'weekly'
    target_time: str     # например '09:00'
    is_active: bool = True


@dataclass
class CheckInEntry:
    """Модуль 2: Журнал отметок"""
    habit_id: int
    date: str            # формат YYYY-MM-DD
    status: str          # 'done' или 'skipped'
    note: Optional[str] = ""
