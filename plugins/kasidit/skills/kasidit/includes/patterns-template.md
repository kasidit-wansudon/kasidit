# Project Patterns

## Naming
- Controllers: PascalCase + "Controller" suffix
- Services: PascalCase + "Service" suffix
- DB columns: snake_case
- API routes: kebab-case

## Error handling
Use `try { } catch (Exception $e) { Log::error($e); throw; }`.
Never swallow exceptions silently.

## DB queries
Always use Eloquent or Query Builder. No raw SQL unless performance-critical.
If raw SQL: use `DB::select(?, [bindings])` with parameter binding.

## Controllers
Method order: public actions → private helpers.
Return JsonResponse, not array.

## Auth
Use `Auth::user()` inside controllers.
For middleware-level, use `$request->user()`.
