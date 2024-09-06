from tabulate import tabulate

def print_task_list(tasks):
    table = [[task['id'], task['title']] for task in tasks]
    headers = ["ID", "Título"]
    print(tabulate(table, headers, tablefmt="grid"))

def print_task_details(task):
    task_details = [
        ["Título", task["title"]],
        ["Descripción", task["description"]],
        ["Fecha de vencimiento", task["due_date"]],
        ["Etiqueta", task["tag"]],
        ["Estado", task["status"]]
    ]
    print("Detalles de la tarea:")
    print(tabulate(task_details, tablefmt="grid"))

def print_all_tasks(tasks):
    table = [[task['title'], task['status']] for task in tasks]
    headers = ["Título", "Estado"]
    print(tabulate(table, headers, tablefmt="grid"))