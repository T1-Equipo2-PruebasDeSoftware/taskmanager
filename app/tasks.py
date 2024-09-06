import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, '../data/tasks.json')

class TaskResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

def create_task(task):
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            tasks_list = tasks_data.get('tasks', [])
            task['id'] = tasks_data['AUTOINCREMENT']
            task['status'] = 'pendiente'
            tasks_list.append(task)
            tasks_data['AUTOINCREMENT'] += 1
        with open(DATA_FILE, 'w') as file:
            json.dump(tasks_data, file, indent=2)
        return TaskResult(True, "Tarea creada exitosamente.")
    except FileNotFoundError:
        return TaskResult(False, "Error: El archivo tasks.json no fue encontrado.")

def update_task(task):
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            tasks_list = tasks_data.get('tasks', [])
            for i, t in enumerate(tasks_list):
                if t['id'] == task['id']:
                    tasks_list[i].update(task)
                    break
        with open(DATA_FILE, 'w') as file:
            json.dump(tasks_data, file, indent=2)
        return TaskResult(True, "Tarea actualizada exitosamente.")
    except FileNotFoundError:
        return TaskResult(False, "Error: El archivo tasks.json no fue encontrado.")

def delete_task(task_id):
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            tasks_list = tasks_data.get('tasks', [])
            task_exists = any(t['id'] == task_id for t in tasks_list)
            if not task_exists:
                return TaskResult(False, "Error: La tarea con el ID especificado no existe.")
            tasks_list = [t for t in tasks_list if t['id'] != task_id]
            tasks_data['tasks'] = tasks_list
        with open(DATA_FILE, 'w') as file:
            json.dump(tasks_data, file, indent=2)
        return TaskResult(True, "Tarea eliminada exitosamente.")
    except FileNotFoundError:
        return TaskResult(False, "Error: El archivo tasks.json no fue encontrado.")

def find_all_tasks():
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            return TaskResult(True, "Tareas encontradas.", tasks_data.get('tasks', []))
    except FileNotFoundError:
        return TaskResult(False, "Error: El archivo tasks.json no fue encontrado.")

def find_task_by_id(task_id):
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            task = next((t for t in tasks_data.get('tasks', []) if t['id'] == task_id), None)
            if task:
                return TaskResult(True, "Tarea encontrada.", task)
            else:
                return TaskResult(False, "Tarea no encontrada.")
    except FileNotFoundError:
        return TaskResult(False, "Error: El archivo tasks.json no fue encontrado.")