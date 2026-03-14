from pawpal_system import Pet, Task


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
