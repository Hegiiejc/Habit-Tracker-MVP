from datetime import datetime, timedelta
from typing import List
from models import CheckInEntry


class StreakCalculator:
    """Модуль 3: Метрики и Стрики"""

    @staticmethod
    def get_current_streak(entries: List[CheckInEntry], habit_id: int) -> int:
        """Текущая непрерывная серия выполнений до сегодня."""
        done = sorted(
            [e for e in entries if e.habit_id == habit_id and e.status == "done"],
            key=lambda x: x.date, reverse=True
        )
        streak = 0
        for i, entry in enumerate(done):
            expected = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            if entry.date == expected:
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def get_best_streak(entries: List[CheckInEntry], habit_id: int) -> int:
        """Лучший стрик за всё время."""
        done = sorted(
            [e for e in entries if e.habit_id == habit_id and e.status == "done"],
            key=lambda x: x.date
        )
        if not done:
            return 0
        best = current = 1
        for i in range(1, len(done)):
            prev = datetime.strptime(done[i-1].date, "%Y-%m-%d")
            curr = datetime.strptime(done[i].date, "%Y-%m-%d")
            if (curr - prev).days == 1:
                current += 1
                best = max(best, current)
            else:
                current = 1
        return best

    @staticmethod
    def get_monthly_rate(entries: List[CheckInEntry], habit_id: int, month: str) -> float:
        """Процент успешности за месяц (формат месяца: '2026-10')."""
        month_entries = [e for e in entries if e.habit_id == habit_id and e.date.startswith(month)]
        if not month_entries:
            return 0.0
        done = sum(1 for e in month_entries if e.status == "done")
        return round((done / len(month_entries)) * 100, 1)
