"""Lunatask Task objects."""

import datetime
from dataclasses import dataclass
from enum import Enum, StrEnum, unique
from uuid import UUID

from dataclass_wizard import JSONPyWizard, JSONWizard
from dataclass_wizard.enums import DateTimeTo

from lunatask.models.source import Source


# Task enums - https://lunatask.app/api/tasks-api/entity
@unique
class Status(StrEnum):
    """Task status values."""

    COMPLETED = "completed"
    LATER = "later"
    NEXT = "next"
    STARTED = "started"
    WAITING = "waiting"


@unique
class Priority(Enum):
    """Task priority values."""

    HIGHEST = 2
    HIGH = 1
    NORMAL = 0  # Default
    LOW = -1
    LOWEST = -2


@unique
class Motivation(StrEnum):
    """Task motivation values."""

    MUST = "must"
    SHOULD = "should"
    UNKNOWN = "unknown"  # Default
    WANT = "want"


@unique
class Eisenhower(Enum):
    """Task Eisenhower values."""

    URGENT_IMPORTANT = 1
    URGENT_NOT_IMPORTANT = 2
    NOT_URGENT_IMPORTANT = 3
    NOT_URGENT_NOT_IMPORTANT = 4
    UNCATEGORIZED = 0


@dataclass
class NewTask(JSONPyWizard):
    """A new Task, about to be added to Lunatask.

    Optional fields are marked *(Optional)*, the others are required.

    `area_id` - Get this in the app from the Area of Life settings; click the
                Copy Area ID button. Looks like
                "49d7c7ad-332d-50ef-a2b6-a3b972fa880c".
    `goal_id` - Get this in the app from the Goal's "Edit goal" settings; click
                the Copy Goal ID button. Looks like
                "49d7c7ad-332d-50ef-a2b6-a3b972fa880c". *(Optional)*
    `name` - Task name, no Markdown support. Technically *(Optional)*, but a
             really good idea.
    `note` - Task note(s), with Markdown support. *(Optional)*
    `status` - Task status. Defaults to Status.LATER.
    `motivation` - Task motivation. Defaults to Motivation.UNKNOWN.
    `estimate` - Estimated amount of time, in minutes, to finish this task.
                 *(Optional)*
    `priority` - Task priority. Defaults to Priority.NORMAL.
    `scheduled_on` - ISO 8601 formatted date/time for when this task was
                     created. Defaults to now, but *(Optional)* if you set it
                     to None.
    `completed_at` - ISO 8601 formatted date/time for when this task was
                     completed. *(Optional)*
    `source` - The source of this task; not currently visible in the UI, can
               be used to filter `get_tasks()`. Tools like todoist2lunatask
               use this to indicate what created the task. *(Optional)*

    A TaskEntity can have multiple `source`: `source_id` pairs; do you
    use `update_task()` repeatedly to do this?
    """

    class _(JSONWizard.Meta):  # noqa: N801
        marshall_date_time_as = DateTimeTo.ISO_FORMAT
        skip_defaults = True

    area_id: UUID
    goal_id: UUID | None = None
    name: str | None = None  # Name of the task, no Markdown support.
    note: str | None = None  # Task notes; Markdown supported.
    status: Status = Status.LATER
    motivation: Motivation = Motivation.UNKNOWN
    eisenhower: Eisenhower = Eisenhower.UNCATEGORIZED
    estimate: int | None = None  # Estimate in minutes
    priority: Priority | None = None
    scheduled_on: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    source: str | None = None
    source_id: str | None = None


@dataclass
class Task(JSONPyWizard):
    """A Lunatask task.

    https://lunatask.app/api/tasks-api/entity

    Task data available to the API is entirely metadata; the task name and
    notes (for example) are encrypted and only visible in the Lunatask app.

    Could we get the encrypted data via future API calls and decrypt
    them ourselves?

    These fields are undocumented:

    - deleted_at: datetime | None
    """

    class _(JSONWizard.Meta):  # noqa: N801
        marshall_date_time_as = DateTimeTo.ISO_FORMAT
        skip_defaults = True

    id: UUID
    area_id: UUID
    status: Status
    motivation: Motivation
    eisenhower: Eisenhower
    sources: list[Source]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    goal_id: UUID | None = None
    previous_status: Status | None = None
    estimate: int | None = None
    priority: Priority | None = None
    progress: float | None = None
    scheduled_on: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None
