from pawpal_system import Pet, Scheduler, Task


def test_task_completion_changes_status() -> None:
    pet = Pet(name="Mochi", species="dog", age=4)
    task = Task(
        id=1,
        title="Morning walk",
        category="walking",
        duration_minutes=30,
        priority="high",
        is_required=True,
        applies_to=pet,
    )

    task.mark_complete()

    assert task.status == "completed"


def test_adding_task_to_pet_increases_task_count() -> None:
    pet = Pet(name="Luna", species="cat", age=2)
    task = Task(
        id=2,
        title="Feeding",
        category="feeding",
        duration_minutes=10,
        priority="high",
        is_required=True,
        applies_to=pet,
    )

    initial_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_sort_by_time_orders_tasks_shortest_first() -> None:
    pet = Pet(name="Mochi", species="dog", age=4)
    task_long = Task(
        id=1,
        title="Long walk",
        category="walking",
        duration_minutes=40,
        priority="medium",
        is_required=False,
        applies_to=pet,
    )
    task_short = Task(
        id=2,
        title="Quick feeding",
        category="feeding",
        duration_minutes=10,
        priority="high",
        is_required=True,
        applies_to=pet,
    )

    scheduler = Scheduler(available_minutes=60)
    sorted_tasks = scheduler.sort_by_time([task_long, task_short])

    assert [task.id for task in sorted_tasks] == [2, 1]


def test_filter_tasks_by_completion_status() -> None:
    pet = Pet(name="Mochi", species="dog", age=4)
    completed_task = Task(
        id=1,
        title="Feeding",
        category="feeding",
        duration_minutes=10,
        priority="high",
        is_required=True,
        applies_to=pet,
        status="completed",
    )
    pending_task = Task(
        id=2,
        title="Walk",
        category="walking",
        duration_minutes=20,
        priority="medium",
        is_required=False,
        applies_to=pet,
    )

    scheduler = Scheduler(available_minutes=60)
    filtered = scheduler.filter_tasks(
        [completed_task, pending_task], status="completed")

    assert [task.id for task in filtered] == [1]


def test_filter_tasks_by_pet_name() -> None:
    mochi = Pet(name="Mochi", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)
    task_mochi = Task(
        id=1,
        title="Morning walk",
        category="walking",
        duration_minutes=30,
        priority="high",
        is_required=True,
        applies_to=mochi,
    )
    task_luna = Task(
        id=2,
        title="Dinner",
        category="feeding",
        duration_minutes=10,
        priority="high",
        is_required=True,
        applies_to=luna,
    )

    scheduler = Scheduler(available_minutes=60)
    filtered = scheduler.filter_tasks(
        [task_mochi, task_luna], pet_name="Mochi")

    assert [task.id for task in filtered] == [1]
