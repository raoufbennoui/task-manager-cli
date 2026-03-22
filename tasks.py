#!/usr/bin/env python3
"""
Task Manager CLI
A command-line task management application
Author: Raouf
"""

import json
import os
import sys
from datetime import datetime


# ─────────────────────────────────────────────
# DATA LAYER — handles reading/writing to file
# ─────────────────────────────────────────────

DATA_FILE = "tasks.json"


def load_tasks():
    """Load tasks from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Error reading tasks file. Starting fresh.")
        return []


def save_tasks(tasks):
    """Save tasks to JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(tasks, f, indent=2)
    except IOError as e:
        print(f"Error saving tasks: {e}")
        sys.exit(1)


# ─────────────────────────────────────────────
# BUSINESS LOGIC — core task operations
# ─────────────────────────────────────────────

def generate_id(tasks):
    """Generate a unique incrementing ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(title, priority="medium", category="general"):
    """Add a new task."""
    if not title.strip():
        print("Error: Task title cannot be empty.")
        return

    tasks = load_tasks()
    task = {
        "id": generate_id(tasks),
        "title": title.strip(),
        "priority": priority.lower(),
        "category": category.lower(),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completed_at": None
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✓ Task added: [{task['id']}] {task['title']} ({task['priority']} priority)")


def list_tasks(filter_status=None, filter_priority=None, filter_category=None):
    """List all tasks with optional filters."""
    tasks = load_tasks()

    if not tasks:
        print("No tasks found. Add one with: python tasks.py add \"Your task\"")
        return

    # Apply filters
    filtered = tasks
    if filter_status:
        filtered = [t for t in filtered if t["status"] == filter_status]
    if filter_priority:
        filtered = [t for t in filtered if t["priority"] == filter_priority]
    if filter_category:
        filtered = [t for t in filtered if t["category"] == filter_category]

    if not filtered:
        print("No tasks match your filter.")
        return

    # Priority colors/symbols
    priority_symbol = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    status_symbol = {"pending": "○", "in-progress": "◑", "done": "●"}

    print("\n" + "─" * 60)
    print(f"  {'ID':<4} {'STATUS':<12} {'PRI':<3} {'TITLE':<30} {'CATEGORY'}")
    print("─" * 60)

    for task in filtered:
        pri = priority_symbol.get(task["priority"], "⚪")
        sta = status_symbol.get(task["status"], "?")
        title = task["title"][:28] + ".." if len(task["title"]) > 28 else task["title"]
        status_display = task["status"].upper()
        print(f"  {task['id']:<4} {sta} {status_display:<10} {pri}  {title:<30} {task['category']}")

    print("─" * 60)

    # Summary
    total = len(tasks)
    done = len([t for t in tasks if t["status"] == "done"])
    pending = len([t for t in tasks if t["status"] == "pending"])
    in_progress = len([t for t in tasks if t["status"] == "in-progress"])

    print(f"\n  Total: {total}  |  Done: {done}  |  In Progress: {in_progress}  |  Pending: {pending}")
    if total > 0:
        completion = round((done / total) * 100)
        bar = "█" * (completion // 5) + "░" * (20 - completion // 5)
        print(f"  Progress: [{bar}] {completion}%\n")


def complete_task(task_id):
    """Mark a task as done."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "done":
                print(f"Task [{task_id}] is already completed.")
                return
            task["status"] = "done"
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(tasks)
            print(f"✓ Task completed: [{task_id}] {task['title']}")
            return
    print(f"Error: Task [{task_id}] not found.")


