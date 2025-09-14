from datetime import datetime
import os,sys
from colorama import Fore,Back,Style,init

init(autoreset=True)

TASKS_FILE="tasks.txt"
def get_project_dir():
    if getattr(sys, 'frozen', False):
        # Running from PyInstaller bundle → use the folder of the exe
        return os.path.dirname(sys.executable)
    else:
        # Running from source → use the folder where main.py is
        return os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = get_project_dir()
file_path = os.path.join(PROJECT_DIR, TASKS_FILE)

def validate_date(date_text):
    """
    Returns True if the date is valid and not in the past.
    Format: YYYY-MM-DD
    """
    try:
        input_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        today = datetime.today().date()
        if input_date < today:
            print(Fore.RED+"❌ Date cannot be in the past.")
            return False
        return True
    except ValueError:
        print(Fore.RED+"❌ Invalid date format. Use YYYY-MM-DD.")
        return False

def load_tasks():
    tasks=[]
    if os.path.exists(file_path):
        with open(file_path,"r") as file:
            for line in file:
                line=line.strip()
                if line:
                    task_id,task_description,task_deadline,task_status=line.split(",",3)
                    tasks.append([int(task_id),task_description,task_deadline,task_status])
    else:
        print(Fore.RED+"❌ File path not found:", file_path)
    return tasks

def save_tasks(tasks):
    try:
        with open(file_path, "w") as file:
            for task in tasks:
                file.write(f"{task[0]},{task[1]},{task[2]},{task[3]}\n")
        print(Fore.GREEN+"✅ Tasks saved successfully to:", file_path)
    except PermissionError:
        print(Fore.RED+"❌ Permission denied: cannot write to", file_path)
    except FileNotFoundError:
        print(Back.RED+"❌ File path not found:", file_path)
    except Exception as e:
        print(Back.RED+"❌ An unexpected error occurred while saving tasks:", e)


def add_task(tasks):
    task_id= 1 if len(tasks)==0 else tasks[-1][0]+1
    task_desc=input(Fore.BLUE+"📑 Enter task description: ")
    task_deadline=input(Fore.BLUE+"📆 Enter deadline (YYYY-MM-DD): ")
    if(validate_date(task_deadline)):
        task_status="Pending"
        tasks.append([task_id,task_desc,task_deadline,task_status])
        save_tasks(tasks)
        print(Fore.GREEN+"✅ Task added successfully!")
        return load_tasks()
    else:
        return tasks

def view_tasks(tasks):
    print()
    print(Back.LIGHTMAGENTA_EX+"📝 To-Do List:"+Style.RESET_ALL)
    pending_tasks=[t for t in tasks if t[3]=='Pending']
    pending_tasks.sort(key=lambda pt:datetime.strptime(pt[2], "%Y-%m-%d"))
    completed_tasks=[t for t in tasks if t[3]=='Completed']
    completed_tasks.sort(key=lambda ct:datetime.strptime(ct[2], "%Y-%m-%d"))
    print(Back.LIGHTMAGENTA_EX+Style.BRIGHT+"[Pending]")
    if len(pending_tasks)>0:
        for pending in pending_tasks:
            print(Fore.LIGHTYELLOW_EX+f"{pending[0]}. {pending[1]} - Deadline: {pending[2]}")
    else:
        print(Fore.LIGHTRED_EX+"❌ No pending tasks.")
    print()
    print(Back.LIGHTMAGENTA_EX+Style.BRIGHT+"[Completed]"+Style.RESET_ALL)
    if len(completed_tasks)>0:
        for completed in completed_tasks:
            print(Fore.LIGHTGREEN_EX+f"{completed[0]}. {completed[1]} - Deadline: {completed[2]}")
    else:
        print(Fore.LIGHTRED_EX+"❌ No completed tasks.")
    print()

def edit_task(tasks):
    view_tasks(tasks)
    try:
        task_id=int(input(Fore.BLUE+"👩🏻‍💻Enter task id to edit:"))
        for t in tasks:
            if t[0]== task_id:
                task_desc=input(Fore.BLUE+"🆕 Enter new description: ")
                task_deadline=input(Fore.BLUE+"🆕 Enter new task deadline (YYYY-MM-DD): ")
                if(validate_date(task_deadline)):
                    t[1],t[2]=task_desc,task_deadline
                    save_tasks(tasks)
                    print(Fore.GREEN+Style.BRIGHT+"✅Task updated successfully")
                    return load_tasks()
                else:
                    return tasks
        print(Fore.RED+"❌ Task not found.")
    except ValueError:
        print(Fore.RED+"❌ Invalid input.")
    return tasks

def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_id=int(input(Fore.BLUE+"👩🏻‍💻Enter task id to delete:"))
        new_tasks=[t for t in tasks if t[0]!=task_id]
        if len(new_tasks)==len(tasks):
            print(Fore.RED+"❌Task not found.")
        else:
            save_tasks(new_tasks)
            print(Fore.GREEN+Style.BRIGHT+"✅ Task deleted successfully")
            return load_tasks()
    except ValueError:
        print(Fore.RED+"❌ Invalid input.")
    return tasks

def mark_completed(tasks):
    view_tasks(tasks)
    try:
        task_id=int(input(Fore.BLUE+"👩🏻‍💻 Enter task id to mark as completed:"))
        for t in tasks:
            if t[0]==task_id:
                t[3]='Completed'
                save_tasks(tasks)
                print(Fore.GREEN+Style.BRIGHT+"✅ Task marked as completed!")
                return load_tasks()
    except ValueError:
        print(Fore.RED+"❌ Invalid input.")
    return tasks


def main():
    tasks=load_tasks()
    while(True):
        print()
        print(Back.LIGHTMAGENTA_EX+Style.BRIGHT+"📝 Welcome to To-Do List Manager! ✅"+Style.RESET_ALL)
        print(Fore.MAGENTA+"1. Add Task")
        print(Fore.MAGENTA+"2. View Tasks")
        print(Fore.MAGENTA+"3. Edit Task")
        print(Fore.MAGENTA+"4. Delete Task")
        print(Fore.MAGENTA+"5. Mark Task as completed.")
        print(Fore.MAGENTA+"6. Exit")
        
        choice=input(Fore.BLUE+"Enter your choice: ")

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
            print(Fore.GREEN+"Exiting To Do List Manager.Goodbye! 👋🏻")
            break
        else:
            print(Fore.RED+"❌ Invalid choice. Please try again.")

if __name__=='__main__':
    main()