"""Lunatask Note objects.

https://lunatask.app/api/notes-api/entity
"""

import datetime
from dataclasses import dataclass
from uuid import UUID

from dataclass_wizard import DumpMixin, JSONPyWizard, JSONWizard, LoadMixin
from dataclass_wizard.enums import DateTimeTo

from lunatask.models.source import Source


@dataclass
class Note(JSONPyWizard, LoadMixin, DumpMixin):
    """A Lunatask Note.

    This field is undocumented:

    - pinned: bool
    """

    class _(JSONWizard.Meta):  # noqa: N801
        marshall_date_time_as = DateTimeTo.ISO_FORMAT
        skip_defaults = True

    id: UUID
    notebook_id: UUID
    sources: list[Source]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    pinned: bool = False
    date_on: datetime.datetime | None = None
    deleted_at: datetime.datetime | None = None
