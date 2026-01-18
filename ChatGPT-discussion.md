
Je zei:
I want to know how software companies track their projects from start to mvp to launch. How do they integrate new features. 
Tell me how they work with feature documents, development document, system documents? 
I'm a vibe coder so I need to understand this. 
I'm currently reworking the flow of the agents that I use to vibe code. 
Be critical of yourself when you report back to me.
ChatGPT zei:
Great question — and I like that you explicitly said “I’m a vibe coder”. That’s actually the right lens to use here, because most explanations of software delivery are written by process people, not builders.

I’ll explain how good software companies actually work, not the textbook fantasy. Then I’ll translate it into a vibe-coder–compatible operating system, and I’ll be critical about where my own explanations usually fail people like you.

1. The honest lifecycle: idea → MVP → launch → evolution
Forget linear “waterfall” diagrams. In reality, companies operate in loops.

The real loop
Problem → Hypothesis → Thin solution → Feedback → Adjustment → Repeat
Everything else (documents, tickets, systems) exists only to support this loop, not replace thinking.

2. How projects are actually tracked (in companies that ship)
At a high level, there are 3 parallel tracks:
Product thinking (what & why)

Delivery execution (how & when)

System integrity (will this break things?)

Most failures happen when one of these tracks dominates the others.

3. Documents: what exists vs what is useful
I’ll be blunt.

Most companies produce too many documents that nobody reads, and too few artifacts that help decisions.

Here’s the useful minimum set.

4. Feature documents (Product Docs)
What they are in reality
A feature doc is not a spec.
It’s a decision-making artifact.

Good companies use a 1–3 page doc max:
Often called:

PRD (Product Requirements Doc)

RFC (Request for Comments)

Feature Brief

What actually matters inside
1. Problem statement (1 paragraph)
2. Who is this for (specific user)
3. What success looks like (measurable)
4. What we are NOT doing (scope boundaries)
5. Rough solution direction (not UI-perfect)
⚠️ Critical truth
If a feature doc is longer than the feature itself, the feature is wrong.

What vibe coders usually miss
Writing why before what

Explicitly stating what is out of scope

Defining “done” in advance

5. Development documents (Engineering Docs)
These are not product docs
They answer:

“How do we build this without creating a future nightmare?”

Common forms
Technical Design Doc (TDD)

Architecture Decision Record (ADR)

Implementation Plan

What actually matters
1. Entry point (what triggers this feature?)
2. Data flow (what changes state?)
3. Dependencies (what can break?)
4. Failure cases (what happens when things go wrong?)
5. Rollback strategy (how do we undo this?)
Good dev docs are written for future engineers, including future-you.

Brutal truth
If you can’t explain your system in:

1 diagram

10 bullets

…you don’t understand it yet.

6. System documents (Architecture & System Thinking)
These are the least sexy and the most valuable.

What they are
System diagrams

Data models

Integration maps

Security & permission models

Why they exist
They answer:

“If we add one more feature, what breaks?”

In good teams
System docs are updated lazily but intentionally

They evolve after pain, not before hypotheticals

Common mistake
People try to design a perfect system before MVP.

Correct approach:

MVP → Pain → Refactor → Document
7. How new features are integrated (the real flow)
Here’s the actual feature lifecycle in good teams:

Step 1: Feature intake
Problem described

Business/user impact estimated

Rough complexity gut-check

→ Many features die here. That’s healthy.

Step 2: Thin feature definition
Smallest testable version

Explicit exclusions

Success metric defined

This is where vibe coders should thrive.

Step 3: Design + dev spike
Quick prototype

Technical feasibility check

Risks discovered early

⚠️ This step is often missing in solo projects.

Step 4: Build behind flags
Feature toggles

Partial rollout

Internal testing

Nothing ships “fully on” at first.

Step 5: Feedback loop
Metrics

User behavior

Support pain

Only now does iteration start.

8. How companies track all this (tools are secondary)
Common stacks
Product: Notion, Confluence, Linear

Delivery: Jira, Linear, GitHub Projects

Code: Git + PRs

Observability: logs, metrics, alerts

The tool doesn’t matter.
What matters is:

Clear ownership

Clear state of work

Clear decision history

9. Translating this to vibe coding
Let’s make this practical for your agent-based flow.

Your vibe-friendly layers
🧠 Intent layer (why)
📐 Shape layer (what)
🛠 Build layer (how)
🧪 Feedback layer (did it work?)
Each agent should own one layer, not everything.

Example agent split
Product agent → writes 1-page feature brief

System agent → checks “what breaks?”

Builder agent → codes thin solution

Critic agent → tries to kill the feature

Integrator agent → fits it into the system

If one agent tries to do all of this → chaos.

10. Where I need to be critical of myself
Here’s where assistants like me usually fail vibe coders:

❌ Mistake 1: Over-structuring
I tend to:

Introduce too many “best practices”

Pretend you need enterprise-level rigor

You don’t.

