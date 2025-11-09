import tkinter as tk
from tkinter import messagebox, font
from datetime import datetime

filename = "tasks.txt"
tasks = []

def save_tasks():
    with open(filename, 'w',encoding="utf-8") as file:
        for task in tasks:
            file.write(f"{task}\n")
    print("Saved:", tasks)

def load_tasks():
    try:
        with open(filename, 'r',encoding="utf-8") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return []

tasks = load_tasks()
print("Loaded:", tasks)

tasks.append("✔️ Test Task")
save_tasks()

# Add new task
def add_task():
    task_text = entry.get().strip()
    if task_text:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        task = f"☐ {task_text}  (Added: {timestamp})"
        tasks.append(task)
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Delete selected task
def delete_task():
    try:
        index = listbox.curselection()[0]
        listbox.delete(index)
        tasks.pop(index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Edit selected task
def edit_task():
    try:
        index = listbox.curselection()[0]
        new_text = entry.get().strip()
        if new_text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            tasks[index] = f"☐ {new_text}  (Edited: {timestamp})"
            listbox.delete(index)
            listbox.insert(index, tasks[index])
            save_tasks()
            entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Enter new task text to edit.")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")

# Search task by keyword
def search_task():
    keyword = entry.get().lower()
    listbox.selection_clear(0, tk.END)
    for i, task in enumerate(tasks):
        if keyword in task.lower():
            listbox.selection_set(i)
            listbox.activate(i)
            return
    messagebox.showinfo("Search", "No matching task found.")

# Toggle completion status
def toggle_complete():
    try:
        index = listbox.curselection()[0]
        task = tasks[index]
        if task.startswith("☐"):
            task = "✔️" + task[1:]
        elif task.startswith("✔️"):
            task = "☐" + task[2:]
        tasks[index] = task
        listbox.delete(index)
        listbox.insert(index, task)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to toggle.")

# Clear all tasks
def clear_all_tasks():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
        listbox.delete(0, tk.END)
        tasks.clear()
        save_tasks()

# GUI setup
root = tk.Tk()
root.title("Enhanced To-Do List App")
root.geometry("500x500")
root.configure(bg="#e9f5f9")

hf = font.Font(family="Helvetica", size=16, weight="bold")
title_label = tk.Label(root, text="To-Do List 📝", font=hf, bg="#e9f5f9")
title_label.pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5)

# Button frame
btn_frame = tk.Frame(root, bg="#e9f5f9")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add", width=12, command=add_task).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit", width=12, command=edit_task).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", width=12, command=delete_task).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Complete", width=12, command=toggle_complete).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Search", width=12, command=search_task).grid(row=1, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Clear All", width=12, command=clear_all_tasks).grid(row=1, column=2, padx=5, pady=5)

listbox = tk.Listbox(root, width=60, height=15, font=("Arial", 12))
listbox.pack(pady=10)

# Load existing tasks
tasks = load_tasks()
for task in tasks:
    listbox.insert(tk.END, task)

root.mainloop()
