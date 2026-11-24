---
name: where-are-we
description: Check whether the session's current direction still serves the user's core goal, and steer back to it.
disable-model-invocation: true
---

# Where Are We?

Run a **bearing check**: measure where the session is heading now against the user's core goal, and steer back when it has drifted. The check is done when the user can see where the session stands relative to the goal and the work continues on a line that serves it.

## 1. Take the goal

The **goal** is the user's core goal for this session, in the user's terms. Take it from the first source that has one:

1. the goal stated with this invocation;
2. the goal the user most recently stated or confirmed earlier in the session.

If neither exists, ask the user for the goal in one question and wait. Use the goal as the user gave it; sharpening it is the user's call.

## 2. Read the current heading

The **current heading** is where the session is going now: the topic under discussion, the items still open, and the next step the Agent proposed or planned. Read only these; an earlier turn matters only where it still feeds the heading.

Mark each part of the heading as serving the goal or **drifted**. A part has drifted when the Agent led the session there and the goal does not depend on it: an improvement beyond what the goal needs, a detail the goal does not turn on, an adjacent problem picked up along the way. A detour the user started stays on the heading as the user's choice.

Step 2 is complete when every part of the current heading is marked, and each drifted part has a one-line reason naming where it departs from the goal.

## 3. Steer back

Drop every drifted part: stop pursuing it and leave it out of the next step. Files changed while pursuing a drifted part stay as they are; list them with a suggested action, and revert only when the user agrees.

Reply with three parts:

- **Goal**: the goal from Step 1.
- **Drift**: each drifted part with its reason, or a statement that the heading is on course.
- **Next step**: the next step that serves the goal.

Then carry out that next step.