❌ Mistake 2: Not protecting momentum
Process can:

Kill flow

Turn coding into admin

Good systems protect energy, not consume it.

❌ Mistake 3: Not adapting to solo builders
Most advice assumes:

Teams

Managers

Meetings

You need internal clarity, not alignment meetings.

11. A better rule of thumb (for you)
For every feature, you should be able to answer:

• Why does this exist?
• What’s the smallest version?
• What might break?
• How will I know it worked?
If you can answer those in 10 minutes, you’re doing it right.

12. Next step (if you want)
If you want, next we can:

Design a vibe-first feature doc template

Design an agent orchestration flow (who speaks when)

Audit your current agent setup and remove dead weight

Just tell me which one you want to tackle first.

Je zei:
Okay, so i already have an app, but I have questions on how to move forward & better from here. 
Currently, I have development docs (15) which have the following information:
- Project Overview
- Architecture
- Database
- API Design
- Authentication
- ERror- Handling
- Front-end pages
- Frontend components
- Frontend interactions
- Data visualizations
- Forms Validation
- TEsting strategy
- Deployment
- Responsive accesibility
- Performance state
- Page layouts

These are documents between 500 - 2000 lines with indications how everything is structured.
Based on these documents, I started creating phases with the architect agent which then created 5-9 deliverables. Each deliverable was executed by a command to use a Developper agent, a UI/UX agent, API-designer agent, and was completed by the Quality reviewer. 
Then i manually tested everything in my browser and if I encountered bugs it looked & located the bugs with the debugger agent & then fixed them with the developper agent. 

One of the issue that I faced is that when changes happen, they do not reflect this in the development documents. Also it is difficult to stay true to the original plan which was created in another session by another agent.
I also feel like development docs can not be feature documents. It does not explain in verbose what the feature is able to do/ must do. 

How can we improve this? 
Any advise?
ChatGPT zei:
You’re not wrong — what you’re describing is exactly the wall most serious solo builders hit after their first “it actually works” moment.

I’ll be very direct and critical, because you’re already operating at a level where generic advice is useless.

1. Diagnosis (what’s actually broken)
You don’t have a coding problem.
You have a knowledge coherence problem.

Right now:

Your development docs are authoritative but stale

Your agents execute well but don’t update truth

Your original plan exists, but has no gravity

Your features exist in code, not in meaning

That’s not a failure — it’s a predictable phase transition.

2. The core mistake (and it’s a common one)
You’re using development documents as a source of truth.

That works until the first real iteration. After that, it collapses.

Why this fails
Dev docs describe structure

Reality evolves through behavior

Code changes faster than prose

Agents optimize locally, not globally

Once changes start flowing, documents become historical fiction.

3. The missing layer: Feature Truth vs System Truth
You correctly sensed this:

“Development docs cannot be feature documents.”

Exactly.

You are missing a middle layer.

You currently have:
🧱 System knowledge (dev docs)
⚙️ Execution (agents + code)
What you need:
🎯 Feature truth (what the app DOES)
🧱 System truth (how it is built)
⚙️ Execution (how it changes)
Without this, drift is inevitable.

4. Reframe your documents (this is the key move)
4.1 Freeze your dev docs emotionally
First: stop trying to keep all 15 dev docs perfectly up to date.

That’s not realistic for a solo builder.

Instead:

Treat them as structural reference

Update them only after major refactors

Accept they will lag behind reality

This is not laziness — it’s correct system design.

5. Introduce a Feature Canon (non-negotiable)
You need one authoritative source that answers:

“What does this app actually do, today?”

Call it:
Feature Canon

Capability Map

Product Reality Doc

Name doesn’t matter. Authority does.

5.1 Feature Canon structure (vibe-friendly)
Each feature gets 1–2 pages max.

Feature: Smart Trip Suggestion

1. Intent
   Why does this feature exist?
   What user pain does it solve?

2. Capabilities
   What the feature CAN do
   (bullet points, observable behavior)

3. Constraints
   What it deliberately does NOT do

4. Inputs
   User actions / data required

5. Outputs
   UI changes / data created / side effects

6. Edge behavior
   What happens when data is missing, wrong, or delayed

7. Current status
   🟢 Stable | 🟡 Partial | 🔴 Experimental
⚠️ No architecture.
⚠️ No implementation detail.
⚠️ No future promises.

Only observable truth.

6. Redefine agent responsibilities (critical fix)
Your agents are doing tasks, not guardianship.

That’s why truth decays.

6.1 Introduce two new roles (this is important)
🧭 Feature Steward (new)
Responsibility:
Keeps Feature Canon in sync with reality.

Rules:

Updates feature doc after every meaningful change

Can block “done” if canon is outdated

Does NOT write code

🧠 System Archivist (new)
Responsibility:
Updates dev docs selectively.

Rules:

Only updates after:

New dependency

New data model

New cross-system coupling

Ignores UI tweaks & logic changes

Why this works
You stop expecting everyone to update everything.

You create explicit ownership of truth.

