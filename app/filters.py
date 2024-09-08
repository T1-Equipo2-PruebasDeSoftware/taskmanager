import logging
from datetime import datetime
from app.tasks import find_all_tasks
from utils.tasks_utils import print_task_list
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

class FilterResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

def filter_tasks_by_due_date(start_date=None, end_date=None):
    try:
        tasks = find_all_tasks()
        if not tasks.success:
            logging.error(tasks.message)
            return FilterResult(False, tasks.message)
        
        filtered_tasks = tasks.data
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                logging.error("Error: Formato de fecha de inicio incorrecto.")
                return FilterResult(False, "Error: Formato de fecha de inicio incorrecto.")
                
            filtered_tasks = [t for t in filtered_tasks if 'due_date' in t and datetime.strptime(t['due_date'], "%Y-%m-%d") >= start_date]
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                logging.error("Error: Formato de fecha de fin incorrecto.")
                return FilterResult(False, "Error: Formato de fecha de fin incorrecto.")
                
            filtered_tasks = [t for t in filtered_tasks if 'due_date' in t and datetime.strptime(t['due_date'], "%Y-%m-%d") <= end_date]
        
        if start_date and end_date and start_date > end_date:
            logging.error("Error: La fecha de inicio no puede ser posterior a la fecha de fin.")
            return FilterResult(False, "Error: La fecha de inicio no puede ser posterior a la fecha de fin.")
        
        return FilterResult(True, "Tareas filtradas por fecha de vencimiento.", filtered_tasks)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return FilterResult(False, f"Error: {str(e)}")


def filter_tasks_by_tag(tag):
    tasks = find_all_tasks()
    if not tasks.success:
        logging.error(tasks.message)
        return FilterResult(False, tasks.message)
    
    filtered_tasks = [t for t in tasks.data if t['tag'].lower() == tag.lower()]
    
    if not filtered_tasks:
        logging.warning(f"No existen tareas con la etiqueta: {tag}.")
        return FilterResult(False, f"No existen tareas con la etiqueta: {tag}.")
    
    return FilterResult(True, f"Tareas filtradas por etiqueta: {tag}.", filtered_tasks)

def filter_tasks_by_status(status):
    valid_statuses = ['pendiente', 'en progreso', 'completada', 'atrasada']
    if status not in valid_statuses:
        logging.error(f"Estado '{status}' no válido. Use 'pendiente', 'en progreso', 'completada' o 'atrasada.'")
        return FilterResult(False, f"Error: Estado '{status}' no válido. Use 'pendiente', 'en progreso', 'completada' o 'atrasada.'")
    
    tasks = find_all_tasks()
    if not tasks.success:
        logging.error(tasks.message)
        return FilterResult(False, tasks.message)
    
    filtered_tasks = [t for t in tasks.data if t['status'] == status]
    
    if not filtered_tasks:
        logging.warning(f"No se encontraron tareas con el estado: {status}.")
        return FilterResult(False, f"No se encontraron tareas con el estado: {status}.")
    
    return FilterResult(True, f"Tareas encontradas con el estado: {status}.", filtered_tasks)

def search_tasks_by_title(title):
    if not title:
        logging.error("No se proporcionó un título para buscar.")
        return FilterResult(False, "No se proporcionó un título para buscar.")
    
    tasks = find_all_tasks()
    if not tasks.success:
        logging.error(tasks.message)
        return FilterResult(False, tasks.message)
    
    filtered_tasks = [t for t in tasks.data if title.lower() in t['title'].lower()]
    
    if not filtered_tasks:
        logging.warning(f"No se encontraron tareas con el título: {title}.")
        return FilterResult(False, f"No se encontraron tareas con el título: {title}.")
    
    return FilterResult(True, f"Tareas encontradas con el título: {title}.", filtered_tasks)

def filter_and_search_tasks():
    logging.info("Filtrar o buscar tareas:")
    logging.info("1. Filtrar por fecha de vencimiento")
    logging.info("2. Filtrar por etiqueta")
    logging.info("3. Filtrar por estado")
    logging.info("4. Buscar por título")
    
    choice = input("Seleccione una opción (1-4): ")
    
    if choice == '1':
        start_date = input("Fecha de inicio (YYYY-MM-DD) o presione Enter para omitir: ")
        end_date = input("Fecha de fin (YYYY-MM-DD) o presione Enter para omitir: ")
        result = filter_tasks_by_due_date(start_date if start_date else None, end_date if end_date else None)
    elif choice == '2':
        tag = input("Etiqueta a filtrar: ")
        result = filter_tasks_by_tag(tag)
    elif choice == '3':
        status = input("Estado (pendiente, en progreso, completada, atrasada): ")
        result = filter_tasks_by_status(status)
    elif choice == '4':
        title = input("Título o parte del título: ")
        result = search_tasks_by_title(title)
    else:
        logging.error("Opción no válida.")
        result = FilterResult(False, "Opción no válida.")
    
    if result.success:
        logging.info(result.message)
        for task in result.data:
            logging.info(task)
    else:
        logging.warning(result.message)
