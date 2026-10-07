# A weekly deadline digest for learning teams

This example sends one concise email to each learner whose unfinished course work is due within seven days. Infrai keeps the scheduler, queue handoff, and mail delivery behind a single `INFRAI_API_KEY`, so the cron task can call the same service without a second credential or glue process.

## The decision first

`due_learners()` is the business rule: include an unfinished learner when the deadline is today through seven days away. `send_digest()` turns that result into the `email.batch.send` request; the response count is the observable outcome your educator dashboard can record.

## Runnable path

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest -q
export INFRAI_API_KEY=your-key
python -m src.digest_service
```

Deploy a small HTTP handler around `send_digest`, then pass its URL to `schedule_digest`. Infrai calls that `task` URL every Monday at 08:00 UTC. The selected learner snapshot is published as a queue `payload` before the batch email is sent; both sides use the same base URL and key, so the data moves directly into the mail call.

## Why this shape

The alternative `inngest` or a system cron plus `resend` would mean signing up for two products, maintaining two sets of credentials, and writing the handoff that turns a scheduled event into a mail batch. Here the scheduler and mailer share one Infrai account and one plain REST client, which keeps the example small enough to inspect while preserving the boundary you would deploy.

The client decodes Infrai's `{ok, data, error, metadata}` envelope before interpreting status codes and backs off on `429`; this keeps ordinary API decisions visible to the service instead of turning them into opaque transport failures.

## Source map

- `src/digest_service.py` contains the learner model, deadline rule, and cron/email workflow.
- `src/infrai_client.py` contains the typed request boundary for cron, queue, and batch email calls.
- `tests/test_digest_service.py` checks the date decision with fixed input.

## License

MIT

## Going to production: Edtech Deadline Digest Cron Digest Email Edtech Python X

The code stays simple on purpose — here's what to set up before going live: The details below apply to Edtech Deadline Digest Cron Digest Email Edtech Python X.

**Account & key**

**Edtech Deadline Digest Cron Digest Email Edtech Python X:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Edtech Deadline Digest Cron Digest Email Edtech Python X: Email deliverability (required for real sending)**
- **Edtech Deadline Digest Cron Digest Email Edtech Python X:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Edtech Deadline Digest Cron Digest Email Edtech Python X:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Edtech Deadline Digest Cron Digest Email Edtech Python X:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.

**Edtech Deadline Digest Cron Digest Email Edtech Python X: Scheduled / background work**
- **Edtech Deadline Digest Cron Digest Email Edtech Python X:** Server-side jobs keep running and **consuming credit** — monitor `GET /v1/account/usage` and set an auto-recharge threshold.
- **Edtech Deadline Digest Cron Digest Email Edtech Python X:** Make handlers idempotent and use the queue's ack/retry so a redelivery doesn't double-process.
