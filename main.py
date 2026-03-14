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
        )
    )

    return owner


def main() -> None:
    owner = build_sample_data()
    scheduler = Scheduler(
        available_minutes=60,
        owner_preferences={"preferred_categories": ["walking", "feeding"]},
    )

    plan = scheduler.generate_daily_plan(owner)

    print("Today's Schedule")
    print("=" * 16)

    if not plan:
        print("No tasks could be scheduled today.")
        return

    for idx, task in enumerate(plan, start=1):
        print(
            f"{idx}. {task.title} for {task.applies_to.name} "
            f"({task.duration_minutes} min, priority: {task.priority})"
        )


if __name__ == "__main__":
    main()
