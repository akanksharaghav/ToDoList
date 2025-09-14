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
    """
    Loads tasks from the tasks file (file_path).

    - Checks if the file exists.
    - Reads each non-empty line from the file.
    - Splits the line into: task_id, task_description, task_deadline, task_status.
    - Converts task_id to an integer and appends the task as a list to tasks.
    - If file is not found, prints an error message in red.
    - Returns a list of tasks, where each task is represented as:
      [task_id (int), description (str), deadline (str), status (str)]
    """
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
    """
    Saves a list of tasks to the tasks file (file_path).

    - Opens the file in write mode ("w"), overwriting any existing content.
    - Writes each task as a comma-separated line in the format:
        task_id, task_description, task_deadline, task_status
    - If saving succeeds, prints a success message in green.
    - Handles possible errors:
        * PermissionError → No write permission for the file.
        * FileNotFoundError → Invalid file path.
        * Exception → Any other unexpected error.
    """
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
    """
    Adds a new task to the task list.

    - Generates a new task_id:
        * 1 if the task list is empty
        * Otherwise, last task's id + 1
    - Prompts the user for:
        * Task description
        * Task deadline (in YYYY-MM-DD format)
    - Validates the deadline format using validate_date().
        * If valid:
            - Creates a new task with status "Pending"
            - Appends it to the tasks list
            - Saves tasks to file using save_tasks()
            - Prints a success message
            - Reloads tasks from file and returns them
        * If invalid:
            - Returns the original tasks list unchanged
    """
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
    """
    Displays the list of tasks grouped into Pending and Completed sections.

    - Separates tasks into:
        * pending_tasks   → tasks with status "Pending"
        * completed_tasks → tasks with status "Completed"
    - Sorts both groups by their deadline date (ascending).
    - Prints:
        * A header for "Pending" tasks, followed by each task’s id, description, and deadline
          in yellow text (or a red warning if no pending tasks exist).
        * A header for "Completed" tasks, followed by each task’s id, description, and deadline
          in green text (or a red warning if no completed tasks exist).
    - Uses color formatting (via colorama) to highlight sections and improve readability.
    """
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
    """
    Allows the user to edit an existing task in the task list.

    Workflow:
    - Displays the current tasks by calling view_tasks().
    - Prompts the user to enter the task_id of the task they want to edit.
    - Searches the tasks list for a matching task_id.
        * If found:
            - Asks the user for a new description and a new deadline (YYYY-MM-DD).
            - Validates the deadline format using validate_date().
                · If valid → updates the task’s description and deadline,
                  saves changes to the file (via save_tasks()), prints success,
                  and reloads tasks (via load_tasks()).
                · If invalid → returns the original tasks unchanged.
        * If no matching task_id is found → prints a "Task not found" message.
    - Handles invalid input (non-integer task_id) with a ValueError exception.
    - Returns the updated tasks list (or original list if update fails).
    """
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
    """
    Deletes a task from the task list based on its task_id.

    Workflow:
    - Displays the current tasks by calling view_tasks().
    - Prompts the user to enter the task_id of the task they want to delete.
    - Creates a new list (new_tasks) that excludes the task with the given id.
        * If the length of new_tasks is the same as the original tasks list,
          it means the task_id was not found → prints an error message.
        * Otherwise:
            - Saves the updated list using save_tasks().
            - Prints a success message.
            - Reloads tasks from file (via load_tasks()) and returns them.
    - Handles invalid input (non-integer task_id) with a ValueError exception.
    - Returns the updated tasks list (or original list if deletion fails).
    """
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
    """
    Marks a specific task as completed in the task list.

    Workflow:
    - Displays the current tasks by calling view_tasks().
    - Prompts the user to enter the task_id of the task to mark as completed.
    - Searches the tasks list for the matching task_id.
        * If found:
            - Updates the task’s status to "Completed".
            - Saves the updated task list using save_tasks().
            - Prints a success message.
            - Reloads tasks from file (via load_tasks()) and returns them.
        * If not found:
            - No explicit "not found" message is shown; function simply returns tasks unchanged.
    - Handles invalid input (non-integer task_id) with a ValueError exception.
    - Returns the updated tasks list (or original list if marking fails).
    """
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
    """
    Main function to run the To-Do List Manager.

    Features:
    - Loads tasks from the file using load_tasks().
    - Displays a menu with options for the user:
        1. Add Task
        2. View Tasks
        3. Edit Task
        4. Delete Task
        5. Mark Task as Completed
        6. Exit
    - Executes the selected option by calling the respective function.
    - Updates the task list after operations like add, edit, delete, or mark completed.
    - Loops continuously until the user chooses to exit.
    - Provides colored, user-friendly CLI output.
    """
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