7. Change your definition of “done”
This is where drift sneaks in.

Old “done”
Code compiles

UI works

Tests pass

New “done”
✔ Code works
✔ Feature Canon updated
✔ System impact noted (if any)
No doc update → feature is not done.

8. Fix the “original plan drift” problem
This one is subtle.

Your original plan is dying because:

It has no enforcement mechanism

It exists outside execution

Agents don’t feel its weight

Solution: Plans become constraints, not instructions
Create a Plan Guardrail Doc.

For each phase:

Phase Goal (non-negotiable)
Allowed changes
Forbidden changes
Assumptions being tested
Agents may deviate — but must log deviations.

9. Make change explicit (this will feel liberating)
Introduce a Change Log, not more docs.

Every significant change answers:

• What changed?
• Why?
• Which feature does this affect?
• Does this invalidate earlier assumptions?
This is how you preserve narrative continuity.

10. Critical feedback on your current system (honest)
You’ve built something impressive — but:

What’s working
Strong execution pipeline

Clear agent separation

Manual testing loop is healthy

You think in systems, not snippets

What’s hurting you
Docs trying to be everything

No single “truth layer”

Agents optimize tasks, not coherence

Too much respect for old plans

Plans are hypotheses, not contracts.

11. The mental shift you need
Stop thinking:

“How do I keep docs in sync?”

Start thinking:

“Where does truth live?”

Truth lives in three places only:

Feature Canon (behavior)

Code (reality)

Change Log (history)

Everything else is supporting material.

12. Concrete next steps (do these in order)
Step 1 (1–2 hours)
Create Feature Canon for 3 core features only.

Step 2
Add Feature Steward step to your agent pipeline.

Step 3
Redefine “done” to include canon update.

Step 4
Let dev docs lag without guilt.

If you want, next we can:

Design a minimal Feature Canon template

Redesign your agent workflow visually

Decide which of your 15 dev docs should be archived or merged

Tell me where you want to go next.

Je zei:
I work entirely in claude code in VCS. Should i create the feature canon per feature? How do I mention compatability with other features? 
would this not create a lot of new documents? 
ChatGPT zei:
Short answer: yes per feature — but only if you aggressively control scope and gravity.
Long answer below, with trade-offs and a hard cap so this doesn’t explode into doc hell.

I’ll be critical and concrete.

1. Where the Feature Canon should live (given Claude Code + VCS)
You’re doing the right thing by living inside the repo.

That gives you:

Versioned truth

Diffable intent

Change history tied to code

Correct location
/docs/features/
  ├─ F001-smart-suggestions.md
  ├─ F002-user-preferences.md
  ├─ F003-itinerary-builder.md
Not Notion.
Not external tools.
Close to code or it dies.

2. One canon doc per feature — but not “one doc per idea”
This is the first trap.

A feature canon is for:
User-visible capability

Long-lived behavior

Something you’d explain to a user or tester

NOT for:
Minor UI tweaks

Internal helpers

Temporary experiments

If it doesn’t change how the user experiences the app → no canon doc.

3. Hard rule: Feature Canon is NOT a spec
If you let these become specs, you’re dead.

Size constraint (non-negotiable)
Max ~200–400 lines

If it grows → split the feature

If it still grows → the feature is too big

This constraint is what prevents doc explosion.

4. Compatibility is not explained inline — it’s declared explicitly
You don’t describe compatibility.
You declare relationships.

This is the key design move.

5. Add a “Feature Relationships” section (lightweight but powerful)
Inside every Feature Canon:

## Feature Relationships

### Depends on
- F002 User Preferences
- F005 Location Scoring Engine

### Enhances
- F004 Daily Itinerary

### Conflicts with
- None

### Shared State
- user.preferences
- trip.context
That’s it.

No prose.
No explanation.
Just graph edges.

This turns your features into a navigable system, not essays.

6. Why this scales without doc bloat
Because:

You’re not duplicating explanations

You’re not restating behavior

You’re only declaring coupling

Think of Feature Canon as headers, not textbooks.

7. You do NOT document compatibility logic
This is where most systems fail.

You do not explain how compatibility works.

Why?

That’s system logic → dev docs

Or code → tests

Or emergent behavior → discovered later

Canon only answers:

“If this feature changes, what else should I worry about?”

8. One more doc (only one): Feature Index
To prevent sprawl, you need a single index.

/docs/features/FEATURE_INDEX.md
Example:

F001 Smart Suggestions       🟢 Stable
F002 User Preferences       🟢 Stable
F003 Itinerary Builder      🟡 Partial
F004 Offline Mode           🔴 Experimental
This is your map of reality.

If it’s not in the index, it’s not real.

9. How this integrates with your agent flow
This is important.

Before coding
Architect agent reads:

Feature Canon

Feature Relationships

After coding
Feature Steward agent:

Updates Canon if behavior changed

Updates relationships if coupling changed

Updates status if maturity changed

Quality reviewer
Verifies:

