import json
import http
from pytest_mock import MockerFixture
from db.task import Task


def test_get_all_task_when_result_should_be_expected(client, mocker: MockerFixture):
    # Mock
    stub_value = [Task(id=1, name="Test task", status=False)]
    mocker.patch(target="service.task.query_all", return_value=stub_value)

    # Act
    response = client.get("/tasks")
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.OK,
        "result": [
            {"id": 1, "name": "Test task", "status": 0},
        ],
    }

    # Assert
    assert response == assert_value


def test_get_all_task_when_return_is_empty_then_result_should_be_expected(
    client, mocker: MockerFixture
):
    # Mock
    mocker.patch(target="service.task.query_all", return_value=[])

    # Act
    response = client.get("/tasks")
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.OK,
        "result": [],
    }

    # Assert
    assert response == assert_value


def test_get_task_when_result_should_be_expected(client, mocker: MockerFixture):
    # Mock
    stub_value = Task(id=1, name="Test task", status=False)
    mocker.patch(target="service.task.query", return_value=stub_value)

    # Act
    response = client.get("/task/1")
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.OK,
        "result": {"id": 1, "name": "Test task", "status": 0},
    }

    # Assert
    assert response == assert_value


def test_get_task_when_return_is_empty_then_result_should_be_expected(
    client, mocker: MockerFixture
):
    # Mock
    mocker.patch(target="service.task.query", return_value=None)

    # Act
    response = client.get("/task/1")
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.OK,
        "result": None,
    }

    # Assert
    assert response == assert_value
