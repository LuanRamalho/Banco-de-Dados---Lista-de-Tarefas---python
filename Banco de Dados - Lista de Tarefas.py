import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Configura o arquivo para armazenamento local das tarefas
DATA_FILE = "tasks.json"

# Carrega as tarefas do arquivo JSON
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Salva as tarefas no arquivo JSON
def save_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Classe da aplicação
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tarefas")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0f7fa")

        self.tasks = load_tasks()

        # Título
        title = tk.Label(root, text="Lista de Tarefas", font=("Arial", 24, "bold"), bg="#e0f7fa", fg="#00796b")
        title.pack(pady=10)

        # Entrada e botão de adicionar tarefa
        self.name_input = tk.Entry(root, font=("Arial", 14))
        self.name_input.pack(pady=5)
        add_btn = tk.Button(root, text="Adicionar Tarefa", font=("Arial", 12), bg="darkgreen", fg="white", command=self.add_task)
        add_btn.pack(pady=5)

        # Área de busca
        self.search_input = tk.Entry(root, font=("Arial", 14))
        self.search_input.pack(pady=10)
        self.search_input.bind("<KeyRelease>", self.search_tasks)

        # Botões de ordenação
        sort_frame = tk.Frame(root, bg="#e0f7fa")
        sort_frame.pack(pady=10)
        tk.Button(sort_frame, text="Ordem Crescente por ID", font=("Arial", 10), command=self.sort_by_id_asc, bg="darkgoldenrod", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(sort_frame, text="Ordem Decrescente por ID", font=("Arial", 10), command=self.sort_by_id_desc, bg="darkgoldenrod", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(sort_frame, text="Ordem Crescente por Nome", font=("Arial", 10), command=self.sort_by_name_asc, bg="darkgoldenrod", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(sort_frame, text="Ordem Decrescente por Nome", font=("Arial", 10), command=self.sort_by_name_desc, bg="darkgoldenrod", fg="white").pack(side=tk.LEFT, padx=5)

        # Tabela de tarefas
        self.tree = ttk.Treeview(root, columns=("ID", "Tarefa", "Ações"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tarefa", text="Tarefa")
        self.tree.heading("Ações", text="Ações")
        self.tree.column("ID", width=50)
        self.tree.column("Tarefa", width=400)
        self.tree.column("Ações", width=200)
        self.tree.pack(pady=10)

        # Adiciona botões à tabela
        self.tree.bind("<Double-1>", self.on_tree_select)
        self.update_tree(self.tasks)

    def add_task(self):
        name = self.name_input.get().strip()
        if name:
            task_id = self.tasks[-1]["id"] + 1 if self.tasks else 1
            self.tasks.append({"id": task_id, "name": name, "note": ""})
            save_tasks(self.tasks)
            self.update_tree(self.tasks)
            self.name_input.delete(0, tk.END)

    def update_tree(self, tasks):
        self.tree.delete(*self.tree.get_children())
        for task in tasks:
            self.tree.insert("", "end", values=(task["id"], task["name"], "Editar | Nota | Excluir"))

    def search_tasks(self, event=None):
        query = self.search_input.get().strip().lower()
        filtered_tasks = [task for task in self.tasks if query in task["name"].lower()]
        self.update_tree(filtered_tasks)

    def sort_by_id_asc(self):
        self.tasks.sort(key=lambda x: x["id"])
        self.update_tree(self.tasks)

    def sort_by_id_desc(self):
        self.tasks.sort(key=lambda x: x["id"], reverse=True)
        self.update_tree(self.tasks)

    def sort_by_name_asc(self):
        self.tasks.sort(key=lambda x: x["name"].lower())
        self.update_tree(self.tasks)

    def sort_by_name_desc(self):
        self.tasks.sort(key=lambda x: x["name"].lower(), reverse=True)
        self.update_tree(self.tasks)

    def on_tree_select(self, event):
        item = self.tree.selection()[0]
        task_id = self.tree.item(item, "values")[0]
        task = next(task for task in self.tasks if str(task["id"]) == task_id)
        self.open_task_editor(task)

    def open_task_editor(self, task):
        editor = tk.Toplevel(self.root)
        editor.title("Editar Tarefa")
        editor.geometry("400x300")

        tk.Label(editor, text="Editar Tarefa", font=("Arial", 18)).pack(pady=10)
        name_entry = tk.Entry(editor, font=("Arial", 14))
        name_entry.insert(0, task["name"])
        name_entry.pack(pady=5)

        tk.Label(editor, text="Nota:", font=("Arial", 14)).pack(pady=5)
        note_text = tk.Text(editor, height=5, font=("Arial", 12))
        note_text.insert("1.0", task["note"])
        note_text.pack(pady=5)

        def save_changes():
            task["name"] = name_entry.get().strip()
            task["note"] = note_text.get("1.0", tk.END).strip()
            save_tasks(self.tasks)
            self.update_tree(self.tasks)
            editor.destroy()

        def delete_task():
            self.tasks = [t for t in self.tasks if t["id"] != task["id"]]
            save_tasks(self.tasks)
            self.update_tree(self.tasks)
            editor.destroy()

        tk.Button(editor, text="Salvar", command=save_changes, bg="#28a745", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(editor, text="Excluir", command=delete_task, bg="#dc3545", fg="white", font=("Arial", 12)).pack(side=tk.RIGHT, padx=10, pady=10)

# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
