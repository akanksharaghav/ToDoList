# ToDoListApp

A Python command-line To-Do List Manager with deadline validation.  
Allows adding, viewing, editing, deleting, and completing tasks. Tasks are saved in `todolist/tasks.txt` in the project folder.

---

## Project Structure

```
ToDoListApp/
│── todolist/           # Python package
│   └── main.py         # main CLI script
│   └── tasks.txt       # stores tasks (auto-created)
│── setup.py            # optional installation script
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

> Tasks will be saved in `todolist/tasks.txt` in the project folder.

---

### 4. Optional: Install as a CLI command

If `setup.py` is provided:

```bash
pip install -e .
```

- Run the app from anywhere using:

```bash
todo
```

> Tasks will be saved in the `todolist` folder where the command is run.

---

## Features

- Add new tasks with a description and **deadline (YYYY-MM-DD)**  
- Validates date format and prevents past dates  
- View tasks (Pending and Completed) sorted by deadline  
- Edit tasks  
- Delete tasks  
- Mark tasks as completed  
- Tasks are persisted in `todolist/tasks.txt`  

---

## Notes

- `todolist/tasks.txt` is auto-created if it doesn’t exist  
- CLI colors are powered by `colorama`  
- Use a virtual environment to isolate dependencies  
- Sorting ensures earliest deadlines appear first  

---

## Cleaning Up

To remove Python build artifacts:

```bash
rm -rf __pycache__ *.pyc build dist *.spec
```

---

## License

MIT License

