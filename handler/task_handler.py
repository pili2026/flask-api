import http

from flask import Blueprint, jsonify, make_response, request
from db.model.task_model import Task, db
from service.task import create_task, query_task, query_tasks, remove_task, update_task

task = Blueprint(
    "task",
    __name__,
)


@task.route("/task/<int:id>", methods=["GET"])
def get_task(id):

    task: dict = query_task(id=id)

    response = make_response(
        jsonify({"status": http.HTTPStatus.OK, "result": task}),
        http.HTTPStatus.OK,
    )
    return response


@task.route("/tasks", methods=["GET"])
def get_tasks():
    tasks: list = query_tasks()

    response = make_response(
        jsonify(
            {
                "status": http.HTTPStatus.OK,
                "result": tasks,
            }
        ),
        http.HTTPStatus.OK,
    )
    return response


@task.route("/task", methods=["POST"])
def post_task():
    data: dict = request.get_json()

    if len(data) > 1:
        response = make_response(
            jsonify(
                {
                    "status": http.HTTPStatus.BAD_REQUEST,
                    "result": "The input field is invalid, the add task only accept name field",
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
        return response

    if not data.get("name"):
        response = make_response(
            jsonify(
                {
                    "status": http.HTTPStatus.BAD_REQUEST,
                    "result": "The name field is empty or null",
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
        return response

    created_task: dict = create_task(data=data)

    response = make_response(
        jsonify(
            {
                "status": http.HTTPStatus.CREATED,
                "result": created_task,
            }
        ),
        http.HTTPStatus.CREATED,
    )

    return response


@task.route("/task/<int:id>", methods=["PUT"])
def put_task(id: str):

    data = request.get_json()
    updated_task: dict = update_task(id, data)

    response = make_response(
        jsonify(updated_task),
        http.HTTPStatus.OK,
    )
    return response


@task.route("/task/<int:id>", methods=["DELETE"])
def delete_task(id: str):

    deleted_task: dict = remove_task(id)

    response = make_response(
        jsonify(deleted_task),
        http.HTTPStatus.OK,
    )
    return response
