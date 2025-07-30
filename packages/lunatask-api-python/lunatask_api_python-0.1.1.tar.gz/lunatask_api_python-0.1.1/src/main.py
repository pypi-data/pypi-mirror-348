"""Import your tasks from Todoist to Lunatask."""

import argparse
import os
import uuid
from tomllib import TOMLDecodeError

from requests import HTTPError, RequestException
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Label as TodoistLabel
from todoist_api_python.models import Project as TodoistProject
from todoist_api_python.models import Task as TodoistTask

from config import Config
from lunatask.api import LunataskAPI
from lunatask.models.people import NewPerson, Relationship
from lunatask.models.source import Source
from lunatask.models.task import NewTask


def _convert_task(config: Config, todoist_task: TodoistTask) -> None:
    """Given a Todoist Task object, return a similar Lunatask task JSON.

    config: a Config object
    todoist_task: a Task from the Todoist API

    Example Todoist Task object:

    Task(assignee_id=None, assigner_id=None, comment_count=0,
    is_completed=False, content='Review ideas for Plot',
    created_at='2023-07-22T19:53:20.666308Z', creator_id='587049',
    description='', due=None, id='7072027828', labels=['arcana📜'], order=1,
    parent_id=None, priority=1, project_id='2327921473', section_id=None,
    url='https://app.todoist.com/app/task/7072027828', duration=None,
    sync_id=None)
    """
    raise NotImplementedError


def _live_test_tasks(config: Config, api: LunataskAPI, uuid_str: str) -> None:
    """Run a live test of the Task APIs."""
    test_task = None
    try:
        print("Creating task.")
        test_task = api.create_task(
            NewTask(
                config.todoist_default_area,
                name=uuid_str,
            ),
            source=Source("todoist2lunatask", "live test"),
        )

        try:
            print("Updating task.")
            test_task = api.update_task(test_task, "New Name", "A task note.")
        except RequestException as ex:
            print(f"Unable to update task: {ex.response}")

        try:
            print("Get task.")
            _ = api.get_task(test_task.id)
        except RequestException as ex:
            print(f"Unable to get task: {ex.response}")

        try:
            print("Get tasks.")
            _ = api.get_tasks(Source("todoist2lunatask", "live test"))
        except RequestException as ex:
            print(f"Unable to get tasks: {ex.response}")

    except RequestException as ex:
        print(f"Unable to test Task APIs: {ex.response}")
    finally:
        if test_task:
            try:
                print("Delete task.")
                _ = api.delete_task(test_task.id)
            except RequestException as ex:
                print(f"Unable to delete test task: {ex.response}")


def _list_test_person(config: Config, api: LunataskAPI, uuid_parts: list[str]) -> None:
    """Run a live test of the People APIs."""
    test_person = None
    try:
        print("Creating person.")
        test_person = api.create_person(
            NewPerson(
                uuid_parts[0],
                uuid_parts[-1],
                Relationship.ALMOST_STRANGERS,
                "todoist2lunatask",
                "live test",
            )
        )

        try:
            print("Get person.")
            _ = api.get_person(test_person.id)
        except RequestException as ex:
            print(f"Get person failed: {ex.response}")

        try:
            print("Get people.")
            _ = api.get_people(Source("todoist2lunatask", "live test"))
        except RequestException as ex:
            print(f"Get people failed: {ex.response}")

        try:
            print("Create person timeline note.")
            _ = api.create_timeline_note(test_person.id, content="Hello, world.")
        except RequestException as ex:
            print(f"Couldn't add a person timeline note: {ex.response}")

    except RequestException as ex:
        print(f"Unable to test People APIs: {ex.response}")
    finally:
        if test_person:
            try:
                print("Deleting person.")
                _ = api.delete_person(test_person.id)
            except RequestException as ex:
                print(f"Unable to delete test person: {ex.response}")


def _live_test(config: Config, api: LunataskAPI) -> None:
    """Run a live test.

    This exercises the Lunatask API by creating Tasks, Notes, People and Person
    Timeline Notes, updating the Tasks, attempting to track a Habit, and
    deleting the Tasks and People. This is done in the todoist_default_area
    specified in your config file.
    """
    # Check authentication.
    try:
        print("Attempting authentication.")
        _ = api.ping()
    except HTTPError as ex:
        print("\tFailed to authenticate.")
        raise SystemExit from ex

    uuid_str = str(uuid.uuid1())
    uuid_parts = uuid_str.split("-")

    # Task APIs
    _live_test_tasks(config, api, uuid_str)

    # People APIs
    #
    # - people API
    # - person timeline note
    _list_test_person(config, api, uuid_parts)

    # TODO: Things we can't currently test; these need an existing target habit
    # or notebook, and there's currently no API for creating those.
    #
    # needs existing habit
    # - habit tracking
    #
    # needs existing notebook
    # - note creation


def _markdown_for_task(config: Config, task: TodoistTask) -> str:
    """Convert a given Todoist Task into Markdown."""
    raise NotImplementedError


