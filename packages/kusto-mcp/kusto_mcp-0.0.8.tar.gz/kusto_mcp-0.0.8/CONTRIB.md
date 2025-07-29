# CONTRIBUTING

## Style
- **PEP 8 + PEP 257** by default.  
- **Naming**
  - Functions & variables → `snake_case`
  - Constants → `UPPER_CASE`
  - Classes & exceptions → `CamelCase`
  - Private symbols → prefix with `_`
- Max line length = 88 chars (Black default).

## Tooling
- **Black** is the source of truth: run `black .` before every commit.
- CI also runs `flake8` & `isort`; keep them clean.

## Typing
- Full **PEP 484** type annotations are required on all new or modified code.
- Pass `mypy --strict`; avoid `Any` unless there’s no alternative.

## Tests
- Use **pytest**; cover every new path or bug fix.
- Keep unit tests fast; long-running tests go in `tests/integration/`.

## Git & PRs
- Branch from `main`; use flat branch names like `add_feature_a` or `fix_bug_b`
- Make small, focused PRs with clear descriptions.
- Run copilot code review before submitting.

Thanks for contributing! 🙌
