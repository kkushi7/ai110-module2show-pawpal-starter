# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    Classes should include: 
    - owner: name, pet information, add and edit tasks and schedule
    - pet: type, age
    - tasks: walking, feeding, meds, etc.
    - scheduler: avalability, priority, owner preferences

UML diagram:
```mermaid
classDiagram
    class Owner {
        +name: str
        +preferences: dict
        +pets: list[Pet]
        +tasks: list[Task]
        +add_pet(pet: Pet)
        +add_task(task: Task)
        +edit_task(task_id: int, updates: dict)
        +set_preferences(preferences: dict)
    }

    class Pet {
        +name: str
        +species: str
        +age: int
        +notes: str
    }

    class Task {
        +id: int
        +title: str
        +category: str
        +duration_minutes: int
        +priority: str
        +is_required: bool
        +applies_to: Pet
        +estimate_score() int
    }

    class Scheduler {
        +available_minutes: int
        +owner_preferences: dict
        +generate_daily_plan(owner: Owner) list[Task]
        +sort_by_priority(tasks: list[Task]) list[Task]
        +fits_time_limit(task: Task, used_minutes: int) bool
        +explain_plan(plan: list[Task]) str
    }

Relationship between classes:
    Owner "1" --> "1..*" Pet : owns
    Owner "1" --> "0..*" Task : manages
    Task "0..*" --> "1" Pet : for
    Scheduler ..> Owner : reads data
    Scheduler ..> Task : ranks/selects
```

Responsibilities by class:
- `Owner`: stores owner profile, pet info, and task list; supports adding/editing tasks and managing preferences.
- `Pet`: stores pet-specific attributes (name, species/type, age) used to scope tasks.
- `Task`: represents care activities like walking, feeding, meds, grooming, and enrichment with duration/priority metadata.
- `Scheduler`: applies constraints (available time, priorities, owner preferences) to build a daily plan and explain task choices.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
