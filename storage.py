import json
import os
from typing import List, Tuple
from models import Habit, CheckInEntry


class HabitStorage:
    """Модуль 4: Хранение данных"""
    FILE_NAME = "data.json"

    @staticmethod
    def save_data(habits: List[Habit], entries: List[CheckInEntry]):
        data = {
            "habits": [h.__dict__ for h in habits],
            "entries": [e.__dict__ for e in entries]
        }
        with open(HabitStorage.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_data() -> Tuple[List[Habit], List[CheckInEntry]]:
        if not os.path.exists(HabitStorage.FILE_NAME):
            return [], []
        with open(HabitStorage.FILE_NAME, "r", encoding="utf-8") as f:
            data = json.load(f)
        habits = [Habit(**h) for h in data.get("habits", [])]
        entries = [CheckInEntry(**e) for e in data.get("entries", [])]
        return habits, entries
