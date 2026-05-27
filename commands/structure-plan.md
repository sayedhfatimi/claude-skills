Turn the input into a concrete implementation plan ready for `/audit-plan`.
 
Input may be a single feature name or a hyphenated list of features. Either way, produce one unified plan.
 
For each feature or the single feature given:
 
1. State what needs to be built in plain terms — one or two sentences, no ambiguity
2. List every file that will need to be created or modified, with a reason for each
3. Define the types, interfaces, and schemas required — be explicit about shapes, not just names
4. Specify the implementation sequence in dependency order — what must exist before what
5. State any assumptions the plan is making about existing code, APIs, or behaviour that `/audit-plan` will need to verify
If multiple features were given, identify any shared types, utilities, or files across them and plan those once at the top before the per-feature sections.
 
Output the plan as structured markdown. Keep it concrete enough that `/audit-plan` has something unambiguous to check against real code.
