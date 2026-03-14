```
classDiagram


class Owner {
    +name: str
    + preferences: dict
    + pets: list[Pet]
    + tasks: list[Task]
    + add_pet(pet: Pet)
    + add_task(task: Task)
    + edit_task(task_id: int, updates: dict)
    + set_preferences(preferences: dict)
}


class Pet {
    +name: str
    + species: str
    + age: int
    + notes: str
}


class Task {
    +id: int
    + title: str
    + category: str
    + duration_minutes: int
    + priority: str
    + is_required: bool
    + applies_to: Pet
    + estimate_score() int
}


class Scheduler {
    +available_minutes: int
    + owner_preferences: dict
    + generate_daily_plan(owner: Owner) list[Task]
    + sort_by_priority(tasks: list[Task]) list[Task]
    + fits_time_limit(task: Task, used_minutes: int) bool
    + explain_plan(plan: list[Task]) str
}


Owner "1" - -> "1..*" Pet: owns
Owner "1" - -> "0..*" Task: manages
Task "0..*" - -> "1" Pet: for
Scheduler .. > Owner: reads data
Scheduler .. > Task: ranks/selects


```

Responsibilities by class:
- `Owner`: stores owner profile, pet info, and task list
supports adding/editing tasks and managing preferences.
- `Pet`: stores pet-specific attributes(name, species/type, age) used to scope tasks.
- `Task`: represents care activities like walking, feeding, meds, grooming, and enrichment with duration/priority metadata.
- `Scheduler`: applies constraints(available time, priorities, owner preferences) to build a daily plan and explain task choices.
