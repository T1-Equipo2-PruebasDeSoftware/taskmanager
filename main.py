from app.tasks import create_task, update_task, delete_task, find_all_tasks
from utils.tasks_utils import print_task_list, print_task_details, print_all_tasks
from app.filters import filter_tasks_by_due_date, filter_tasks_by_tag, filter_tasks_by_status, search_tasks_by_title
from app.auth import authenticate

def main_menu():
    """
    Muestra el menú principal y permite al usuario seleccionar opciones para gestionar tareas.
    """
    while True:
        print("="*30)
        print("       Autenticación")
        print("="*30)
        username = input("Nombre de usuario: ")
        password = input("Contraseña: ")
        
        is_authenticated, message = authenticate(username, password)
        if not is_authenticated:
            print(message)
            continue  # Solicitar credenciales nuevamente si la autenticación falla
        
        while True:
            print("="*30)
            print("       Menú de Tareas")
            print("="*30)
            print("1. Crear tarea")
            print("2. Actualizar tarea")
            print("3. Eliminar tarea")
            print("4. Listar todas las tareas")
            print("5. Buscar tarea por ID")
            print("6. Filtrar/Buscar tareas")  # Nueva opción
            print("7. Salir")
            print("="*30)
            
            choice = input("Seleccione una opción (1-7): ")
            
            if choice == '1':
                title = input("Título: ")
                description = input("Descripción: ")
                due_date = input("Fecha de vencimiento (YYYY-MM-DD): ")
                tag = input("Etiqueta: ")
                task = {
                    "title": title,
                    "description": description,
                    "due_date": due_date,
                    "tag": tag,
                    "status": "pendiente"
                }
                result = create_task(task)
                print(result.message)
            
            elif choice == '2':
                tasks = find_all_tasks()
                if tasks.success:
                    print_task_list(tasks.data)
                    selected_id = int(input("Seleccione el ID de la tarea para actualizar: "))
                    task = next((t for t in tasks.data if t['id'] == selected_id), None)
                    if task:
                        status = input("Nuevo estado (pendiente, en progreso, completada): ")
                        task_update = {
                            "id": selected_id,
                            "status": status
                        }
                        result = update_task(task_update)
                        print(result.message)
                    else:
                        print("ID de tarea inválido.")
                else:
                    print(tasks.message)
            
            elif choice == '3':
                tasks = find_all_tasks()
                if tasks.success:
                    print_task_list(tasks.data)
                    task_id = int(input("ID de la tarea a eliminar: "))
                    result = delete_task(task_id)
                    print(result.message)
                else:
                    print(tasks.message)
            
            elif choice == '4':
                tasks = find_all_tasks()
                if tasks.success:
                    print_all_tasks(tasks.data)
                else:
                    print(tasks.message)
            
            elif choice == '5':
                tasks = find_all_tasks()
                if tasks.success:
                    print_task_list(tasks.data)
                    selected_id = int(input("Seleccione el ID de la tarea para ver detalles: "))
                    task = next((t for t in tasks.data if t['id'] == selected_id), None)
                    if task:
                        print_task_details(task)
                    else:
                        print("ID de tarea inválido.")
                else:
                    print(tasks.message)

            elif choice == '6':
                filter_and_search_tasks()
            elif choice == '7':
                print("Saliendo del programa...")
                return
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

def filter_and_search_tasks():
    """
    Muestra el menú para filtrar o buscar tareas y procesa la opción seleccionada por el usuario.
    """
    while True:
        print("="*30)
        print("     Filtrar o Buscar Tareas")
        print("="*30)
        print("1. Filtrar por fecha de vencimiento")
        print("2. Filtrar por etiqueta")
        print("3. Filtrar por estado")
        print("4. Buscar por título")
        print("5. Volver al menú principal")
        print("="*30)
        
        choice = input("Seleccione una opción (1-5): ")
        
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
        elif choice == '5':
            break  # Salir del bucle y volver al menú principal
        else:
            print("Opción inválida.")
            continue  # Volver a mostrar el menú de filtrado/búsqueda

        if result.success:
            print("="*30)
            print("     Resultados de Tareas")
            print("="*30)
            print_task_list(result.data)
        else:
            print("="*30)
            print(result.message)
            print("="*30)


if __name__ == "__main__":
    main_menu()