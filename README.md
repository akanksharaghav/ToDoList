# ToDoListApp

A simple Python command-line To-Do List Manager.  
Allows adding, viewing, editing, deleting, and completing tasks. Tasks are saved in `tasks.txt`.

---

## Project Structure

```
ToDoListApp/
│── todolist/           # Python package
│   └── main.py         # main CLI script
│── tasks.txt           # stores tasks
│── setup.py            # installation script
│── README.md
│── .gitignore
```

---

## Requirements

- Python 3.7 or higher  
- pip  

---

## Running the Project

### 1. Clone the repository

```bash
git clone <repo-url>
cd ToDoListApp
```

### 2. Install dependencies

```bash
pip install colorama
```

---

### 3. Run from source

```bash
python3 todolist/main.py
```

> Your tasks will be saved in `tasks.txt` in the project folder.

---

### 4. Install as a CLI command (optional)

If `setup.py` is included:

```bash
pip install -e .
```

- Run the app from anywhere using:

```bash
todo
```

> Tasks will be saved in the folder where the command is run.

---

## Features

- Add new tasks with a description and deadline (YYYY-MM-DD)  
- View tasks (Pending and Completed)  
- Edit tasks  
- Delete tasks  
- Mark tasks as completed  
- Tasks are persisted in `tasks.txt`  

---

## Notes

- `tasks.txt` will be created automatically if it doesn’t exist.  
- CLI colors are powered by `colorama`.  
- Using a virtual environment is recommended to keep dependencies isolated.  

---

## Cleaning Up

To remove Python build artifacts:

```bash
rm -rf __pycache__ *.pyc build dist *.spec
```

---

## License

MIT License

