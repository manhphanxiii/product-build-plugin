# Principles

Read this file when the user asks why the workspace has this structure.

## Treat the model like a new employee

A capable new employee still needs a place to work, verified context, a clear task, a quality gate, and explicit authority limits.
The repository structure supplies those conditions so the model does not have to guess.

## Keep one source of truth per fact

Duplication is the main failure mode in a repository used by several agents.
If one rule exists in two files, one copy will eventually be stale and nobody will know which one to trust.
Keep working rules in `AGENTS.md`, product truth in `prd/concept.md`, quality criteria in `prd/evals/checklist.md`, and architecture in `prd/architecture.md`.
Link instead of copying.

## Customer language outranks internal phrasing

Founders and customers rarely describe a problem with the same vocabulary.
Keep objections, complaints, and problem names verbatim in `client-note/` so product decisions and copy can use the language customers actually use.
An empty `client-note/` means the repository is operating on assumptions, and the user should be told plainly.

## Repeated prompts should become skills

The third repetition is the clearest signal that instructions need a stable, improvable home.
Repeated ad hoc prompts drift even when they appear faster in the moment.

## Parallel sessions are separate people

Give each concurrent session its own task, output location, and isolated changes.
Useful parallelism comes from selecting a few independent threads, not maximizing session count.

## Begin with tight permissions

Use conservative permissions, plans for large or behavior-changing work, and manual review while the repository is learning its standards.
Loosen permissions only after `prd/evals/checklist.md` has caught real problems and the evidence base is reliable.

## The repository compounds

Roadmap evidence, review standards, customer language, and routines create context that another user of the same model does not have.
The system is never finished because every escaped defect should strengthen `prd/evals/checklist.md` and every valuable customer phrase should strengthen `client-note/`.

## Wrap instead of rebuilding

A running application is evidence, not technical debt that must be reorganized before product work can begin.
The product repository adds a decision and quality layer around the existing application without forcing its code to move.
