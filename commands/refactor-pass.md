Produce a comprehensive, non-destructive `REFACTOR_PLAN.md` for the current codebase — a read-only structural analysis that surveys naming, structure, consolidation, and dead code, and drives a later implementation phase.

---

## Phase 1 — Project Survey

Start by building a complete picture of the project before reading individual files.

1. Run `find . -type f` (or equivalent) filtered to source files — exclude `node_modules`,
   `.git`, `dist`, `build`, `.next`, `coverage`, and any lock files. List every source file
   with its path.
2. Read the top-level `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` (whichever
   applies) to understand language, framework, tooling, and declared dependencies.
3. Read any config files that affect structure: `tsconfig.json`, `eslint.config.*`,
   `biome.json`, path alias maps, barrel export patterns.
4. Note the folder topology: how many layers deep, which directories exist, what naming
   pattern is used for directories (kebab-case, PascalCase, feature-vs-type grouping).

Document what you find in an internal summary before proceeding — you'll reference it
throughout the plan.

---

## Phase 2 — Deep Analysis

Work through each concern category below. For each one, read the relevant files in full —
do not skim or sample. Track every finding as you go.

### 2A · File & Folder Organisation

- Identify files that are misplaced relative to their responsibility (e.g., a utility living
  in a component directory, a type file living next to a route handler).
- Identify directories that mix concerns and should be split.
- Identify related files that are scattered and should be co-located.
- Flag any files that are oversized and likely contain too many responsibilities.
- Flag missing index/barrel files where they would improve import ergonomics.
- Check for inconsistent directory naming (e.g., mixing `components/` and `Components/`,
  `utils/` and `helpers/` for the same purpose).

### 2B · Naming Conventions — Variables & Constants

- Identify variables that use ambiguous single-letter or abbreviation names outside of
  tight loop scopes (e.g., `d`, `tmp`, `res`, `val`, `obj`).
- Identify boolean variables that do not read as predicates (should start with `is`, `has`,
  `can`, `should`, `did`, `will`, etc.).
- Identify magic numbers or string literals that should be named constants.
- Flag inconsistent casing (e.g., `camelCase` vs `snake_case` mixed in the same scope or
  the same language).
- Flag variables whose names contradict what they actually hold.

### 2C · Naming Conventions — Functions & Methods

- Identify functions whose names do not describe their action (prefer verb-noun: `fetchUser`,
  `buildPayload`, `validateToken`).
- Identify functions named with vague verbs: `handle`, `process`, `do`, `run`, `manage`,
  `execute` with no qualifying noun — these almost always need a more specific name.
- Flag functions named after implementation details rather than intent (e.g.,
  `useEffectForAuth` instead of `useAuthSession`).
- Flag getter functions that mutate state, or mutation functions whose names suggest they
  are read-only.
- Identify event handler names that don't follow a consistent convention (e.g., mixing
  `onClick`, `handleClick`, `onClickButton`).

### 2D · Naming Conventions — Types, Interfaces & Enums

- Identify type/interface names that are generic to the point of meaninglessness (`Data`,
  `Info`, `Params`, `Props`, `Options` without a qualifying prefix).
- Flag enums or union types whose members lack consistent casing or naming patterns.
- Identify types that duplicate each other (even partially) — candidates for a shared base
  or intersection type.
- Flag interfaces vs types that follow inconsistent conventions (if the project has a
  preference, enforce it; if not, note the inconsistency).
- Identify prop types defined inline in component signatures that should be extracted and
  named.

### 2E · Function Consolidation & Decomposition

- Identify functions that are doing two or more distinct things and should be split.
- Identify near-duplicate functions (same logic, different variable names or minor
  variations) — candidates for a single parameterised version.
- Identify utility logic that is copy-pasted across files and should live in a shared module.
- Identify deeply nested logic (3+ levels of if/loop nesting) that should be extracted
  into helper functions.
- Flag functions that are longer than ~60 lines — these almost always benefit from
  decomposition (use judgement, not a hard rule).

### 2F · Type & Interface Organisation

- Identify types that are defined in the file where they are first used but are referenced
  across multiple files — they should be moved to a shared types module.
- Identify types that are defined multiple times with the same or near-same shape.
- Flag loosely typed signatures: `any`, `unknown` used without narrowing, `object`,
  untyped function parameters.
- Identify domain concepts that have no dedicated type (logic is passing raw primitives
  where a named type would make intent clearer).

### 2G · Import Structure & Module Boundaries

- Flag circular import chains if detectable from static analysis.
- Identify imports that reach deep into another module's internals rather than its public
  surface (`../../other-feature/internal/helper`).
