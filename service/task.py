import http
from sqlalchemy.exc import IntegrityError
from db.task import Task, query, query_all
from db.task import commit, delete, flush, insert


def query_task(id: str) -> dict:
    task: Task = query(id)

    if not task:
        return None

    res: dict = task.to_json()
    return res


def query_tasks() -> list:
    tasks = query_all()
    res: list = list(map(lambda task: task.to_json(), tasks))
    return res


def create_task(data: dict) -> dict:
    task = Task(name=data["name"])

    try:
        insert(task)
        flush()
        commit()
        ret: dict = task.to_json()
        return ret
    except IntegrityError:
        return {"status": http.HTTPStatus.CONFLICT, "result": "Task already existed"}


def update_task(id, data) -> dict:

    task: Task = Task.query.get(id)
    if not task:
        return {"status": http.HTTPStatus.NOT_FOUND, "result": "Task is not found"}

    if not data.get("name"):
        return {
            "status": http.HTTPStatus.BAD_REQUEST,
            "result": "The name field is empty or null",
        }

    task.name = data["name"]

    if data.get("status") == 1 or data.get("status") == 0:
        task.status = data["status"]

    elif not data.get("status"):
        pass
    else:
        return {
            "status": http.HTTPStatus.BAD_REQUEST,
            "result": f"The status: {task.status} is invalid",
        }

    flush()
    commit()

    return {"status": http.HTTPStatus.OK, "result": task.to_json()}


def remove_task(id) -> dict:
    task = Task.query.get(id)
    if not task:
        return {"status": http.HTTPStatus.NOT_FOUND, "result": "Task not found"}

    delete(task)
    commit()
    return {"status": http.HTTPStatus.OK, "result": "Task deleted successfully"}
