---
name: audit-plan
description: Use after an implementation plan is drafted and before any code is written, to audit the plan against the actual code it touches and correct wrong assumptions.
---

Audit the plan above against the relevant code surface. Before proceeding to implementation:

1. Read the actual implementation of every file, function, and module referenced in the plan
2. Verify all assumptions — confirm signatures, types, exports, and dependencies match what the plan expects
3. Identify any gaps between the plan's model of the code and the code's actual shape
4. Revise the plan where assumptions were wrong, then confirm the corrected plan before writing any code