def _show_projects(projects: list[TodoistProject]) -> None:
    """Pretty-print Todoist Projects."""
    print("Projects:")
    for project in projects:
        print(f"\t'{project.name}' = {project}'")


def _show_labels(labels: list[TodoistLabel]) -> None:
    """Pretty-print Todoist Labels."""
    print("Labels:")
    for label in labels:
        print(f"\t'{label.name}' = {label}")


def main() -> int:
    """Import your tasks from Todoist to Lunatask.

    `todoist2lunatask --help` for details, and read the
    [`todoist2lunatask.config`](https://codeberg.org/Taffer/todoist2lunatask/src/branch/main/todoist2lunatask.config.template)
    template.
    """
    parser = argparse.ArgumentParser(
        prog="todoist2lunatask",
        description="Import tasks/projects/labels from Todoist into Lunatask",
        epilog="You must create a todoist2lunatask.config file by copying "
        "todoist2lunatask.config.template and editing it. Please read the "
        "README.md for details.",
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store",
        default="todoist2lunatask.config",
        help="Specify the configuration file.",
    )
    parser.add_argument(
        "--show-labels",
        action="store_true",
        help="List your Todoist Labels and exit.",
    )
    parser.add_argument(
        "--show-projects",
        action="store_true",
        help="List your Todoist Projects and exit.",
    )
    parser.add_argument(
        "--live-test",
        action="store_true",
        help="Run a live test; this exercises the Lunatask API by creating "
        "Tasks, Notes, People and Person Timeline Notes, updating the Tasks, "
        "attempting to track a Habit, and deleting the Tasks and People. "
        "This is done in the todoist_default_area specified in your config "
        "file.",
    )
    args = parser.parse_args()

    # Load configuration
    config = None
    try:
        tmp = Config.from_toml_file(args.config)
        config = tmp[0] if isinstance(tmp, list) else tmp
    except TOMLDecodeError as ex:
        print(f"Invalid config file {args.config}: {ex}")
        return os.EX_OSFILE

    # TODO: Error handling
    lunatask_api = LunataskAPI(config.lunatask_api_token)
    if args.live_test:
        _live_test(config, lunatask_api)
        return os.EX_OK

    todoist_api = TodoistAPI(config.todoist_api_token)
    projects = todoist_api.get_projects()
    if args.show_projects:
        _show_projects(projects)
        return os.EX_OK

    labels = todoist_api.get_labels()
    if args.show_labels:
        _show_labels(labels)
        return os.EX_OK

    label_map = {}
    for label in labels:
        label_map[label.id] = label.name

    # Map Todoist Projects to Lunatask Areas of Life. If a Project doesn't
    # have a mapping in todoist2lunatask.config, it's mapped into the
    # todoist_default_area, and we'll warn the users about that.
    #
    # If the todoist_default_area doesn't exist (or any of the mapped Areas),
    # we'll error out trying to create the Lunatask Task.
    project_map = {}  # Lookups done via project.id found in the task object.
    missing_projects = []
    for project in projects:
        if project.name in config.todoist_project_map:
            project_map[project.id] = config.todoist_project_map[project.name]
        else:
            project_map[project.id] = config.todoist_default_area
            missing_projects.append(project.name)

    print(
        f"Found {len(projects)} Todoist projects, mapping to "
        f"{len(config.todoist_project_map)} Lunatask Areas."
    )
    print(f"{config.todoist_project_map}")

    if missing_projects:
        print(
            f"WARNING: {len(missing_projects)} projects not found in todoist_project_map:"  # noqa: E501
        )
        print(f"\t{', '.join(missing_projects)}")

    return os.EX_OK

    todoist_tasks = todoist_api.get_tasks()
    print(f"Found {len(todoist_tasks)} tasks in Todoist:")
    for task in todoist_tasks:
        print(f"\t{task}")

    # Transform the Todoist Task into a Lunatask Task; see the README.md for
    # some details, they don't support the same set of features.
    #
    # Additional data from Todoist Tasks is preserved in the Lunatask Task
    # notes.
    #
    # Todoist Labels map to Lunatask Goals, but there's currently no API to
    # create Goals. Instead, we create a task reminding the user to recreate
    # those and add them to the appropriate tasks.
    #
    # There's also no way to mark a task as recurring. Again, we'll create a
    # task reminding the user to set those up.

    # - create tasks in Lunatask
    # - create a task to create/apply Goals=Labels in each Area as necessary
    # - create a task to update recurring tasks as necessary
    # TODO: can we link to other tasks for those?
    # TODO: do we need to make subtasks as full tasks before we create the
    # parent? or just collect them and stash them in the notes?

    tasks = lunatask_api.get_tasks()
    print(f"Got {len(tasks.tasks)} tasks!")
    for task in tasks.tasks:
        print(f"\t{task.id}, {task.sources}")
    task = lunatask_api.get_task("8bc0a03f-6cec-4ee5-a7a5-e8c7c0a695cf")
    print(f"\t{task}")

    return os.EX_OK


if __name__ == "__main__":
    main()
