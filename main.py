from fastapi import FastAPI, HTTPException, Depends
from psycopg.rows import dict_row
from schemas import TodoCreate, TodoResponse, TodoUpdate
from database import get_conn
from setup import init_table


init_table()

app = FastAPI()


@app.get("/todos", response_model=list[TodoResponse], status_code=200)
def get_todos(conn = Depends(get_conn)):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            SELECT * FROM todos;
""")
        result = cur.fetchall()
    return result
    

@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate, conn = Depends(get_conn)):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            INSERT INTO todos (title, description, completed)
            VALUES (%s, %s, %s)
            RETURNING id, title, description, completed;
""", (todo.title, todo.description, todo.completed))
        conn.commit()
        result = cur.fetchone()
    return result

@app.get("/todos/{todo_id}", response_model=TodoResponse, status_code=200)
def get_todo(todo_id: int, conn = Depends(get_conn)):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            SELECT * FROM todos
            WHERE id = %s;
""", (todo_id,))
        result = cur.fetchone()
        if result:
            return result
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=TodoResponse, status_code=200)
def update_todo(todo: TodoUpdate, todo_id: int, conn = Depends(get_conn)):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            UPDATE todos
            SET title = %s, description = %s, completed = %s
            WHERE id = %s
            RETURNING id, title, description, completed;
""", (todo.title, todo.description, todo.completed, todo_id))
        result = cur.fetchone()

        if cur.rowcount > 0:
            if result:
                conn.commit()
                return result
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