import json
import os
import logging
from datetime import datetime

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, '../data/tasks.json')

class TaskResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

def validate_task(task):
    if len(task['title']) > 50:
        return TaskResult(False, "Los títulos tienen un máximo de 50 caracteres.")
    if len(task['description']) > 250:
        return TaskResult(False, "Las descripciones tienen un máximo de 250 caracteres.")
    if len(task['tag']) > 20:
        return TaskResult(False, "Las etiquetas tienen un máximo de 20 caracteres.")
    if not task['title']:
        return TaskResult(False, "Los títulos de las tareas no pueden estar en blanco.")
    return TaskResult(True, "Tarea válida.")

def mark_overdue_tasks():
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            tasks_list = tasks_data.get('tasks', [])
            current_date = datetime.now().date()
            for task in tasks_list:
                due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                if due_date < current_date and task['status'] != 'completada':
                    task['status'] = 'atrasada'
        with open(DATA_FILE, 'w') as file:
            json.dump(tasks_data, file, indent=2)
        return TaskResult(True, "Tareas vencidas marcadas como atrasadas.")
    except FileNotFoundError:
        return TaskResult(False, "Error: El archivo tasks.json no fue encontrado.")
    except Exception as e:
        return TaskResult(False, f"Error: {str(e)}")

def create_task(task):
    try:
        datetime.strptime(task['due_date'], '%Y-%m-%d')
    except ValueError:
        return TaskResult(False, "Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")
    validation_result = validate_task(task)
    if not validation_result.success:
        return validation_result
    
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
        logging.info("Tarea creada exitosamente.")
        return TaskResult(True, "Tarea creada exitosamente.")
    except FileNotFoundError:
        logging.error("Error: No se encontró el archivo tasks.json.")
        return TaskResult(False, "Error: No se encontró el archivo tasks.json.")

def update_task(task):
    valid_statuses = ['pendiente', 'en progreso', 'completada', 'atrasada']
    if 'status' in task and task['status'] not in valid_statuses:
        return TaskResult(False, f"Error: Estado '{task['status']}' no válido. Use uno de {valid_statuses}.")
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
        logging.info("Tarea actualizada exitosamente.")
        return TaskResult(True, "Tarea actualizada exitosamente.")
    except FileNotFoundError:
        logging.error("Error: No se encontró el archivo tasks.json.")
        return TaskResult(False, "Error: No se encontró el archivo tasks.json.")
    except Exception as e:
        logging.error(f"Error al actualizar la tarea: {e}")
        return TaskResult(False, f"Error: {str(e)}")
def delete_task(task_id):
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            tasks_list = tasks_data.get('tasks', [])
            task_exists = any(t['id'] == task_id for t in tasks_list)
            if not task_exists:
                logging.error("Error: La tarea con el ID especificado no existe.")
                return TaskResult(False, "Error: La tarea con el ID especificado no existe.")
            tasks_list = [t for t in tasks_list if t['id'] != task_id]
            tasks_data['tasks'] = tasks_list
        with open(DATA_FILE, 'w') as file:
            json.dump(tasks_data, file, indent=2)
        logging.info("Tarea eliminada exitosamente.")
        return TaskResult(True, "Tarea eliminada exitosamente.")
    except FileNotFoundError:
        logging.error("Error: No se encontró el archivo tasks.json.")
        return TaskResult(False, "Error: No se encontró el archivo tasks.json.")

def find_all_tasks():
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            logging.info("Todas las tareas encontradas.")
            return TaskResult(True, "Todas las tareas encontradas.", tasks_data.get('tasks', []))
    except FileNotFoundError:
        logging.error("Error: No se encontró el archivo tasks.json.")
        return TaskResult(False, "Error: No se encontró el archivo tasks.json.")

def find_task_by_id(task_id):
    try:
        with open(DATA_FILE, 'r') as file:
            tasks_data = json.load(file)
            task = next((t for t in tasks_data.get('tasks', []) if t['id'] == task_id), None)
            if task:
                logging.info("Tarea encontrada.")
                return TaskResult(True, "Tarea encontrada.", task)
            else:
                logging.error("Tarea no encontrada.")
                return TaskResult(False, "Tarea no encontrada.")
    except FileNotFoundError:
        logging.error("Error: No se encontró el archivo tasks.json.")
        return TaskResult(False, "Error: No se encontró el archivo tasks.json.")