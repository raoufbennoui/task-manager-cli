# Task Manager CLI

A command-line task management application built with pure Python.
Manage your tasks directly from the terminal with priorities, 
categories, status tracking, and persistent storage.

## 🔗 Live Demo
```bash
python tasks.py help
```

## ✨ Features

- **Add tasks** with priority levels (high, medium, low)
- **Categorize tasks** by project or area (work, study, personal)
- **Track status** — pending, in-progress, done
- **Persistent storage** — tasks saved to JSON, survive between sessions
- **Statistics dashboard** — completion rate, progress bar, category breakdown
- **Filter tasks** — by status, priority, or category
- **Edit and delete** tasks
- **Zero dependencies** — pure Python standard library only

## 🚀 Getting Started
```bash
# Clone the repository
git clone https://github.com/raoufbennoui/task-manager-cli

# Run immediately — no install needed
python tasks.py help
```

## 📖 Usage
```bash
# Add tasks
python tasks.py add "Build hotel website" -p high -c work
python tasks.py add "Learn Flask" -p medium -c study
python tasks.py add "Apply for Masters" -p high -c personal

# View tasks
python tasks.py list
python tasks.py list --pending
python tasks.py list --high

# Update status
python tasks.py start 1
python tasks.py done 1

# Manage tasks
python tasks.py edit 2 "Learn Flask REST API"
python tasks.py delete 3
python tasks.py clear-done

# Statistics
python tasks.py stats
```

## 📊 Example Output
```
────────────────────────────────────────────────────────────
  ID   STATUS       PRI  TITLE                          CATEGORY
────────────────────────────────────────────────────────────
  1    ● DONE       🔴   Build hotel website            work
  2    ◑ IN-PROGRESS 🟡  Learn Flask REST API           study
  3    ○ PENDING    🔴   Apply for Masters              personal
────────────────────────────────────────────────────────────

  Total: 3  |  Done: 1  |  In Progress: 1  |  Pending: 1
  Progress: [████░░░░░░░░░░░░░░░░] 33%
```

## 🏗️ Architecture
```
tasks.py
├── Data Layer        → load_tasks(), save_tasks()
├── Business Logic    → add_task(), complete_task(), delete_task()
├── CLI Interface     → main(), argument parsing
└── tasks.json        → persistent data storage
```

## 🛠️ Tech Stack

- **Python 3** — core language
- **JSON** — data persistence
- **sys / os** — system operations
- **datetime** — timestamp tracking
- **Zero external dependencies**

## 💡 What I Learned

- Designing a clean separation between data, logic, and interface layers
- Implementing persistent storage without a database using JSON
- Building a real CLI interface similar to git or npm
- Error handling and input validation for robust user experience
- Applying Software Engineering principles from academic study 
  to a practical, usable tool

## 🔮 Future Improvements

- Due dates and deadline reminders
- Export tasks to CSV or PDF
- SQLite database instead of JSON for larger datasets
- Web interface using Flask
- Sync across devices via REST API

---

Built by Raouf Bennoui  
GitHub: [@raoufbennoui](https://github.com/raoufbennoui)