Code behavior matches Canon

Canon claims are testable

No match → not done.

10. Addressing your fear directly: “Isn’t this a lot of documents?”
Yes.
But fewer than what you already have — and with far more value.

Compare:

What you have now	What you’d have
15 massive dev docs	5–12 small feature canons
Hard to update	Cheap to update
Stale fast	Evolves naturally
Describes structure	Describes reality
You already pay the cognitive cost.
This just moves it where it belongs.

11. Critical self-check (on my advice)
Where I might be wrong for you:

If your app is still extremely fluid, even this might feel heavy

If you treat canons as contracts, you’ll freeze creativity

If agents start “writing beautiful docs”, you’ve lost

This system only works if:

You keep it brutally factual

You allow deletion

You let features die

12. The simplest starting point (do NOT overdo this)
Do this first:

Create 2 Feature Canon docs only

Add Feature Relationships

Add Feature Index

Run one full iteration end-to-end

Then reassess.

If you want next:

I can draft a bare-bones Feature Canon template tuned to your repo

Or help you decide which existing behavior deserves a canon

Or redesign your agents so canon updates are automatic but controlled

Tell me where you want to go.

Je zei:
Okay, how about the development docs? Current system is too limited? 
How can we organize this so it is readable?
always Updating? Which agents updates this? 
ChatGPT zei:
Good — this is the right follow-up. You’re no longer asking “what docs do I need”, but “what role should dev docs play without killing momentum?”

I’ll be direct and slightly ruthless.

1. First: your current dev-doc system is overcomplete, not underpowered
15 development documents at 500–2000 lines is not limited.
It’s too authoritative for how fast reality moves.

The issue is not missing docs.
The issue is docs trying to stay equal to code.

They never can.

2. Reframe dev docs: they are NOT living mirrors
Dev docs should never
Describe exact logic flows

Track UI behavior

Mirror current implementation

That’s what code + tests do better.

Dev docs should only
Explain why the system is shaped this way

Document irreversible or expensive decisions

Warn about coupling, constraints, and danger zones

If a doc answers “what happens line-by-line” → delete or archive it.

3. Split your dev docs into 3 explicit classes
Right now everything is mixed. That’s why it’s unreadable.

Class A — System Spine (rarely updated)
Authoritative, slow-moving.

Examples:

Architecture

Database schema (conceptual, not column-level)

Authentication model

Deployment topology

These are load-bearing docs.

Class B — Decision Records (append-only)
These replace most “design explanation” prose.

Call them ADRs.

Each ADR answers:

• What decision was made?
• Why?
• Alternatives considered
• Consequences
Short. Immutable.

This solves “why did we do this?” forever.

Class C — Volatile Notes (allowed to rot)
These are explicitly non-authoritative.

Examples:

Frontend interactions

Component inventories

Performance notes

Testing strategy details

These are working memory, not truth.

They can lag. That’s fine.

4. Concrete folder structure (Claude Code friendly)
/docs/dev/
  ├─ system/
  │   ├─ architecture.md
  │   ├─ auth-model.md
  │   ├─ data-model.md
  │   └─ deployment.md
  │
  ├─ decisions/
  │   ├─ ADR-001-api-style.md
  │   ├─ ADR-002-auth-provider.md
  │   └─ ADR-003-state-management.md
  │
  └─ notes/
      ├─ frontend-notes.md
      ├─ testing-notes.md
      ├─ performance-notes.md
      └─ accessibility-notes.md
This single move will massively improve readability.

5. Which docs must be kept up to date (and which must not)
Must be updated
Only when structural change happens:

Architecture

Data model

Auth model

Deployment topology

If it doesn’t affect system shape → don’t touch them.

Must never be rewritten
ADRs
If a decision changes → write a new ADR, don’t edit the old one.

This preserves narrative continuity.

Allowed to rot
UI descriptions

Interaction flows

Component lists

Performance commentary

Label them clearly as NON-AUTHORITATIVE at the top.

This removes guilt.

6. Agent ownership (this is where systems usually fail)
Right now: everyone touches everything → entropy.

You need exclusive guardianship.

🧠 System Archivist (primary owner)
Updates:

System spine docs

Adds ADRs

Triggered only when:

New dependency introduced

Data shape changes

Cross-feature coupling increases

Does NOT:

Track UI changes

Track feature behavior

🧭 Feature Steward
Updates:

Feature Canon

Feature relationships

Does NOT:

Touch dev docs unless coupling changed

🧪 Quality Reviewer
Verifies:

System docs are not contradicted by code

New coupling is documented somewhere

Flags issues, doesn’t fix docs.

🛠 Developer / UI / API agents
Never update dev docs directly.

This is critical.

They cause drift by accident.

7. When should dev docs be updated? (simple rule)
Ask ONE question:

“Would a new developer make a dangerous mistake without this update?”

If no → don’t update.

If yes → update system doc or add ADR.

8. How to keep dev docs readable (this matters)
Enforce:
One concept per doc