def start_task(task_id):
    """Mark a task as in-progress."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "done":
                print(f"Task [{task_id}] is already completed.")
                return
            task["status"] = "in-progress"
            save_tasks(tasks)
            print(f"◑ Task started: [{task_id}] {task['title']}")
            return
    print(f"Error: Task [{task_id}] not found.")


def delete_task(task_id):
    """Delete a task by ID."""
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) == original_count:
        print(f"Error: Task [{task_id}] not found.")
        return

    save_tasks(tasks)
    print(f"✓ Task [{task_id}] deleted.")


def edit_task(task_id, new_title):
    """Edit a task title."""
    if not new_title.strip():
        print("Error: Title cannot be empty.")
        return

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            old_title = task["title"]
            task["title"] = new_title.strip()
            save_tasks(tasks)
            print(f"✓ Task [{task_id}] updated:")
            print(f"   Before: {old_title}")
            print(f"   After:  {new_title.strip()}")
            return
    print(f"Error: Task [{task_id}] not found.")


def clear_done():
    """Remove all completed tasks."""
    tasks = load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if t["status"] != "done"]
    after = len(tasks)
    removed = before - after

    if removed == 0:
        print("No completed tasks to clear.")
        return

    save_tasks(tasks)
    print(f"✓ Cleared {removed} completed task(s).")


def show_stats():
    """Show task statistics."""
    tasks = load_tasks()

    if not tasks:
        print("No tasks yet.")
        return

    total = len(tasks)
    done = len([t for t in tasks if t["status"] == "done"])
    pending = len([t for t in tasks if t["status"] == "pending"])
    in_progress = len([t for t in tasks if t["status"] == "in-progress"])

    high = len([t for t in tasks if t["priority"] == "high"])
    medium = len([t for t in tasks if t["priority"] == "medium"])
    low = len([t for t in tasks if t["priority"] == "low"])

    categories = {}
    for task in tasks:
        cat = task["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\n" + "═" * 40)
    print("  TASK STATISTICS")
    print("═" * 40)
    print(f"  Total tasks    : {total}")
    print(f"  Completed      : {done} ({round(done/total*100)}%)")
    print(f"  In progress    : {in_progress}")
    print(f"  Pending        : {pending}")
    print()
    print(f"  🔴 High priority   : {high}")
    print(f"  🟡 Medium priority : {medium}")
    print(f"  🟢 Low priority    : {low}")
    print()
    print("  CATEGORIES:")
    for cat, count in sorted(categories.items(),
                              key=lambda x: x[1], reverse=True):
        bar = "█" * count
        print(f"  {cat:<15} {bar} ({count})")
    print("═" * 40 + "\n")


# ─────────────────────────────────────────────
# CLI INTERFACE — parses command line arguments
# ─────────────────────────────────────────────

def show_help():
    print("""
╔══════════════════════════════════════════════╗
║           TASK MANAGER CLI                  ║
║           by Raouf                          ║
╚══════════════════════════════════════════════╝

USAGE:
  python tasks.py <command> [arguments]

COMMANDS:
  add <title>                Add a new task
  add <title> -p <priority>  Add with priority (high/medium/low)
  add <title> -c <category>  Add with category
  list                       List all tasks
  list --pending             List only pending tasks
  list --done                List only completed tasks
  list --high                List high priority tasks
  start <id>                 Mark task as in-progress
  done <id>                  Mark task as completed
  delete <id>                Delete a task
  edit <id> <new title>      Edit task title
  stats                      Show statistics
  clear-done                 Remove all completed tasks
  help                       Show this help message

EXAMPLES:
  python tasks.py add "Build hotel website" -p high -c work
  python tasks.py add "Learn Python" -p medium -c study
  python tasks.py list
  python tasks.py list --pending
  python tasks.py start 1
  python tasks.py done 1
  python tasks.py delete 2
  python tasks.py edit 3 "Build dental clinic website"
  python tasks.py stats
  python tasks.py clear-done
""")


def main():
    args = sys.argv[1:]

    if not args or args[0] == "help":
        show_help()
        return

    command = args[0].lower()

    if command == "add":
        if len(args) < 2:
            print("Usage: python tasks.py add \"Task title\" [-p priority] [-c category]")
            return
        title = args[1]
        priority = "medium"
        category = "general"
        if "-p" in args:
            idx = args.index("-p")
            if idx + 1 < len(args):
                p = args[idx + 1].lower()
                if p in ["high", "medium", "low"]:
                    priority = p
                else:
                    print("Priority must be: high, medium, or low")
                    return
        if "-c" in args:
            idx = args.index("-c")
            if idx + 1 < len(args):
                category = args[idx + 1].lower()
        add_task(title, priority, category)

    elif command == "list":
        status_filter = None
        priority_filter = None
        if "--pending" in args:
            status_filter = "pending"
        elif "--done" in args:
            status_filter = "done"
        elif "--progress" in args:
            status_filter = "in-progress"
        if "--high" in args:
            priority_filter = "high"
        elif "--low" in args:
            priority_filter = "low"
        elif "--medium" in args:
            priority_filter = "medium"
        list_tasks(status_filter, priority_filter)

    elif command == "done":
        if len(args) < 2:
            print("Usage: python tasks.py done <id>")
            return
        try:
            complete_task(int(args[1]))
        except ValueError:
            print("Error: ID must be a number.")

    elif command == "start":
        if len(args) < 2:
            print("Usage: python tasks.py start <id>")
            return
        try:
            start_task(int(args[1]))
        except ValueError:
            print("Error: ID must be a number.")

    elif command == "delete":
        if len(args) < 2:
            print("Usage: python tasks.py delete <id>")
            return
        try:
            delete_task(int(args[1]))
        except ValueError:
            print("Error: ID must be a number.")

    elif command == "edit":
        if len(args) < 3:
            print("Usage: python tasks.py edit <id> \"New title\"")
            return
        try:
            edit_task(int(args[1]), args[2])
        except ValueError:
            print("Error: ID must be a number.")

    elif command == "stats":
        show_stats()

    elif command == "clear-done":
        clear_done()

    else:
        print(f"Unknown command: '{command}'")
        print("Run 'python tasks.py help' to see available commands.")


if __name__ == "__main__":
    main()
