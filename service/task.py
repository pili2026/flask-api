import http
from db.model.task_model import Task, db


def query_task(id: str) -> dict:
    task: Task = Task.query.get(id)

    if not task:
        return None

    res: dict = task.to_json()
    return res


def query_tasks() -> list:
    tasks = Task.query.all()
    res: list = list(map(lambda task: task.to_json(), tasks))
    return res


def create_task(data: dict) -> dict:
    task = Task(name=data["name"])
    db.session.add(task)
    db.session.flush()
    db.session.commit()
    ret: dict = task.to_json()
    return ret


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

    db.session.flush()
    db.session.commit()

    return {"status": http.HTTPStatus.OK, "result": task.to_json()}


def remove_task(id) -> dict:
    task = Task.query.get(id)
    if not task:
        return {"status": http.HTTPStatus.NOT_FOUND, "result": "Task not found"}

    db.session.delete(task)
    db.session.commit()
    return {"status": http.HTTPStatus.OK, "result": "Task deleted successfully"}