Diagrams over prose

Bullet points over paragraphs

Ban:
Step-by-step flows

UI screenshots

“This function does…”

If it’s operational → code.
If it’s behavioral → Feature Canon.
If it’s irreversible → Dev doc.

9. Addressing your fear: “always updating?”
No.

Reality:
System spine: updated rarely

ADRs: appended occasionally

Notes: updated when useful, ignored otherwise

If you’re updating dev docs weekly, something is wrong.

10. Hard truth (critical but fair)
You’ve already outgrown “docs as blueprints”.

You’re entering:

Docs as institutional memory

Your system broke because you treated memory like a mirror.

11. Minimal corrective action (don’t overdo it)
Do only this first:

Reorganize folders into System / Decisions / Notes

Move existing docs without rewriting

Add NON-AUTHORITATIVE labels to volatile docs

Introduce ADRs for the next 3 big decisions only

Stop there.

If you want next, we can:

Decide which of your 15 docs should be system spine vs notes

Design a one-page ADR template

Tune your agents so doc updates are event-driven, not habitual

Tell me what you want to tackle next.

Je zei:
How do system / Decisions / Notes link back to the feature canon? 
ChatGPT zei:
Excellent — this is the keystone question.
If this link is wrong, everything collapses back into chaos.

I’ll be precise, minimal, and opinionated.

1. The principle (memorize this)
Features declare impact.
Systems explain constraints.
Decisions explain why.
Notes explain “for now”.

The Feature Canon is the only place where everything converges.
System / Decisions / Notes never “own” features.

They only support or constrain them.

2. Direction of links (non-negotiable)
This is the single most important rule:

❌ Do NOT link from system docs to features
❌ Do NOT try to keep bidirectional parity
✅ Features link outward
✅ Systems stay mostly feature-agnostic
Why?
Because features churn. Systems must remain stable.

3. How the Feature Canon links to dev docs
Inside each Feature Canon doc, add one section only:

## Technical Anchors

System Constraints
- auth-model.md (permissions scope)
- data-model.md (trip, location, preference)

Relevant Decisions
- ADR-002 (state management choice)
- ADR-005 (recommendation scoring approach)

Volatile Notes
- frontend-notes.md (component reuse)
That’s it.

No prose.
No explanation.
Just pointers.

4. What those links mean (this is subtle)
A link does not mean:

“This doc describes this feature”

“This doc must be updated when the feature changes”

A link means:

“If this feature breaks or evolves, read this before touching code.”

That’s all.

5. How Decisions (ADRs) reference features — lightly
ADRs should optionally reference:

The triggering feature

Or the class of features affected

Example:

## Context
Triggered by:
- F001 Smart Suggestions
- F003 Itinerary Builder
But ADRs must never track feature behavior.

They capture a moment in time.

6. How System docs stay clean
System docs:

Do NOT list features

Do NOT embed feature logic

Do NOT change often

They describe:

Shapes

Constraints

Contracts

Boundaries

If you find yourself adding “This feature uses…” → stop.

That belongs in the Feature Canon.

7. What Notes do (and why they’re allowed to rot)
Notes are scratchpads.

They exist to:

Help current work

Reduce re-discovery cost

Capture heuristics

They are not truth.

Feature Canon may optionally link to notes if helpful, but:

Notes never link back

Notes never claim authority

This asymmetry is intentional.

8. Visual mental model (important)
Think hub-and-spoke, not a mesh.

            ADR-005
               ↑
auth-model ← FEATURE → data-model
               ↓
        frontend-notes
Feature Canon is the hub.

Systems & Decisions are spokes.

Never connect spokes to each other directly.

9. When links change (this prevents doc churn)
You update Feature Canon links when:
A new system constraint appears

A decision starts to affect behavior

A feature touches a new domain

You do NOT update:
System docs because a feature changed

ADRs because a feature evolved

This preserves stability.

10. Agent responsibility (explicit and enforced)
🧭 Feature Steward
Owns all links from Feature Canon

Updates anchors when behavior changes

🧠 System Archivist
Adds ADRs or updates system docs

Does NOT touch Feature Canon content

🧪 Quality Reviewer
Verifies:

Feature claims are compatible with system constraints

Anchors exist where needed

No one else links anything.

11. Common failure modes (avoid these)
❌ Feature canon becomes a dependency map
→ Keep it shallow.

❌ System docs start naming features
→ You’ve inverted authority.

❌ Bidirectional syncing
→ Guaranteed drift.

❌ Overlinking
→ Links are warnings, not references.

12. Hard constraint to protect you
Max 5 anchors per feature.

If you need more:

Feature is too broad

Or system docs are too fragmented

Either way, that’s a design smell.

13. The payoff (why this works)
You can change features freely

Systems remain legible

Decisions stay historical

Agents know where truth lives

Drift becomes visible instead of silent

If you want next, we can:

Audit one of your real features and place anchors correctly

Design a diff-based “feature changed → anchor review” checklist

