# Planned Wavelink HR packages — website 3.1.0

Proposed product scope requested by Adriano on 4 October 2026. This document is a roadmap, not a delivery or availability announcement. Website packages are optional and separate from the current operations platform. Commercial terms and release dates remain unconfirmed.

## Proposed packages

| Package | Intended workflow | Useful additions |
| --- | --- | --- |
| Crew & Rotations | Plan an assignment, confirm joining, record embarkation, coordinate relief and record leaving | Vessel rosters; onboard/ashore/upcoming personnel; planned vs actual dates; rotation calendars; leave and availability; relief assignments; joining instructions |
| Timesheets & Approvals | Draft a period, submit it, review it, return corrections and export an approved period | Vessel/project allocation; configurable work/travel/training/standby categories; reviewer assignment; period summaries; correction history |
| Travel & Expenses | Prepare a journey, submit receipts and claims, review costs and record reimbursement status | Joining itineraries; expense categories; currency recording; vessel/project allocation; receipt attachments; finance exports |
| People & Readiness | Maintain role/training information, identify outstanding preparation and review assignment readiness | Skills and role records; training/certificate validity; renewal reminders; onboarding and preparation checklists; missing-document follow-up |

## Integration principles for later application development

- Reuse named company membership and reviewed access roles; limit personnel and finance records to appropriate HR/coordinator/reviewer roles.
- Connect assignments to the existing vessel/site and department records without replacing current daily handover workflows.
- Separate planned assignments from confirmed dates and actual embarkation/leaving records.
- Preserve personal drafts, explicit submission, reviewer feedback and correction history.
- Keep finance exports and recorded reimbursement statuses distinct from executing payroll or payments.
- Support human readiness decisions; validity reminders do not certify competence or medical fitness.
- Define storage, retention, permissions and employee access before introducing real personnel records. Do not place private HR details in general Team posts or public crew displays.
- Confirm hosted/local behavior and exports during each package's implementation; do not promise unbuilt integrations or automatic cross-deployment synchronisation.

## Suggested delivery order

1. Crew & Rotations: shared onboard/ashore/upcoming view and planned/confirmed crew changes.
2. Timesheets & Approvals: clear period submission, review and exports.
3. Travel & Expenses: receipts, review and assignment cost allocation.
4. People & Readiness: personnel records, renewal attention and assignment preparation.

This is a suggested sequence only. Priorities should be agreed with company users, and each package should be implemented and accepted before its website label changes from planned to available.

## Website boundaries

The website shows four planned packages and a fictional rotation concept. It accepts no timesheets, receipts, personnel records or uploads. Its enquiry button opens an email draft to comercial@mywavelink.com. No package application code, database, login controls, HR records, payroll, payment execution, accounting integration or live hosting settings were changed for this release.
