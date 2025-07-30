"""Lunatask Person Timeline Note objects.

https://lunatask.app/api/person-timeline-notes-api/create
"""

import datetime
from dataclasses import dataclass, field
from uuid import UUID

from dataclass_wizard import JSONPyWizard, JSONWizard
from dataclass_wizard.enums import DateTimeTo


@dataclass
class TimelineNote(JSONPyWizard):
    """A Lunatask Person Timeline Note object.

    Is `date_on` YYYY-MM-DD only, or is a time component just ignored?

    The following fields are undocumented:

    - content: str (encrypted, base64), "Busy doing things." became 90 chars…
    - deleted_at: datetime | None
    - person_id: UUID
    """

    class _(JSONWizard.Meta):  # noqa: N801
        marshall_date_time_as = DateTimeTo.ISO_FORMAT
        skip_defaults = True

    id: UUID
    date_on: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.fromisoformat(
            "1970-01-01T00:00:00.000Z"
        )
    )
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.fromisoformat(
            "1970-01-01T00:00:00.000Z"
        )
    )
    updated_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.fromisoformat(
            "1970-01-01T00:00:00.000Z"
        )
    )
    deleted_at: datetime.datetime | None = None
    person_id: UUID | None = None
    content: str | None = None
