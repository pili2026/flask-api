from flask import Flask

from db.task import create_table, db
from handler.task_handler import task


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(task, url_prefix="")


app = create_app()


def setup_database(app):
    with app.app_context():
        create_table()


if __name__ == "__main__":
    setup_database(app)
    app.run(host="192.168.56.102", port=5000)
