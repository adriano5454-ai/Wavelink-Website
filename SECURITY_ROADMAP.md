# Security and company access — website messaging checkpoint

Website release **2.3.0**, prepared 26 September 2026 (UTC).

## What the user requested

Present Wavelink attractively to companies; emphasise collaboration and security; show future two-step verification and access through corporate email. These are product intentions, not permission to assert completed implementation or certification.

## Claims published in this release

| Area | Website treatment | Evidence boundary |
| --- | --- | --- |
| Users, roles, departments and vessel-specific controls where supported | Product capability | Retained from the supplied website lineage/product scope; module-specific access must be confirmed. Not independently re-audited in application source here. |
| Authorship, review, acknowledgement and approval responsibilities | Product capability | Relevant workflow scope; not an immutable or tamper-evident audit-log claim. |
| Two-step verification | **Planned protection / Future release** | No implementation or deployment verification in this website task. |
| Company-email sign-in with administrator-managed onboarding | **Planned company access / Future release** | Describes intended company access; does not establish domain verification, identity-provider federation or directory provisioning. |
| Corporate SSO / identity-provider integration | Requirements discussion | Not represented as an implemented or committed provider integration. |
| Hosting, data handling, backup and recovery | IT rollout discussion | No blanket technical guarantee, retention policy, location or recovery objective invented. |

No release dates or providers are promised. The public demo is not presented as having planned protections. Website labels should change only when an application release provides evidence of implementation, testing and deployment configuration.

## Future engineering acceptance questions

These are proposed implementation-review questions, not implemented features:

1. **Second-factor policy:** Which verification method will be supported? Can an organisation require it for administrators or all users? How are enrolment, recovery, revoked devices, failed attempts and session invalidation handled and tested? Avoid claiming that all two-step methods are phishing-resistant.
2. **Company email:** How is an address verified? Who can invite, approve or deactivate members? Is organisation/domain ownership established securely? An email suffix alone must not grant access to a company workspace.
3. **Federated identity:** Is corporate SSO actually required? Select and validate the protocol/provider, identity-to-user mapping, account linking, administrator recovery and sign-out behaviour before naming a supported integration. A work-email username is not SSO.
4. **Authorisation:** Verify project, vessel, department, module, action and private-record boundaries server-side, including exported records and attachments. Preserve the existing named-admin and public-demo gateway boundaries.
5. **Data and deployment:** Establish transport security, storage protections, secrets handling, backups, restore testing, logging, retention, updates and incident handling for the chosen hosted/local deployment. Do not infer these controls from attractive website copy.
6. **Acceptance evidence:** Record the exact application version, tests, configuration requirements and limitations. Separate prepared code, tested behaviour and deployed protection. Review website wording against that evidence before removing a Planned label.

## Public-site data boundary

The static website contains no account form, login field, credential collection, analytics, API requests or browser storage. Contact is via the user's email application; the copy action writes only the displayed address after an explicit click. Hosting logs and the separate demo are outside the marketing code's scope.

No customer security policy, secret, identity-provider configuration or genuine operational record belongs in this public repository.

## Development priority boundary

This document is a future security checkpoint. It does not change the agreed application development sequence or claim that the handover-priority development branch has received security changes. Coordinate implementation with the separate application workstream.
