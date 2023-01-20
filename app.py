import http

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, name, status=False):
        self.name = name
        self.status = status

    def to_json(self):

        return {
            "id": self.id,
            "name": self.name,
            "status": 0 if self.status is False else 1,
        }


@app.before_first_request
def create_tables():
    db.create_all()


def get_task_service(id: str) -> dict:
    task: Task = Task.query.get(id)

    if not task:
        return None

    res: dict = task.to_json()
    return res


def get_tasks_service() -> list:
    tasks = Task.query.all()
    res: list = list(map(lambda task: task.to_json(), tasks))
    return res


@app.route("/task/<int:id>", methods=["GET"])
def get_task(id):

    task: dict = get_task_service(id=id)

    response = make_response(
        jsonify({"status": http.HTTPStatus.OK, "result": task}),
        http.HTTPStatus.OK,
    )
    return response


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks: list = get_tasks_service()

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


@app.route("/task", methods=["POST"])
def post_task():
    data = request.get_json()

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

    task = Task(name=data["name"])
    db.session.add(task)
    db.session.flush()
    db.session.commit()

    response = make_response(
        jsonify(
            {
                "status": http.HTTPStatus.CREATED,
                "result": task.to_json(),
            }
        ),
        http.HTTPStatus.CREATED,
    )

    return response


@app.route("/task/<int:id>", methods=["PUT"])
def put_task(id: str):

    task: Task = Task.query.get(id)
    if not task:
        response = make_response(
            jsonify(
                {"status": http.HTTPStatus.NOT_FOUND, "result": "Task is not found"}
            ),
            http.HTTPStatus.NOT_FOUND,
        )
        return response

    data = request.get_json()

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

    task.name = data["name"]

    if not data.get("status"):
        pass
    elif isinstance(data["status"], int) and abs(data["status"]) <= 1:
        task.status = data["status"]
    else:
        response = make_response(
            jsonify(
                {
                    "status": http.HTTPStatus.BAD_REQUEST,
                    "result": f"The status: {task.status} is invalid",
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )
        return response

    db.session.flush()
    db.session.commit()

    response = make_response(
        jsonify({"status": http.HTTPStatus.OK, "result": task.to_json()}),
        http.HTTPStatus.OK,
    )
    return response


@app.route("/task/<int:id>", methods=["DELETE"])
def delete_task(id: str):
    task = Task.query.get(id)
    if not task:
        response = make_response(
            jsonify({"status": http.HTTPStatus.NOT_FOUND, "result": "Task not found"}),
            http.HTTPStatus.NOT_FOUND,
        )
        return response

    db.session.delete(task)
    db.session.commit()

    response = make_response(
        jsonify({"status": http.HTTPStatus.OK, "result": "Task deleted successfully"}),
        http.HTTPStatus.OK,
    )
    return response


if __name__ == "__main__":
    app.run(debug=True)
