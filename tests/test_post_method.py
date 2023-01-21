import json
import http
from pytest_mock import MockerFixture


def test_post_task_when_result_should_be_expected(client, mocker: MockerFixture):
    # Mock
    mocker.patch(target="service.task.insert", return_value=None)
    mocker.patch(target="service.task.flush", return_value=None)
    mocker.patch(target="service.task.commit", return_value=None)

    # Act
    response = client.post("/task", json={"name": "Test task"})
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.CREATED,
        "result": {"id": None, "name": "Test task", "status": 0},
    }

    # Assert
    assert response == assert_value


def test_post_task_when_body_is_invalid_then_return_error(client):
    # Act
    response = client.post("/task", json={"name": "Test task", "status": 0})
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.BAD_REQUEST,
        "result": "The input field is invalid, the add task only accept name field",
    }

    # Assert
    assert response == assert_value


def test_post_task_when_name_is_empty_then_return_error(client):
    # Mock
    response = client.post("/task", json={"name": None})
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.BAD_REQUEST,
        "result": "The name field is empty or null",
    }

    # Assert
    assert response == assert_value


def test_post_task_when_not_name_field_then_return_error(client):
    # Act
    response = client.post("/task", json={})
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.BAD_REQUEST,
        "result": "The name field is empty or null",
    }

    # Assert
    assert response == assert_value
