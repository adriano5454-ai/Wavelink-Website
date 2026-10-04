# Security and deployment wording — website 3.0.0

The 2.3.1 “Planned” labels for company-email sign-in and two-step verification are superseded by the current UI83–95 implementation.

| Capability | Current wording / boundary |
| --- | --- |
| Company membership | Controlled exact-email invitation, verification, department and reviewed role/access profile. |
| Email sign-in | Exact approved verified membership mailbox inside the already selected company service; User ID remains available. |
| Two-step verification | Optional member enrolment with authenticator TOTP, one-time recovery codes and session controls. |
| Sessions | Members may review and revoke their own active sessions. |
| Permissions | Module/current scope rules also apply to search and personal actions; no universal all-module vessel-isolation claim. |
| Email alerts | Optional summaries on a configured company service; user opt-in and provider delivery acceptance are separate. |
| QR visitors | Limited to the invited document/revision when deliberately enabled; self-declared visitors are distinguished from named members. |
| Public email-first company discovery | Separate future work, not part of the website. |
| Enterprise SSO / identity-provider integrations | Separate requirements; no provider integration promised. |
| Independent security certification | No audit, ISO/SOC certification, uptime or compliance guarantee claimed. |
| Hosted/local operation | Separate choices, commissioned for network, HTTPS, identity, mail, backup and recovery needs. |

The marketing site adds no authentication layer, account routing, credentials, company discovery, SMTP or application data access. Content checks against release documentation are not a production-security acceptance test. Existing company/demo services and their settings remain separate from the website update.
