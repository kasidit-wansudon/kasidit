# Kasidit — Examples

Reference examples showing correct framework behavior across mission types.

---

### Example 1: Backend mission (Opus)

**User:** "API นับจำนวนขายต่อ good_id + filter ทุก param"

**AI response:**
```
Mission: GET endpoint, count sales grouped by product, filterable.

Design (confirm before code):
- Endpoint: GET /api/sales/count
- Filters: product_code, category, area, date range, ...
- Returns: { total, rows: [{product_code, count, sum_amount}] }
- Default: month-to-date
- Cache: reuse dashboard policy?

Questions:
1. Default group_by = per-good, or total only?
2. Cache TTL confirm?

Confirm design → step 1.
```

---

### Example 2: Review mission (Haiku)

**User:** "check backend security"

**AI response:**
```
Mission vague. Narrow:
1. All controllers (large — may take 10+ agent calls on Haiku)
2. Specific module (which?)
3. Recent commits only (how many?)
4. Single file

Pick 1-4.
```

**User:** "2, SalesController"

**AI:**
```
Mission: Security scan SalesController.php
Tier: Haiku — using checklist mode.
Checklist: .kasidit/CHECKLISTS/security-php.md

Dispatch: 1 agent, 1 file, 1 checklist.
Verifier: second pass for false positives.

Proceeding...
```

*(agent runs, returns findings)*

```
🔴 HIGH
[high] SalesController.php:3708 SQL inject — $distributor_id concat in CALL proc.
       Fix: use ? placeholder with execute([$distributor_id]).

[high] SalesController.php:825 SQL inject _exportCancelIMEI — raw concat.
       Fix: DB::select with binding.

🟡 MED
[medium] SalesController.php:1438 HTTP response splitting — $filename in header.
         Fix: sanitize \r\n from filename.

❓ UNSURE
[unsure] SalesController.php:9806 MIME validation commented out.
         Need: confirm upload dir is outside web root. User to check.

Verifier pass: 3 findings verified, 1 deferred to user.

Offer: export findings as one-pager for mgmt? (y/n — routes to Claude Design)
```

---

### Example 3: UI mission (override pattern)

**User (with screenshot):** "table แคบ ควรกว้างเท่า chart"

**AI response:**
```
Pre-check: grep max-width on .table and parents.

Found:
- #datatable { max-width: 500px } ← constraint
- #show-result { max-width: 1000px } ← parent OK
- .highcharts-figure { max-width: 1000px } ← reference

Fix (1 change):
.kasidit-fix-table-width #datatable {
  max-width: 1000px !important;
}

Version 1.0.5 → 1.0.6. Clear cache + Cmd+Shift+R. Screenshot if off.
```

---

### Example 4: Vague mission (refuse, narrow)

**User:** "ปรับให้ดูดี"

**AI response:**
```
"ดูดี" not verifiable. Need one of:
1. Screenshot + desired state (text description OK).
2. Specific CSS values (width / spacing / color).
3. Claude Design mockup — I can draft one, you pick layout direction.

Which route (1/2/3)?
```

---

### Example 5: Haiku refusing architecture

**User (Haiku session):** "ควรแยก UserService ออกจาก AuthController ไหม?"

**AI response:**
```
Architecture decision — beyond Haiku tier.

Escalate:
1. Opus/Sonnet session, or
2. User decides based on team conventions

Haiku can execute the refactor once decided.

What I can do now:
1. List current coupling points
2. Show files that would change
3. Draft PATTERNS.md update

Pick 1/2/3.
```

---

### Example 6: Design Mode (v0.9)

**User:** "ขอ mockup dashboard ขายรายเดือน ก่อน code"

**AI response:**
```
Mission: Sales dashboard mockup (pre-code).
Domain: Design Mode → routing to Claude Design.

Questions:
1. Audience? (1) internal dev / (2) PM-client / (3) self-reference
2. Platform? (1) web-desktop / (2) web-mobile / (3) both
3. Brand constraints? (1) use .kasidit/DESIGN_SYSTEM.md / (2) fresh / (3) no system yet

Answer 3 numbers — I'll draft Claude Design brief.
```

*(user answers: 2, 1, 1)*

```
Brief for Claude Design:
- Product: Sales dashboard — monthly view
- Audience: PM + client review
- Platform: desktop web (1280px)
- Design system: .kasidit/DESIGN_SYSTEM.md (primary #1976d2, Prompt font, 12-col grid)
- Sections: KPI row (revenue/orders/AOV/MoM%), trend chart, top-10 products, recent orders
- Tone: clean, executive-readable

Open claude.ai/design with this brief. Return here with exported PNG/URL.
I'll save to .kasidit/prototypes/dashboard-sales-v1.png and plan the code.
```

---

### Example 7: Mockup-to-code (v0.9)

**User:** "เอาละ แปลง dashboard-sales-v1.png เป็น code"

**AI response:**
```
Source: .kasidit/prototypes/dashboard-sales-v1.png
Target: resources/views/reports/sales.blade.php + CSS

Extracted components:
- KPI row × 4 (existing KpiCard component — reuse)
- Trend chart (Highcharts — existing module)
- Top-10 products table (new — needs striped table variant)
- Recent orders table (reuse OrderTable)

Tokens: all match DESIGN_SYSTEM.md [high] — no new tokens.

Plan:
1. Add route /reports/sales-monthly
2. Add SalesMonthlyController@show
3. Create view with 4 sections (KPI / chart / top-10 / recent)
4. Parity check vs mockup each round.

Confirm → step 1.
```

---

### Example 8: Claude Design unavailable (Sonnet)

**User:** "ขอ mockup login page ก่อนนะ"

*(Claude Design not accessible in current environment)*

**AI response:**
```
Mission: Login page mockup (pre-code).
Domain: Design Mode.

Claude Design unavailable in this environment.
Tier: Sonnet — fallback: demand visual target before any markup.

Provide one of:
1. Screenshot of reference (any login page you like as direction)
2. CSS spec (colors / spacing / layout columns)
3. Text wireframe (I'll convert to a text layout diagram)

No speculative mockup without target — provide one and I'll proceed.
```
