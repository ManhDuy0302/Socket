from .database import Database

class TodoModel:
    def __init__(self):
        self.db = Database()

    def create_todo(self, title, description):
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO todos (title, description) VALUES (?, ?)",
                (title, description)
            )
            return cursor.lastrowid

    def get_all_todos(self):
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM todos")
            return [dict(row) for row in cursor.fetchall()]

    def get_todo(self, todo_id):
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_todo(self, todo_id, title, description, completed):
        with self.db.get_connection() as conn:
            conn.execute(
                "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
                (title, description, completed, todo_id)
            )
            return self.get_todo(todo_id)

    def delete_todo(self, todo_id):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))