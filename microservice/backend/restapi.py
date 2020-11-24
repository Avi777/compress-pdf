from fastapi import FastAPI
from pydantic import BaseModel

from worker import integrate

from fastapi.middleware.cors import CORSMiddleware

# from loguru import logger
# logger.add(
#     "logs/{time:dddd MMMM YYYY}.log",
#     level="DEBUG",
#     format="{time:H:mm} | {level} | {message}",
#     rotation="1 days",
# )


app = FastAPI()
TASKS = {}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex="https://.*\.fuseclassroom\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class File(BaseModel):
    path: str


@app.get("/")
def list_tasks():
    tasks = {task_id: {"ready": task.ready()} for task_id, task in TASKS.items()}
    return tasks


@app.get('/<int:task_id>')
def get_task(task_id):
    response = {'task_id': task_id}

    task = TASKS[task_id]
    if task.ready():
        response['result'] = task.get()
    return response


@app.put("/")
async def put_task(file: File):
    in_path = file.path
    task_id = len(TASKS)
    TASKS[task_id] = integrate.delay(in_path)
    response = {"result": task_id}
    return response
