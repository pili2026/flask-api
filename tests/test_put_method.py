import json
import http
from pytest_mock import MockerFixture

from db.task import Task


def test_put_task_when_result_should_be_expected(client, mocker: MockerFixture):
    stub_value = Task(id=1, name="Test task", status=False)
    mocker.patch(target="service.task.query", return_value=stub_value)
    mocker.patch(target="service.task.insert", return_value=None)
    mocker.patch(target="service.task.flush", return_value=None)
    mocker.patch(target="service.task.commit", return_value=None)
    response = client.put("/task/1", json={"status": 1})
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.OK,
        "result": {"id": 1, "name": "Test task", "status": 1},
    }

    assert response == assert_value


def test_put_task_when_task_is_empty_then_return_error(client, mocker: MockerFixture):
    # Mock
    mocker.patch(target="service.task.query", return_value=None)

    # Act
    response = client.put("/task/1", json={"status": 1})
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.NOT_FOUND,
        "result": "Task is not found",
    }

    # Assert
    assert response == assert_value


def test_put_task_when_body_has_id_then_return_error(client, mocker: MockerFixture):
    # Mock
    stub_value = Task(id=1, name="Test task", status=False)
    mocker.patch(target="service.task.query", return_value=stub_value)

    # Act
    response = client.put("/task/1", json={"id": 1})
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.BAD_REQUEST,
        "result": "Task id can not modify",
    }

    # Assert
    assert response == assert_value


def test_put_task_when_body_is_invalid_then_return_error(client, mocker: MockerFixture):
    # Mock
    stub_value = Task(id=1, name="Test task", status=False)
    mocker.patch(target="service.task.query", return_value=stub_value)

    # Act
    response = client.put("/task/1", json={"status": 2})
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.BAD_REQUEST,
        "result": "The status is invalid",
    }

    # Assert
    assert response == assert_value
