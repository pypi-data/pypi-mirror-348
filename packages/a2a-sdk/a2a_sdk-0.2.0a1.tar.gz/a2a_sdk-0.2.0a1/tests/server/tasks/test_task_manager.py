from typing import Any
from unittest.mock import AsyncMock

import pytest

from a2a.server.tasks import TaskManager
from a2a.types import (
    Artifact,
    Message,
    Part,
    Role,
    Task,
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TextPart,
)


MINIMAL_TASK: dict[str, Any] = {
    'id': 'task-abc',
    'contextId': 'session-xyz',
    'status': {'state': 'submitted'},
    'type': 'task',
}


@pytest.fixture
def mock_task_store() -> AsyncMock:
    """Fixture for a mock TaskStore."""
    return AsyncMock()


@pytest.fixture
def task_manager(mock_task_store: AsyncMock) -> TaskManager:
    """Fixture for a TaskManager with a mock TaskStore."""
    return TaskManager(
        task_id=MINIMAL_TASK['id'],
        context_id=MINIMAL_TASK['contextId'],
        task_store=mock_task_store,
        initial_message=None,
    )


@pytest.mark.asyncio
async def test_get_task_existing(
    task_manager: TaskManager, mock_task_store: AsyncMock
) -> None:
    """Test getting an existing task."""
    expected_task = Task(**MINIMAL_TASK)
    mock_task_store.get.return_value = expected_task
    retrieved_task = await task_manager.get_task()
    assert retrieved_task == expected_task
    mock_task_store.get.assert_called_once_with(MINIMAL_TASK['id'])


@pytest.mark.asyncio
async def test_get_task_nonexistent(
    task_manager: TaskManager, mock_task_store: AsyncMock
) -> None:
    """Test getting a nonexistent task."""
    mock_task_store.get.return_value = None
    retrieved_task = await task_manager.get_task()
    assert retrieved_task is None
    mock_task_store.get.assert_called_once_with(MINIMAL_TASK['id'])


@pytest.mark.asyncio
async def test_save_task_event_new_task(
    task_manager: TaskManager, mock_task_store: AsyncMock
) -> None:
    """Test saving a new task."""
    task = Task(**MINIMAL_TASK)
    await task_manager.save_task_event(task)
    mock_task_store.save.assert_called_once_with(task)


@pytest.mark.asyncio
async def test_save_task_event_status_update(
    task_manager: TaskManager, mock_task_store: AsyncMock
) -> None:
    """Test saving a status update for an existing task."""
    initial_task = Task(**MINIMAL_TASK)
    mock_task_store.get.return_value = initial_task
    new_status = TaskStatus(
        state=TaskState.working,
        message=Message(
            role=Role.agent,
            parts=[Part(TextPart(text='content'))],
            messageId='message-id',
        ),
    )
    event = TaskStatusUpdateEvent(
        taskId=MINIMAL_TASK['id'],
        contextId=MINIMAL_TASK['contextId'],
        status=new_status,
        final=False,
    )
    await task_manager.save_task_event(event)
    updated_task = initial_task
    updated_task.status = new_status
    mock_task_store.save.assert_called_once_with(updated_task)


@pytest.mark.asyncio
async def test_save_task_event_artifact_update(
    task_manager: TaskManager, mock_task_store: AsyncMock
) -> None:
    """Test saving an artifact update for an existing task."""
    initial_task = Task(**MINIMAL_TASK)
    mock_task_store.get.return_value = initial_task
    new_artifact = Artifact(
        artifactId='artifact-id',
        name='artifact1',
        parts=[Part(TextPart(text='content'))],
    )
    event = TaskArtifactUpdateEvent(
        taskId=MINIMAL_TASK['id'],
        contextId=MINIMAL_TASK['contextId'],
        artifact=new_artifact,
    )
    await task_manager.save_task_event(event)
    updated_task = initial_task
    updated_task.artifacts = [new_artifact]
    mock_task_store.save.assert_called_once_with(updated_task)


