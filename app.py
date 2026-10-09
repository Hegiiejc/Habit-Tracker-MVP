from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from models import Habit, CheckInEntry
from services import StreakCalculator
from storage import HabitStorage

app = Flask(__name__)
storage = HabitStorage()


@app.route('/')
def index():
    habits, entries = storage.load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    today_ru = datetime.now().strftime("%d.%m.%Y")

    habits_data = []
    for habit in habits:
        if habit.is_active:
            streak = StreakCalculator.get_current_streak(entries, habit.id)
            today_entry = next(
                (e for e in entries if e.habit_id == habit.id and e.date == today), None
            )
            habits_data.append({
                'id': habit.id,
                'name': habit.name,
                'description': habit.description,
                'frequency': habit.frequency,
                'target_time': habit.target_time,
                'streak': streak,
                'completed_today': today_entry is not None and today_entry.status == 'done'
            })

    total_habits = len(habits_data)
    completed_today = sum(1 for h in habits_data if h['completed_today'])
    best_streak = max((h['streak'] for h in habits_data), default=0)

    return render_template(
        'index.html',
        habits=habits_data,
        today=today_ru,
        total_habits=total_habits,
        completed_today=completed_today,
        best_streak=best_streak
    )


@app.route('/add_habit', methods=['POST'])
def add_habit():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    frequency = request.form.get('frequency', 'daily')
    target_time = request.form.get('target_time', '09:00')
    if not name:
        return redirect(url_for('index'))

    habits, entries = storage.load_data()
    new_id = max([h.id for h in habits], default=0) + 1
    habits.append(Habit(id=new_id, name=name, description=description,
                        frequency=frequency, target_time=target_time))
    storage.save_data(habits, entries)
    return redirect(url_for('index'))


@app.route('/check_in', methods=['POST'])
def check_in():
    data = request.json
    habit_id = data.get('habit_id')
    note = data.get('note', '')
    habits, entries = storage.load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    existing = next((e for e in entries if e.habit_id == habit_id and e.date == today), None)
    if existing:
        return jsonify({'success': False, 'message': 'Уже отмечено сегодня'})
    entries.append(CheckInEntry(habit_id=habit_id, date=today, status='done', note=note))
    storage.save_data(habits, entries)
    return jsonify({'success': True})


@app.route('/archive_habit/<int:habit_id>', methods=['POST'])
def archive_habit(habit_id):
    habits, entries = storage.load_data()
    for h in habits:
        if h.id == habit_id:
            h.is_active = False
            break
    storage.save_data(habits, entries)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