- Flag inconsistent import ordering (if the project has an ESLint/Biome rule, flag
  violations; if not, note the inconsistency).
- Identify re-exports that are missing from barrel files, causing consumers to import
  directly from deep paths.

### 2H · Dead Code & Unused Exports

- Identify exported functions, types, or constants that appear to have no importers within
  the project.
- Identify commented-out code blocks that should either be restored or deleted.
- Identify `TODO` / `FIXME` / `HACK` comments — surface them as a catalogue rather than
  a refactoring task.

---

## Phase 3 — Plan Assembly

Once the analysis is complete, write `REFACTOR_PLAN.md` to the project root.

### Document structure

Use this exact structure:

```
# Refactor Plan
> Generated by /refactor-pass · [date]

## Summary
[2–4 sentence executive overview: what the main structural issues are, and what this plan
addresses. Be specific — name the actual problems found, not generic statements.]

## Scope
[List the directories and files that were analysed. Note anything deliberately excluded.]

---

## 1 · File & Folder Organisation
### Findings
[Each finding as a numbered item with file path(s) and a clear explanation of the problem.]
### Recommended Changes
[Concrete, specific actions: move X to Y, rename dir A to B, split file C into C1 and C2.]

## 2 · Variable & Constant Naming
### Findings
[File path + line reference + current name + reason it's unclear.]
### Recommended Renames
[Table or list: Current → Suggested · Rationale]

## 3 · Function & Method Naming
### Findings
[File path + function name + reason the name is inadequate.]
### Recommended Renames
[Current → Suggested · Rationale]

## 4 · Type, Interface & Enum Naming
### Findings
[File path + type name + issue.]
### Recommended Renames / Restructuring
[Current → Suggested · Rationale, or description of structural change.]

## 5 · Function Consolidation & Decomposition
### Functions to Split
[Name, file, and proposed split.]
### Functions to Consolidate
[Names, files, and proposed unified function signature.]
### Utilities to Extract
[Description of repeated logic and proposed shared module location.]

## 6 · Type Organisation
### Types to Promote to Shared Module
[Type name, current file, proposed destination.]
### Duplicate / Overlapping Types
[Names and proposed resolution.]
### Loose Typing to Tighten
[Location and recommended type.]

## 7 · Import Structure
### Circular Dependencies
[If any found.]
### Boundary Violations
[File importing from deep internal path — what it should import instead.]
### Barrel Export Gaps
[What should be added to which index file.]

## 8 · Dead Code & TODO Catalogue
### Apparently Unused Exports
[Name and file.]
### Commented-Out Code
[File and line range.]
### TODO / FIXME Register
[File, line, comment text.]

---

## Priority Matrix

| # | Change | Category | Effort | Impact |
|---|--------|----------|--------|--------|
| 1 | ...    | ...      | Low    | High   |
...

[Rank all significant items. Effort: Low / Medium / High. Impact: Low / Medium / High.
Items that are Low effort + High impact should appear first.]

---

## Implementation Notes

[Any cross-cutting concerns: things that must happen in a specific order, renames that
require a find-and-replace across the whole codebase, changes that will affect the public
API or external consumers, and anything the implementer should be aware of before starting.]
```

---

## Conduct Rules

- **Read-only pass.** Do not modify, create, or delete any project file other than
  writing `REFACTOR_PLAN.md` at the end.
- **Be specific.** Every finding must cite a file path. Vague statements like "some
  functions have poor names" are not acceptable — name the functions.
- **Distinguish fact from opinion.** Naming is partly subjective. Where a finding is a
  clear violation of the project's own conventions, state it as a fact. Where it is a
  judgement call, say so.
- **Respect existing conventions.** If the project consistently uses a pattern (even one
  you might disagree with), your job is to flag *inconsistencies* with that pattern, not
  to argue against the pattern itself. Only recommend changing the convention if it is
  actively harmful (e.g., naming collisions, misleading names).
- **No implementation.** This command produces a plan. Do not refactor anything. The user
  decides what to act on.
- **Proportionality.** A 3-file utility script needs a lighter-touch plan than a 60-file
  production service. Calibrate depth of analysis and length of plan to the actual
  complexity of the project.

---

## Completion

When the plan is written:

1. Confirm the file has been saved as `REFACTOR_PLAN.md` in the project root.
2. Print a brief console summary:
   - Total files analysed
   - Count of findings per category
   - Top 3 highest-priority items from the Priority Matrix
3. Suggest the next step: review the plan, prune anything out of scope, then run
   `/structure-plan` or begin implementation with the highest-priority items.