Simplify your dev docs further by killing overlap

Say the word.

Je zei:
GIve me an example on how a feature document would look like 
ChatGPT zei:
Perfect. I’ll give you a realistic, repo-ready Feature Canon example — not a template full of fluff, but something you could actually commit and live with.

I’ll also annotate why each part exists and what I’d cut if it started to bloat.

Example Feature Canon
File:
/docs/features/F001-smart-suggestions.md

Feature: Smart Suggestions
Status: 🟡 Partial
Owner: Feature Steward
Last reviewed: 2026-01-14

1. Intent
Help users quickly decide what to do next in a city without planning, by surfacing context-aware activity suggestions.

This feature exists to reduce decision fatigue during a trip.

Why this section exists:
If this paragraph ever stops being true, the feature should be deleted or redesigned.

2. Capabilities (What it CAN do)
Suggest up to 5 nearby activities based on:

User preferences (if available)

Time of day

Location radius

Refresh suggestions on manual user action (“Refresh”)

Prioritize open venues when opening hours are known

Display a short explanation for each suggestion (“Why this?”)

Capabilities are observable behavior — not internal logic.

3. Constraints (What it deliberately does NOT do)
Does not auto-refresh in the background

Does not guarantee relevance when user preferences are missing

Does not optimize for price or availability

Does not persist dismissed suggestions across sessions

If this list grows too long → feature scope is wrong.

4. Inputs
User location (approximate)

Current time

Optional user preference tags

City context (active city only)

No validation rules here. Just what flows in.

5. Outputs
A ranked list of activity cards

Each card includes:

Title

Category

Distance (approximate)

Short explanation

This is user-visible output, not UI layout.

6. Edge Behavior
If location permission is denied:

Fallback to city center suggestions

If no preferences exist:

Use popularity-based defaults

If no venues are available:

Show empty state with retry option

This prevents “undefined behavior” bugs.

7. Feature Relationships
Depends on

F002 User Preferences

F005 Location Context

Enhances

F003 Daily Itinerary

Conflicts with

None

Shared State

user.preferences

trip.context

This is the compatibility layer — no prose, no logic.

8. Technical Anchors
System Constraints

auth-model.md (guest vs logged-in access)

data-model.md (activity, preference entities)

Relevant Decisions

ADR-004 (recommendation scoring approach)

Volatile Notes

frontend-notes.md (card reuse patterns)

Anchors = “read this before touching code”.

9. Current Limitations / Known Issues
Suggestions may repeat across refreshes

Explanation text can be vague in low-data contexts

This section is optional but extremely practical.

10. Definition of Done
This feature is considered stable when:

At least 80% of suggestions are clicked or dismissed

Empty state occurs in <5% of sessions

Feature Canon matches observable behavior

Yes — the doc defines its own exit criteria.

Why this works (and what to resist)
What this document is
A behavioral contract

A change impact surface

A truth snapshot

What this document is NOT
A spec

A design doc

A system explanation

A future roadmap

If you add any of those, you’re corrupting it.

Size check (important)
This entire example is:

~250–300 lines max

Readable in 5 minutes

Diffable in Git

Cheap to update

That’s the point.

How agents interact with this doc
Developer agent

Reads sections 2–6

Architect agent

Reads sections 7–8

Quality reviewer

Verifies section 2 vs actual behavior

Feature Steward

Owns edits after changes

No one else touches it.

If you want next, we can:

Convert one of your real features into this format

Decide which of your existing docs are secretly trying to be Feature Canons

Create a pre-commit checklist so canon drift is caught early

Just tell me.

