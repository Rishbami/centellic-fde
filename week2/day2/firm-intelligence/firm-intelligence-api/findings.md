# Reports API review

## Verdict

The review found four behavioral problems involving availability, retry safety, HTTP
semantics, and data integrity. The highest-ranked problem is fixed; three remain.

## Ranked findings

### 1. Export blocks unrelated requests (highest severity, fixed)

`GET /reports/{report_id}/export` was declared `async`, but called `time.sleep(...)`.
That blocks the event loop, so one slow export delays unrelated requests handled by
the same worker. This is ranked first because it has API-wide blast radius and gets
worse under load.

Proof (run the export in the background, then time an unrelated health request):

```bash
curl -s http://127.0.0.1:8000/reports/1/export >/tmp/report-export.json &
sleep 0.2
curl -s -o /dev/null -w 'health_time=%{time_total}s status=%{http_code}\n' \
  http://127.0.0.1:8000/health
```

Observed with the original 3-second delay: `health_time=2.798567s status=200`. The
health endpoint should have returned immediately, but waited for the export to finish.

Recommended fix: use an awaitable operation for simulated asynchronous work. If PDF
generation is genuinely blocking or CPU-heavy, move it to a worker thread or job
queue rather than running it on the event loop.

Fixed by replacing the blocking `time.sleep(10)` with `await asyncio.sleep(10)`.
Running the same proof after the change produced
`health_time=0.001647s status=200`, while the export still returned the same response.
No path, method, response field, or status code changed.

### 2. PUT is not idempotent and creates false revisions

Sending the same `PUT /reports/1` twice appends a revision each time, even though the
requested report representation is identical. A client retry after a lost response
therefore records work that did not happen and corrupts revision history.

Proof:

```bash
curl -s -X PUT http://127.0.0.1:8000/reports/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"UK Market Outlook","firm_id":1}'
curl -s -X PUT http://127.0.0.1:8000/reports/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"UK Market Outlook","firm_id":1}'
```

Observed: the first response ended in `"v2"`; the identical retry ended in `"v3"`.

Recommended fix: only append a revision when persisted report data actually changes,
or redesign revision creation as an explicit operation. The latter would alter the
public contract and requires agreement with callers.

### 3. GET changes server state

`GET /reports/1` increments `views`. GET requests may be retried, prefetched, crawled,
or used by monitoring, so the value counts request executions rather than reliable
human views. A lost response followed by a retry increments it twice.

Proof:

```bash
curl -s http://127.0.0.1:8000/reports/1
curl -s http://127.0.0.1:8000/reports/1
```

Observed: `views` changed from `1` to `2` across two otherwise identical reads.

Recommended fix: record deduplicated analytics separately, using a request/session
identifier. Simply removing the counter may change the already-public response field,
so product and API consumers should agree on the migration.

### 4. Reports can reference firms that do not exist

Unlike the people router, report creation and update do not validate `firm_id`. This
allows orphaned report data and makes joins/lookups unreliable.

Proof:

```bash
curl -i -X POST http://127.0.0.1:8000/reports \
  -H 'Content-Type: application/json' \
  -d '{"title":"Invalid firm report","firm_id":999}'
```

Observed: `HTTP/1.1 201 Created` with `"firm_id":999`, although that firm does not
exist.

Recommended fix: validate `firm_id` on both create and update. Rejecting invalid input
would introduce a new error response for requests that currently succeed, so the
status code and rollout need to be communicated as a contract change.

## Deliberately not findings

- Not using `Depends` is a consistency/readability difference, not a demonstrated bug.
- A second DELETE returning `404` is not necessarily an idempotency violation: after
  either one or two calls, the resource remains deleted.
- POST itself is not required to be idempotent.

## Work completed

Finding 1 was fixed with a two-line diff: import `asyncio` instead of `time`, then await
the simulated export delay. Findings 2-4 were deliberately left unchanged.

## 60-second handover

> We found four problems, ranked by impact. First, report export blocked the async event
> loop and delayed unrelated requests. It ranked first because one caller could slow the
> entire API, and the effect would worsen under load. Second, identical PUT retries add
> false revisions. Third, GET changes state by incrementing views. Fourth, reports can
> reference firms that do not exist.
>
> We fixed number one by replacing the blocking `time.sleep(10)` with
> `await asyncio.sleep(10)`. The command below starts an export and times `/health` at
> the same time. Before the fix, health waited for the export; after the fix, it returned
> in 0.001647 seconds while the export continued. The public API contract did not change.
>
> We did not fix the other three. Number two needs idempotency tests and agreement on
> when revisions should be created. Number three needs a product decision and properly
> deduplicated analytics. Number four needs firm validation on create and update, plus
> agreement on the new error response because callers currently receive success.

Proof command:

```bash
curl -s http://127.0.0.1:8000/reports/1/export & curl -s http://127.0.0.1:8000/health; wait
```

Expected after the fix: `{"status":"ok"}` appears immediately, and the export response
appears about 10 seconds later. Before the fix, both responses appeared after the export
delay.

## API terms in plain English

### API contract

An API contract is the agreement between an API and the programs that use it. It says:

- which URLs and HTTP methods are available;
- what data callers must send;
- what data the API returns; and
- which status codes callers should expect.

For example, the reports contract currently says that a caller can send a `PUT` request
to `/reports/1` with `title` and `firm_id`, and receive the updated report in response.
Other teams may have written code that relies on those exact names and behaviours.

### Breaking change

A breaking change is a change that could stop existing callers from working. Examples
include renaming `firm_id`, removing `title`, changing `/reports` to `/documents`, making
a new field compulsory, or changing a status code that callers expect.

Adding a new optional field or a new endpoint is usually not breaking because existing
callers can continue doing what they already do.

### API versioning (`/v1/` and `/v2/`)

Versioning lets us introduce a different API contract without immediately breaking the
old one:

```text
/v1/reports
/v2/reports
```

Existing callers can keep using `/v1/reports`, while updated callers move to
`/v2/reports`. This gives teams time to update, but it also means the API team may need
to support both versions for a while.

### OpenAPI and Swagger UI

OpenAPI is a standard description of an API. It lists endpoints, request fields,
response fields, validation rules, and status codes. In FastAPI, the raw description is
normally available at:

```text
http://127.0.0.1:8000/openapi.json
```

Swagger UI turns that OpenAPI description into a readable, interactive webpage:

```text
http://127.0.0.1:8000/docs
```

Swagger does not change the Python implementation. We make changes in files such as
`reports.py`, then use Swagger to understand and test the API. Clicking **Execute** in
Swagger sends a real request; it is not a simulation. A POST can create real data and a
DELETE can delete real data.

### Backward compatibility

A change is backward compatible when existing callers continue working without changing
their code.

Usually backward compatible:

- adding a new optional response field;
- adding a new endpoint; or
- improving performance without changing the request or response.

Usually breaking:

- renaming or removing a field;
- changing a field's type;
- changing an endpoint path;
- making a new request field required; or
- changing an expected status code.

### How the terms connect

The **API contract** says what callers can expect. A **breaking change** violates one of
those existing expectations. **Backward compatibility** means preserving those
expectations so existing callers still work. **API versioning** lets a new contract run
alongside the old contract. **OpenAPI** records the contract, and **Swagger UI** makes it
easy for people to read and test.
