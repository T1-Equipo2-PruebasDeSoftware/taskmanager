from app.tasks import create_task, update_task, delete_task, find_all_tasks
from utils.tasks_utils import print_task_list, print_task_details, print_all_tasks

def main_menu():
    while True:
        print("="*30)
        print("       Menú de Tareas")
        print("="*30)
        print("1. Crear tarea")
        print("2. Actualizar tarea")
        print("3. Eliminar tarea")
        print("4. Listar todas las tareas")
        print("5. Buscar tarea por ID")
        print("6. Salir")
        print("="*30)
        
        choice = input("Seleccione una opción (1-6): ")
        
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
            print("Saliendo del programa...")
            break
        
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main_menu()