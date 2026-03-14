from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_mark_task_complete_creates_next_daily_instance() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", age=4)
    owner.add_pet(pet)
    daily_task = Task(
        id=1,
        title="Morning walk",
        category="walking",
        duration_minutes=30,
        priority="high",
        is_required=True,
        applies_to=pet,
        recurrence="daily",
    )
    owner.add_task(daily_task)
    pet.add_task(daily_task)

    scheduler = Scheduler(available_minutes=60)
    next_task = scheduler.mark_task_complete(owner, task_id=1)

    assert daily_task.status == "completed"
    assert next_task is not None
    assert next_task.id == 2
    assert next_task.status == "pending"
    assert next_task.recurrence == "daily"
    assert len(owner.tasks) == 2


def test_mark_task_complete_no_recurrence_creates_no_new_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna", species="cat", age=2)
    owner.add_pet(pet)
    one_time_task = Task(
        id=1,
        title="Vet visit",
        category="health",
        duration_minutes=45,
        priority="high",
        is_required=True,
        applies_to=pet,
        recurrence=None,
    )
    owner.add_task(one_time_task)
    pet.add_task(one_time_task)

    scheduler = Scheduler(available_minutes=60)
    next_task = scheduler.mark_task_complete(owner, task_id=1)

    assert one_time_task.status == "completed"
    assert next_task is None
    assert len(owner.tasks) == 1


def test_detect_time_conflicts_returns_warning() -> None:
    mochi = Pet(name="Mochi", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)
    task_one = Task(
        id=1,
        title="Morning walk",
        category="walking",
        duration_minutes=30,
        priority="high",
        is_required=True,
        applies_to=mochi,
        scheduled_time="08:00",
    )
    task_two = Task(
        id=2,
        title="Breakfast feeding",
        category="feeding",
        duration_minutes=10,
        priority="high",
        is_required=True,
        applies_to=luna,
        scheduled_time="08:00",
    )

    scheduler = Scheduler(available_minutes=60)
    warnings = scheduler.detect_time_conflicts([task_one, task_two])

    assert len(warnings) == 1
    assert "Warning:" in warnings[0]
    assert "08:00" in warnings[0]


def test_sorting_correctness_returns_tasks_in_chronological_order() -> None:
    pet = Pet(name="Mochi", species="dog", age=4)
    task_late = Task(
        id=1,
        title="Evening walk",
        category="walking",
        duration_minutes=15,
        priority="medium",
        is_required=False,
        applies_to=pet,
        scheduled_time="18:30",
    )
    task_early = Task(
        id=2,
        title="Breakfast",
        category="feeding",
        duration_minutes=30,
        priority="high",
        is_required=True,
        applies_to=pet,
        scheduled_time="08:00",
    )
    task_mid = Task(
        id=3,
        title="Meds",
        category="meds",
        duration_minutes=10,
        priority="high",
        is_required=True,
        applies_to=pet,
        scheduled_time="12:00",
    )

    scheduler = Scheduler(available_minutes=120)
    sorted_tasks = scheduler.sort_by_time([task_late, task_early, task_mid])

    assert [task.id for task in sorted_tasks] == [2, 3, 1]


def test_recurrence_logic_daily_completion_creates_next_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", age=4)
    owner.add_pet(pet)
    daily_task = Task(
        id=1,
        title="Daily walk",
        category="walking",
        duration_minutes=20,
        priority="high",
        is_required=True,
        applies_to=pet,
        recurrence="daily",
    )
    owner.add_task(daily_task)
    pet.add_task(daily_task)

    scheduler = Scheduler(available_minutes=60)
    next_task = scheduler.mark_task_complete(owner, task_id=1)

    assert daily_task.status == "completed"
    assert next_task is not None
    assert next_task.id == 2
    assert next_task.recurrence == "daily"
    assert next_task.status == "pending"


def test_conflict_detection_flags_duplicate_times() -> None:
    mochi = Pet(name="Mochi", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)
    task_one = Task(
        id=1,
        title="Walk",
        category="walking",
        duration_minutes=30,
        priority="high",
        is_required=True,
        applies_to=mochi,
        scheduled_time="09:00",
    )
    task_two = Task(
        id=2,
        title="Feed",
        category="feeding",
        duration_minutes=10,
        priority="high",
        is_required=True,
        applies_to=luna,
        scheduled_time="09:00",
    )

    scheduler = Scheduler(available_minutes=60)
    warnings = scheduler.detect_time_conflicts([task_one, task_two])

    assert warnings
    assert "Warning:" in warnings[0]
    assert "09:00" in warnings[0]
