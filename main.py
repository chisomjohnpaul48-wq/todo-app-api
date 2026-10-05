from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import get_conn
from setup import init_table


init_table()

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


@app.get("/todos")
def get_todos(conn = Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM todos;
""")
        result = cur.fetchall()
    return result
    

@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate, conn = Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO todos (title, description, completed)
            VALUES (%s, %s, %s)
            RETURNING id;
""", (todo.title, todo.description, todo.completed))
        conn.commit()
        result = cur.fetchone()
    return {"message": "To do created successfully", "todo": result}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, conn = Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM todos
            WHERE id = %s;
""", (todo_id,))
        result = cur.fetchone()
        if result:
            return result
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}")
def update_todo(todo: TodoCreate, todo_id: int, conn = Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE todos
            SET title = %s, description = %s, completed = %s
            WHERE id = %s
            RETURNING id;
""", (todo.title, todo.description, todo.completed, todo_id))
        result = cur.fetchone()

        if cur.rowcount > 0:
            if result:
                conn.commit()
                return {"message": "Todo updated successfully", "todo": result}
        raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, conn = Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM todos
            WHERE id = %s
""", (todo_id,))
        
        if cur.rowcount > 0:
            conn.commit()
            return {"message": "Todo deleted successfully"}
        raise HTTPException(status_code=404, detail="Todo not found")