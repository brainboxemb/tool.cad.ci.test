# Targeted selection live fixture

Status: current

This synthetic pair exists only to black-box qualify the released reusable
workflow selectors. It is deliberately outside `acceptance_suite/**`.

- `targeted-a` is the positive probe.
- `targeted-b` may be configured to fail during the single-item gate so an
  accidental broad selection is observable.

Both use the same domain-neutral marker builder. Selection must come from the
released workflow input; do not toggle `process` to stage this fixture.
