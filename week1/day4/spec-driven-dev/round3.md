# Duplicate Ticket Merge Brief

## Why
Customers sometimes open a second ticket when their first issue has not been answered quickly enough. Support needs a manual merge action so duplicates stay connected.

## What
A duplicate merge is allowed only when both tickets belong to the same `customer_id` and neither ticket is closed. The system does not auto-detect duplicates; a person reviews the tickets and triggers the merge.

When merged:
- The older ticket becomes the primary ticket.
- The newer ticket is marked `closed`.
- The newer ticket records that it was merged into the older ticket.
- The older ticket gets a merge note saying what newer ticket was merged into this older one.
- The older ticket priority becomes `Urgent` if either ticket is urgent.

If tickets have different `customer_id` values, the merge must fail. If either ticket is closed, the merge must fail. Exact text matching is out of scope.

## Context
This fits into the existing small Python model in `tickets.py`. `Ticket` already has `id`, `customer`, `subject`, `priority`, `status`, timestamps, and `closed_by`.

The implementation should add:
- `customer_id` to `Ticket`
- merge audit fields on tickets
- a merge function in `tickets.py`
- focused tests for allowed and blocked merges

## Constraints
Do not auto-merge tickets. Do not merge tickets across customers. Do not merge anything involving a closed ticket. Do not delete the duplicate ticket. Do not use fuzzy text matching or similarity scoring in v1.

## Tasks

1. Update `Ticket` in `tickets.py` with `customer_id`, `merged_into`, and `merge_notes`.
   Verify sample tickets load successfully and every sample ticket has a stable customer id.

2. Add `merge_duplicate_tickets(tickets, merged_by)` behavior that finds the older and newer ticket automatically.
   Verify the older ticket remains open, the newer ticket is closed, and the newer ticket points to the older ticket.

3. Add validation for blocked merges.
   Verify different customer ids fail, closed tickets fail, and missing ticket ids fail without changing either ticket.

4. Add priority, deadline, and audit-note updates.
   Verify urgent priority is preserved/escalated, the earlier deadline wins, and the primary ticket receives exactly one merge note.

## Done
A support agent can manually merge two reviewed duplicate open tickets from the same customer, preserving both records and leaving a clear audit trail of what was merged, by whom, and into which primary ticket.
