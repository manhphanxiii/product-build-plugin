# Eval Set Format

Start `prd/evals/cases.md` with the active gate:

```md
# Eval Cases

## Ship gate

- Pass rate: at least 90 percent
- Critical failures: 0
- Pass-to-fail regressions: 0
```

Represent every case with stable fields:

```yaml
- id: EVAL-001
  input: <representative product input or scenario>
  must:
    - <required observable behavior>
  must_not:
    - <forbidden observable behavior>
  source: <PRD user story, prototype fixture, or permanent regression source>
  added: YYYY-MM-DD
  critical: false
```

Append one row per complete run to `prd/evals/results.md`:

```md
| Run | Date | Version | Passed | Total | Rate | Critical failures | Regressions | Gate | Evidence |
|---|---|---|---|---|---|---|---|---|---|
```

Keep failed runs.
Never reuse an ID for a different behavior.
