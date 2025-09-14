import os
TASKS_FILE="tasks.txt"
# Get absolute path of current file
script_dir = os.path.dirname(os.path.abspath(__file__))
# Build path to tasks.txt in same folder
file_path = os.path.join(script_dir, TASKS_FILE)

def load_tasks():
    tasks=[]
    if os.path.exists(file_path):
        with open(file_path,"r") as file:
            for line in file:
                line=line.strip()
                if line:
                    task_id,task_description,task_deadline,task_status=line.split(",",3)
                    tasks.append([int(task_id),task_description,task_deadline,task_status])
    return tasks

def save_tasks(tasks):
    with open(file_path,"w") as file:
        for task in tasks:
            file.write(f"{task[0]},{task[1]},{task[2]},{task[3]}")


def add_task(tasks):
    task_id= 1 if len(tasks)==0 else tasks[-1][0]+1
    task_desc=input("Enter task description: ")
    task_deadline=input("Enter deadline (YYYY-MM-DD): ")
    task_status="Pending"
    tasks.add([task_id,task_desc,task_deadline,task_status])
    save_tasks()
    print("Task added successfully!")
    return load_tasks()

def view_tasks(tasks):
    print("\nTo-Do List:")
    pending_tasks=[t for t in tasks if t[3]=='Pending']
    completed_tasks=[t for t in tasks if t[3]=='Completed']
    print("[Pending]")
    if len(pending_tasks)>0:
        for pending in pending_tasks:
            print(f"{pending[0]}. {pending[1]} - Deadline: {pending[2]}")
    else:
        print("No pending tasks.")
    print("\n[Completed]")
    if len(completed_tasks)>0:
        for completed in completed_tasks:
            print(f"{pending[0]}. {pending[1]} - Deadline: {pending[2]}")
    else:
        print("No completed tasks.")
    print()

def edit_task(tasks):
    view_tasks(tasks)
    try:
        task_id=int(input("Enter task id to edit:"))
        for t in tasks:
            if t[0]== task_id:
                task_desc=input("Enter new description: ")
                task_deadline=input("Enter new task deadline (YYYY-MM-DD): ")
                t[1],t[2]=task_desc,task_deadline
                save_tasks(tasks)
                print("Task updated successfully")
                return load_tasks()
        print("Task not found.")
    except ValueError:
        print("Invalid input.")
    return tasks

def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_id=int(input("Enter task id to delete:"))
        tasks=[t for t in tasks if t[0]!=task_id]
        save_tasks(tasks)
        print("Task deleted successfully")
        return load_tasks()
    except ValueError:
        print("Invalid input.")
    return tasks

def mark_completed(tasks):
    view_tasks()
    try:
        task_id=int(input("Enter task id to mark as completed:"))
        for t in tasks:
            if t[0]==task_id:
                t[3]='Completed'
                save_tasks(tasks)
                print("Task marked as completed!")
                return load_tasks()
    except ValueError:
        print("Invalid input.")
    return tasks


def main():
    tasks=load_tasks()
    while(True):
        print("\nWelcome to To-Do List Manager!")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Mark Task as completed.")
        print("6. Exit")
        
        choice=input("Enter your choice: ")

        if choice=='1':
            tasks=add_task(tasks)
        elif choice=='2':
            view_tasks(tasks)
        elif choice=='3':
            tasks=edit_task(tasks)
        elif choice=='4':
            tasks=delete_task(tasks)
        elif choice=='5':
            tasks=mark_completed(tasks)
        elif choice=='6':
            print("Exiting To Do List Manager.Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")