@pytest.mark.asyncio
async def test_ensure_task_existing(
    task_manager: TaskManager, mock_task_store: AsyncMock
) -> None:
    """Test ensuring an existing task."""
    expected_task = Task(**MINIMAL_TASK)
    mock_task_store.get.return_value = expected_task
    event = TaskStatusUpdateEvent(
        taskId=MINIMAL_TASK['id'],
        contextId=MINIMAL_TASK['contextId'],
        status=TaskStatus(state=TaskState.working),
        final=False,
    )
    retrieved_task = await task_manager.ensure_task(event)
    assert retrieved_task == expected_task
    mock_task_store.get.assert_called_once_with(MINIMAL_TASK['id'])


@pytest.mark.asyncio
async def test_ensure_task_nonexistent(
    mock_task_store: AsyncMock,
) -> None:
    """Test ensuring a nonexistent task (creates a new one)."""
    mock_task_store.get.return_value = None
    task_manager_without_id = TaskManager(
        task_id=None,
        context_id=None,
        task_store=mock_task_store,
        initial_message=None,
    )
    event = TaskStatusUpdateEvent(
        taskId='new-task',
        contextId='some-context',
        status=TaskStatus(state=TaskState.submitted),
        final=False,
    )
    new_task = await task_manager_without_id.ensure_task(event)
    assert new_task.id == 'new-task'
    assert new_task.contextId == 'some-context'
    assert new_task.status.state == TaskState.submitted
    mock_task_store.save.assert_called_once_with(new_task)
    assert task_manager_without_id.task_id == 'new-task'
    assert task_manager_without_id.context_id == 'some-context'


def test_init_task_obj(task_manager: TaskManager) -> None:
    """Test initializing a new task object."""
    new_task = task_manager._init_task_obj('new-task', 'new-context')  # type: ignore
    assert new_task.id == 'new-task'
    assert new_task.contextId == 'new-context'
    assert new_task.status.state == TaskState.submitted
    assert new_task.history == []


@pytest.mark.asyncio
async def test_save_task(
    task_manager: TaskManager, mock_task_store: AsyncMock
) -> None:
    """Test saving a task."""
    task = Task(**MINIMAL_TASK)
    await task_manager._save_task(task)  # type: ignore
    mock_task_store.save.assert_called_once_with(task)


@pytest.mark.asyncio
async def test_save_task_event_new_task_no_task_id(
    mock_task_store: AsyncMock,
) -> None:
    """Test saving a task event without task id in TaskManager."""
    task_manager_without_id = TaskManager(
        task_id=None,
        context_id=None,
        task_store=mock_task_store,
        initial_message=None,
    )
    task_data: dict[str, Any] = {
        'id': 'new-task-id',
        'contextId': 'some-context',
        'status': {'state': 'working'},
        'type': 'task',
    }
    task = Task(**task_data)
    await task_manager_without_id.save_task_event(task)
    mock_task_store.save.assert_called_once_with(task)
    assert task_manager_without_id.task_id == 'new-task-id'
    assert task_manager_without_id.context_id == 'some-context'
    # initial submit should be updated to working
    assert task.status.state == TaskState.working


@pytest.mark.asyncio
async def test_get_task_no_task_id(
    mock_task_store: AsyncMock,
) -> None:
    """Test getting a task when task_id is not set in TaskManager."""
    task_manager_without_id = TaskManager(
        task_id=None,
        context_id='some-context',
        task_store=mock_task_store,
        initial_message=None,
    )
    retrieved_task = await task_manager_without_id.get_task()
    assert retrieved_task is None
    mock_task_store.get.assert_not_called()


@pytest.mark.asyncio
async def test_save_task_event_no_task_existing(
    mock_task_store: AsyncMock,
) -> None:
    """Test saving an event when no task exists and task_id is not set."""
    task_manager_without_id = TaskManager(
        task_id=None,
        context_id=None,
        task_store=mock_task_store,
        initial_message=None,
    )
    mock_task_store.get.return_value = None
    event = TaskStatusUpdateEvent(
        taskId='event-task-id',
        contextId='some-context',
        status=TaskStatus(state=TaskState.completed),
        final=True,
    )
    await task_manager_without_id.save_task_event(event)
    # Check if a new task was created and saved
    call_args = mock_task_store.save.call_args
    assert call_args is not None
    saved_task = call_args[0][0]
    assert saved_task.id == 'event-task-id'
    assert saved_task.contextId == 'some-context'
    assert saved_task.status.state == TaskState.completed
    assert task_manager_without_id.task_id == 'event-task-id'
    assert task_manager_without_id.context_id == 'some-context'
