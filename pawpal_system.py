from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


@dataclass
class Task:
    id: int
    title: str
    category: str
    duration_minutes: int
    priority: str
    is_required: bool
    applies_to: Pet
    recurrence: str | None = None
    status: str = "pending"

    def mark_complete(self) -> None:
        self.status = "completed"

    def estimate_score(self) -> int:
        """Compute a ranking score used by Scheduler when selecting tasks."""
        priority_scores = {
            "high": 3,
            "medium": 2,
            "low": 1,
        }
        base = priority_scores.get(self.priority.lower(), 0) * 10
        required_bonus = 5 if self.is_required else 0
        shorter_task_bonus = max(0, 30 - self.duration_minutes) // 5
        return base + required_bonus + shorter_task_bonus


@dataclass
class Owner:
    name: str
    preferences: dict[str, Any] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def edit_task(self, task_id: int, updates: dict[str, Any]) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                return True
        return False

    def set_preferences(self, preferences: dict[str, Any]) -> None:
        self.preferences = preferences


@dataclass
class Scheduler:
    available_minutes: int
    owner_preferences: dict[str, Any] = field(default_factory=dict)

    def mark_task_complete(self, owner: Owner, task_id: int) -> Task | None:
        """Mark a task complete and auto-create the next recurring task instance."""
        for task in owner.tasks:
            if task.id != task_id:
                continue

            task.mark_complete()
            if task.recurrence not in {"daily", "weekly"}:
                return None

            next_task = Task(
                id=self._next_task_id(owner.tasks),
                title=task.title,
                category=task.category,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                is_required=task.is_required,
                applies_to=task.applies_to,
                recurrence=task.recurrence,
                status="pending",
            )
            owner.add_task(next_task)
            task.applies_to.add_task(next_task)
            return next_task

        return None

    def _next_task_id(self, tasks: list[Task]) -> int:
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1

    def filter_tasks(
        self,
        tasks: list[Task],
        status: str | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter tasks by completion status and/or pet name."""
        filtered = tasks
        if status is not None:
            filtered = [task for task in filtered if task.status == status]
        if pet_name is not None:
            normalized = pet_name.strip().lower()
            filtered = [
                task
                for task in filtered
                if task.applies_to.name.strip().lower() == normalized
            ]
        return filtered

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by duration so shorter tasks are considered first."""
        return sorted(tasks, key=lambda task: task.duration_minutes)

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        preferred_categories = set(
            self.owner_preferences.get("preferred_categories", []))

        def task_sort_key(task: Task) -> tuple[int, int]:
            preference_bonus = 1 if task.category in preferred_categories else 0
            return (task.estimate_score() + preference_bonus, -task.duration_minutes)

        return sorted(tasks, key=task_sort_key, reverse=True)

    def fits_time_limit(self, task: Task, used_minutes: int) -> bool:
        return used_minutes + task.duration_minutes <= self.available_minutes

    def generate_daily_plan(self, owner: Owner) -> list[Task]:
        if self.owner_preferences:
            owner.set_preferences(self.owner_preferences)

        selected: list[Task] = []
        used_minutes = 0

        time_sorted_tasks = self.sort_by_time(owner.tasks)
        for task in self.sort_by_priority(time_sorted_tasks):
            if self.fits_time_limit(task, used_minutes):
                selected.append(task)
                used_minutes += task.duration_minutes

        return selected

    def explain_plan(self, plan: list[Task]) -> str:
        if not plan:
            return "No tasks could be scheduled within the available time."

        lines = [
            f"Planned {len(plan)} task(s) within {self.available_minutes} available minutes:",
        ]
        running_total = 0
        for task in plan:
            running_total += task.duration_minutes
            required_text = "required" if task.is_required else "optional"
            lines.append(
                f"- {task.title} ({task.category}, {task.priority}, {required_text}, "
                f"{task.duration_minutes} min, cumulative: {running_total} min)"
            )
        return "\n".join(lines)
