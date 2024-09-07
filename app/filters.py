from datetime import datetime
from app.tasks import find_all_tasks
from utils.tasks_utils import print_task_list

class FilterResult:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

from datetime import datetime

def filter_tasks_by_due_date(start_date=None, end_date=None):
    """
    Filtra tareas por fecha de vencimiento.

    Args:
        start_date (str): Fecha de inicio en formato YYYY-MM-DD.
        end_date (str): Fecha de fin en formato YYYY-MM-DD.

    Returns:
        FilterResult: Resultado del filtrado, con éxito o mensaje de error.
    """
    try:
        tasks = find_all_tasks()
        if not tasks.success:
            return FilterResult(False, tasks.message)
        
        filtered_tasks = tasks.data
        
        # Convierte las fechas de inicio y fin si están presentes
        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                return FilterResult(False, "Error: Formato de fecha de inicio incorrecto.")
                
            filtered_tasks = [t for t in filtered_tasks if 'due_date' in t and datetime.strptime(t['due_date'], "%Y-%m-%d") >= start_date]
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                return FilterResult(False, "Error: Formato de fecha de fin incorrecto.")
                
            filtered_tasks = [t for t in filtered_tasks if 'due_date' in t and datetime.strptime(t['due_date'], "%Y-%m-%d") <= end_date]
        
        if start_date and end_date and start_date > end_date:
            return FilterResult(False, "Error: La fecha de inicio no puede ser posterior a la fecha de fin.")
        
        return FilterResult(True, "Tareas filtradas por fecha de vencimiento.", filtered_tasks)
    except Exception as e:
        return FilterResult(False, f"Error: {str(e)}")


def filter_tasks_by_tag(tag):
    """
    Filtra tareas por etiqueta.

    Args:
        tag (str): Etiqueta para filtrar.

    Returns:
        FilterResult: Resultado del filtrado, con éxito o mensaje de error.
    """
    tasks = find_all_tasks()
    if not tasks.success:
        return FilterResult(False, tasks.message)
    
    filtered_tasks = [t for t in tasks.data if t['tag'].lower() == tag.lower()]
    
    if not filtered_tasks:
        return FilterResult(False, f"No existen tareas con la etiqueta: {tag}.")
    
    return FilterResult(True, f"Tareas filtradas por etiqueta: {tag}.", filtered_tasks)

def filter_tasks_by_status(status):
    """
    Filtra tareas por estado.

    Args:
        status (str): Estado para filtrar.

    Returns:
        FilterResult: Resultado del filtrado, con éxito o mensaje de error.
    """
    tasks = find_all_tasks()
    if not tasks.success:
        return FilterResult(False, tasks.message)
    
    status = status.lower()  # Convertir estado ingresado a minúsculas
    
    filtered_tasks = [t for t in tasks.data if t['status'].lower() == status]
    
    if not filtered_tasks:
        return FilterResult(False, f"No se encontraron tareas con el estado: {status}.")
    
    return FilterResult(True, f"Tareas filtradas por estado: {status}.", filtered_tasks)

def search_tasks_by_title(title):
    """
    Busca tareas por título.

    Args:
        title (str): Título o parte del título para buscar.

    Returns:
        FilterResult: Resultado de la búsqueda, con éxito o mensaje de error.
    """
    if not title:  # Verifica si el título está vacío
        return FilterResult(False, "No se proporcionó un título para buscar.")
    
    tasks = find_all_tasks()
    if not tasks.success:
        return FilterResult(False, tasks.message)
    
    filtered_tasks = [t for t in tasks.data if title.lower() in t['title'].lower()]
    
    if not filtered_tasks:
        return FilterResult(False, f"No se encontraron tareas con el título: {title}.")
    
    return FilterResult(True, f"Tareas encontradas con el título: {title}.", filtered_tasks)

def filter_and_search_tasks():
    """
    Muestra el menú para filtrar o buscar tareas y procesa la opción seleccionada por el usuario.
    """
    print("Filtrar o buscar tareas:")
    print("1. Filtrar por fecha de vencimiento")
    print("2. Filtrar por etiqueta")
    print("3. Filtrar por estado")
    print("4. Buscar por título")
    
    choice = input("Seleccione una opción (1-4): ")
    
    if choice == '1':
        start_date = input("Fecha de inicio (YYYY-MM-DD) o presione Enter para omitir: ")
        end_date = input("Fecha de fin (YYYY-MM-DD) o presione Enter para omitir: ")
        result = filter_tasks_by_due_date(start_date if start_date else None, end_date if end_date else None)
    elif choice == '2':
        tag = input("Etiqueta a filtrar: ")
        result = filter_tasks_by_tag(tag)
    elif choice == '3':
        status = input("Estado (pendiente, en progreso, completada): ")
        result = filter_tasks_by_status(status)
    elif choice == '4':
        title = input("Título o parte del título: ")
        result = search_tasks_by_title(title)
    else:
        print("Opción inválida.")
        return
    
    if result.success:
        print("Mostrando tareas:")
        print_task_list(result.data)
    else:
        print(result.message)