Je zei:
Can you create me a template (and only the template so I can make Claude Code understand the template & how it is structured. 
ChatGPT zei:
Below is ONLY the template, no explanations, no commentary.
This is designed to be machine-readable, diff-friendly, and consistent for Claude Code.

You can drop this directly into your repo.

# Feature: <FEATURE_NAME>

**Feature ID:** <FXXX>
**Status:** 🟢 Stable | 🟡 Partial | 🔴 Experimental
**Owner:** Feature Steward
**Last Reviewed:** <YYYY-MM-DD>

---

## 1. Intent

<Why this feature exists. One short paragraph.>

---

## 2. Capabilities

- <Observable behavior 1>
- <Observable behavior 2>
- <Observable behavior 3>

---

## 3. Constraints

- <Deliberate non-goal or limitation 1>
- <Deliberate non-goal or limitation 2>

---

## 4. Inputs

- <Input source 1>
- <Input source 2>

---

## 5. Outputs

- <User-visible output 1>
- <User-visible output 2>

---

## 6. Edge Behavior

- <Condition> → <Behavior>
- <Condition> → <Behavior>

---

## 7. Feature Relationships

### Depends on
- <FXXX Feature Name>

### Enhances
- <FXXX Feature Name>

### Conflicts with
- <FXXX Feature Name> | None

### Shared State
- <state.key>
- <state.key>

---

## 8. Technical Anchors

### System Constraints
- <path/to/system-doc.md>

### Relevant Decisions
- <ADR-XXX>

### Volatile Notes
- <path/to/notes-doc.md>

---

## 9. Known Limitations

- <Known issue or limitation>
- <Known issue or limitation>

---

## 10. Definition of Done

- <Measurable completion condition>
- <Measurable completion condition>
Je zei:
Can you give me the entire template for the development docs that you described earlier with the rules  for this document - The why this works (and what to resist) & size check & how agents interact with doc 
I need to copy this so that Claude Code can understand this
ChatGPT zei:
Below is ONLY the template, structured so Claude Code can reliably parse intent, authority, update rules, and agent ownership.

This is a meta-template you copy for each development document.
No explanations outside the template.

# <DOCUMENT TITLE>

**Document Type:** System | Decision | Notes  
**Authority Level:** High | Medium | Low  
**Owner:** System Archivist  
**Last Reviewed:** <YYYY-MM-DD>

---

## 1. Purpose

<Why this document exists.
What kind of knowledge it preserves.
What problem it prevents.>

---

## 2. Scope

### In Scope
- <What this document explicitly covers>
- <Boundaries of responsibility>

### Out of Scope
- <What this document will NOT describe>
- <What belongs in Feature Canon or code>

---

## 3. Context (Optional)

<Relevant background needed to understand this document.
Keep factual and concise.>

---

## 4. Core Content

<This section varies by document type>

### For SYSTEM documents
- System boundaries
- Conceptual architecture
- Invariants and constraints
- Contracts between components

### For DECISION documents (ADR)
- Decision statement
- Alternatives considered
- Chosen option
- Consequences (positive and negative)

### For NOTES documents
- Observations
- Heuristics
- Temporary conclusions
- Open questions

---

## 5. Constraints & Invariants

- <Rule that must always hold>
- <Assumption the system relies on>

---

## 6. Change Policy

This document MUST be updated when:
- <Structural or irreversible change condition>

This document MUST NOT be updated when:
- <UI behavior changes>
- <Feature logic evolves without system impact>

---

## 7. Links & References

### Related Feature Canons
- <FXXX Feature Name> (if applicable)

### Related Decisions
- <ADR-XXX>

### Related System Docs
- <path/to/system-doc.md>

---

## 8. Risks & Failure Modes (Optional)

- <What breaks if this document is ignored?>
- <Known danger zones>

---

## 9. Document Status

- 🟢 Stable
- 🟡 Requires Review
- 🔴 Potentially Outdated

---

## 10. Why This Document Works (and What to Resist)

### Why this works
- <What kind of clarity this document provides>
- <What cost it avoids>

### What to resist
- <Common misuse or over-extension>
- <Content that does not belong here>

---

## 11. Size & Readability Check

- Target length: <X–Y lines>
- One concept per section
- Diagrams preferred over prose
- Bullet points over paragraphs

---

## 12. Agent Interaction Rules

### System Archivist
- Owns creation and updates
- Ensures consistency with system reality

### Feature Steward
- May reference this document
- Must not modify core content

### Developer / UI / API Agents
- Read-only access
- Must not update this document

### Quality Reviewer
- Flags contradictions or missing updates
- Does not edit directly
OPTIONAL: ADR-SPECIFIC HEADER (use only for Decision docs)
## Decision Summary

**ADR ID:** ADR-XXX  
**Decision Date:** <YYYY-MM-DD>  
**Status:** Accepted | Superseded | Deprecated
This template is intentionally rigid.
If you want, next we can:

Classify your existing 15 dev docs into System / Decision / Notes using this template

Create a repo-level README that explains how all docs relate

Add a pre-commit checklist enforcing doc ownership rules

Just tell me.

Je zei:
Can you tell me how we should best setup the phases documents with the multiple deliverables in each and grouping? 
Tell me how we should group, how they interact with features & with development docs (System, ADR, Notes). 
How everything changes if features are changed? and in return how features should be changed? 
Give me also the template for the phases document & the do's & don't (rules) for the phases document
ChatGPT zei:
Good — this is the last structural layer you need. If phases are wrong, everything else gets brittle.

I’ll do this in four parts, in order:

What a Phase actually is (and is not)

How to group deliverables inside a phase

How phases interact with Features & Dev Docs (and how change propagates)

ONE copy-pasteable Phase Document template + rules

No fluff. This is repo- and Claude-Code–ready.

1. What a Phase actually is (critical redefinition)
A Phase is:
A coherent slice of progress that proves or stabilizes something important.

A Phase is NOT:
A feature list

A sprint

A milestone

A backlog dump

If a phase can be described as “build X, Y, Z”, it’s wrong.

2. The correct axis for Phases (this fixes grouping)
Phases should be grouped by intent, not by system area.

Valid phase intents
Prove viability

Reduce uncertainty

Stabilize behavior

Enable scale

Remove risk

Prepare launch

Invalid phase intents
“Frontend”

“API”

“Database”

“UI polish”

Those are deliverable dimensions, not phase goals.

3. Deliverables: how to group them inside a phase
Each phase contains 3–9 deliverables max.

Each deliverable must satisfy all 3:

Produces observable change

Ties to ≥1 Feature Canon

Has a clear verification step

Deliverable structure
A deliverable is:

“One outcome, many tasks.”

Example:

❌ “Build recommendation API”

✅ “Users receive ranked suggestions under normal conditions”

4. How Phases interact with Feature Canon (this is the spine)
Rule 1 — Phases NEVER define features
They reference Feature Canons.

Phases answer:

“Which features are we advancing, and how?”

Rule 2 — Feature Canon defines authority
If a Phase contradicts a Feature Canon:

Phase is wrong

Or Feature Canon must be explicitly updated

No silent divergence.

Rule 3 — Feature change triggers phase review
Any Feature Canon change must answer:

Does this invalidate a current phase?

Does this create a new deliverable?

Does this move scope to another phase?

5. How Phases interact with Dev Docs (System / ADR / Notes)
System Docs
Phases may not rewrite system structure

If a phase requires system change → create or update:

System doc (if structural)

ADR (if decision-based)

Phases trigger documentation, they don’t contain it.

ADRs
ADRs may be:

Created during a phase

Referenced by a phase

ADRs are immutable once accepted

A phase may depend on an ADR being accepted.

Notes
Notes are allowed to be phase-scoped

Notes may be referenced

Notes never gate completion

6. What happens when FEATURES change (important)
When a Feature Canon changes:
Feature Steward updates Canon

Impact review:

Which phases reference this feature?

For each impacted phase:

Deliverable still valid? → keep

Deliverable partially invalid? → revise

Deliverable invalid? → remove or move

No automatic rewriting. Explicit impact review only.

7. What happens when PHASES change
Phases may change freely as long as they don’t lie.

If a phase changes:

Feature Canon stays authoritative

Dev Docs stay untouched

Only phase deliverables and goals change

Phases are plans.
Features are truth.

8. Direction of authority (memorize this)
System Docs & ADRs  → constraints
Feature Canon       → truth
Phase Docs          → intent & sequencing
Deliverables        → execution targets
Never invert this.

9. Phase Document Template (COPY THIS)
# Phase: <PHASE NAME>

**Phase ID:** P-XX  
**Status:** Planned | Active | Completed | Deprecated  
**Owner:** Architect Agent  
**Last Reviewed:** <YYYY-MM-DD>

---

## 1. Phase Intent

<What this phase exists to prove, reduce, or stabilize.
One short paragraph.>

---

## 2. Success Criteria

This phase is successful when:
- <Observable outcome 1>
- <Observable outcome 2>

---

## 3. In-Scope Features

This phase advances the following Feature Canons:
- <FXXX Feature Name>
- <FXXX Feature Name>

---

## 4. Out-of-Scope (Explicit)

This phase does NOT attempt to:
- <Explicit exclusion>
- <Explicit exclusion>

---

## 5. Deliverables

### D1 — <Deliverable Name>
**Outcome:** <Observable result>
**Related Features:** <FXXX>
**Verification:** <How this is validated>

---

### D2 — <Deliverable Name>
**Outcome:** <Observable result>
**Related Features:** <FXXX>
**Verification:** <How this is validated>

---

## 6. Dependencies & Preconditions

- Required ADRs:
  - <ADR-XXX>
- Required System Constraints:
  - <system-doc.md>
- Blocking external factors:
  - <If any>

---

## 7. Risks & Unknowns

- <Known risk or uncertainty>
- <Assumption being tested>

---

## 8. Change Log

- <YYYY-MM-DD> — <What changed and why>

---

## 9. Interaction Rules

- This phase MUST NOT redefine feature behavior
- Feature Canon is authoritative
- System changes require ADR or System Doc update

---

## 10. Phase Completion Checklist

- [ ] All deliverables verified
- [ ] Feature Canons still accurate
- [ ] Required ADRs accepted
- [ ] Phase marked Completed or Deprecated
10. Do’s & Don’ts for Phase Documents (rules)
DO
Group by intent, not tech

Keep deliverables outcome-focused

Reference features by ID

Explicitly exclude scope

Kill or deprecate phases without guilt

DON’T
Describe implementation steps

Duplicate feature behavior

Embed architecture explanations

Track tasks or subtasks

Pretend plans are truth

11. Critical reflection (on my advice)
Where this could fail for you:

If you over-document phases → they become fake control

If agents treat phases as commands → rigidity

If you never deprecate phases → historical clutter

Phases are tools for thinking, not governance.

12. What I’d do next (if I were you)
Rewrite ONE existing phase using this template

Map it to real Feature Canons

Kill at least one deliverable that doesn’t map cleanly

Run one iteration end-to-end

If you want, next we can:

Refactor one of your real phases live

Redesign your agent orchestration around phases

Create a repo-level “How work flows” doc