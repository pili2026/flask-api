import json
import http
from pytest_mock import MockerFixture

from db.task import Task


def test_delete_task_when_result_should_be_expected(client, mocker: MockerFixture):
    # Mock
    stub_value = Task(id=1, name="Test task", status=False)
    mocker.patch(target="service.task.query", return_value=stub_value)
    mocker.patch(target="service.task.delete", return_value=None)
    mocker.patch(target="service.task.commit", return_value=None)

    # Act
    response = client.delete("/task/1")
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {"status": http.HTTPStatus.OK, "result": "Task deleted successfully"}

    # Assert
    assert response == assert_value


def test_delete_task_when_task_is_not_found_then_return_error(
    client, mocker: MockerFixture
):
    # Mock
    mocker.patch(target="service.task.query", return_value=None)

    # Act
    response = client.delete("/task/1")
    response: dict = json.loads(response.data.decode("utf-8"))
    assert_value = {
        "status": http.HTTPStatus.NOT_FOUND,
        "result": "Task not found",
    }

    # Assert
    assert response == assert_value
