from pawpal_system import Owner, Pet, Scheduler, Task


def build_sample_data() -> Owner:
    owner = Owner(name="Jordan")

    dog = Pet(name="Mochi", species="dog", age=4)
    cat = Pet(name="Luna", species="cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    owner.add_task(
        Task(
            id=1,
            title="Morning walk",
            category="walking",
            duration_minutes=30,
            priority="high",
            is_required=True,
            applies_to=dog,
            scheduled_time="08:00",
        )
    )
    owner.add_task(
        Task(
            id=2,
            title="Breakfast feeding",
            category="feeding",
            duration_minutes=10,
            priority="high",
            is_required=True,
            applies_to=cat,
            scheduled_time="08:00",
        )
    )
    owner.add_task(
        Task(
            id=3,
            title="Evening meds",
            category="meds",
            duration_minutes=15,
            priority="medium",
            is_required=True,
            applies_to=dog,
            scheduled_time="18:00",
        )
    )
    owner.add_task(
        Task(
            id=4,
            title="Grooming",
            category="grooming",
            duration_minutes=25,
            priority="low",
            is_required=False,
            applies_to=cat,
            scheduled_time="19:00",
        )
    )

    # Mark one task complete to demonstrate status filtering.
    owner.tasks[1].mark_complete()

    return owner


def print_task_list(header: str, tasks: list[Task]) -> None:
    print(header)
    print("-" * len(header))
    if not tasks:
        print("No tasks to show.")
        print()
        return

    for idx, task in enumerate(tasks, start=1):
        time_text = task.scheduled_time or "unscheduled"
        print(
            f"{idx}. {task.title} for {task.applies_to.name} "
            f"({task.duration_minutes} min, {task.priority}, {time_text}, status: {task.status})"
        )
    print()


def main() -> None:
    owner = build_sample_data()
    scheduler = Scheduler(
        available_minutes=60,
        owner_preferences={"preferred_categories": ["walking", "feeding"]},
    )

    print_task_list("Tasks As Added (Out of Order)", owner.tasks)

    sorted_by_time = scheduler.sort_by_time(owner.tasks)
    print_task_list("Tasks Sorted By Time", sorted_by_time)

    completed_tasks = scheduler.filter_tasks(owner.tasks, status="completed")
    print_task_list("Completed Tasks", completed_tasks)

    mochi_tasks = scheduler.filter_tasks(owner.tasks, pet_name="Mochi")
    print_task_list("Tasks For Mochi", mochi_tasks)

    conflict_warnings = scheduler.detect_time_conflicts(owner.tasks)
    if conflict_warnings:
        print("Schedule Warnings")
        print("-" * 17)
        for warning in conflict_warnings:
            print(warning)
        print()

    plan = scheduler.generate_daily_plan(owner)
    print_task_list("Today's Schedule", plan)


if __name__ == "__main__":
    main()
