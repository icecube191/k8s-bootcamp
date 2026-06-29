# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
import os


app = FastAPI(title="Task API", version="1.0.0")

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None


@app.on_event("startup")
async def startup():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    await pool.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
        """
    )


@app.on_event("shutdown")
async def shutdown():
    await pool.close()


class TaskIn(BaseModel):
    title: str


class Task(BaseModel):
    id: int
    title: str
    done: bool


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[Task])
async def list_tasks():
    rows = await pool.fetch(
        "SELECT id, title, done FROM tasks ORDER BY id"
    )
    return [dict(r) for r in rows]


@app.post("/api/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskIn):
    row = await pool.fetchrow(
        """
        INSERT INTO tasks (title)
        VALUES ($1)
        RETURNING id, title, done
        """,
        task.title,
    )
    return dict(row)


@app.patch("/api/tasks/{task_id}", response_model=Task)
async def complete_task(task_id: int):
    row = await pool.fetchrow(
        """
        UPDATE tasks
        SET done = TRUE
        WHERE id = $1
        RETURNING id, title, done
        """,
        task_id,
    )

    if not row:
        raise HTTPException(status_code=404, detail="Not found")

    return dict(row)