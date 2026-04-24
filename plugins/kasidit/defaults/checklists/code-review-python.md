# Python Code Review Checklist

Use during `/kasi-review` on Python modules. Focus: readability, correctness, PEP 8 / typing alignment.

## Correctness
- [ ] Bare `except:` or `except Exception:` swallowing errors — narrow to specific exception?
- [ ] Mutable default arg (`def f(x=[])` / `={}`) — use `None` + init inside body?
- [ ] `is` vs `==` on values (not `None` / singletons) — switch to `==`?
- [ ] `global` statement used — refactor to pass state / class attr?

## API / Typing
- [ ] Public function missing type hints — add annotations on args + return?
- [ ] `*args` / `**kwargs` hides real signature on public API — spell out params or use `Protocol`?
- [ ] Public function / class missing docstring — add one-line purpose + args?

## Structure
- [ ] Circular import between modules — break via local import / extract shared module?
- [ ] `sys.path` manipulation at runtime — fix packaging instead?
- [ ] `__init__.py` runs heavy side effects on import — move to explicit init function?
- [ ] Script missing `if __name__ == "__main__":` guard — add it?
- [ ] `from x import *` at module top — list explicit names?
- [ ] Duplicate code block copy-pasted — extract helper?

## Logging
- [ ] `print()` for diagnostics — switch to `logging`?
- [ ] `logger.info(f"{x}")` eager-formats even when disabled — use `logger.info("%s", x)`?
