# Python Performance Checklist

Use during `/kasi-review perf` on suspected hot paths. Measure (`cProfile` / `timeit`) before you change.

## CPU / data structures
- [ ] CPU-bound work spread across `threading` — GIL caps it; use `multiprocessing` / `concurrent.futures.ProcessPoolExecutor`?
- [ ] `list.append` in tight loop with known size — preallocate or use `collections.deque`?
- [ ] `str` concatenation in loop (`s += part`) — build list + `"".join`?
- [ ] `if x in big_list:` in loop — convert to `set` / `frozenset` for O(1)?
- [ ] `__slots__` missing on class with millions of instances — add to cut memory?

## Compute reuse
- [ ] `re.compile` inside loop — hoist to module level?
- [ ] `copy.deepcopy` on data that is not mutated — drop or shallow copy?
- [ ] Eager `list(...)` / list comprehension where only iteration is needed — use generator expression?

## Pandas / numeric
- [ ] `df.iterrows()` in hot path — vectorize with column ops / `numpy`?
- [ ] `df.apply(func, axis=1)` on large frame — vectorize / `np.where` / `.loc` masking?

## IO / network / DB
- [ ] Django `.filter()` / `.get()` inside a loop — `select_related` / `prefetch_related`?
- [ ] File read via `f.read()` into memory on large file — stream line-by-line / chunked read?
- [ ] `requests.get` per call without `Session` / DB without connection pool — reuse pooled client?
- [ ] `json.dumps` on hot path — pass `ensure_ascii=False` + compact separators, or use `orjson`?

## Async
- [ ] `await` inside sync loop body / `asyncio.run` called per item — batch with `asyncio.gather`?
