# Communications Suite — Agent Capabilities Manifest

*For use by system-03 (Agent Designer) and system-04 (Agent Activator)*
*Last updated: 2026-06-12 — v1.1.0: comm-plaud-sync added (8 skills)*

---

## About This Plugin

`communications-suite` is a complete AI communications toolkit for busy professionals. It covers the full communications loop: triage an overflowing inbox, draft emails in the user's voice, walk into every meeting prepared, extract decisions and actions from transcripts, build strategies for high-stakes negotiations, and automatically sync PLAUD voice recordings into the Cloud Brain.

**Target users:** Business owners, executives, sales professionals, consultants, and anyone who spends significant time in email, meetings, and voice notes. The flagship use case is the **Executive Inbox Agent** — a scheduled agent that triages email and syncs PLAUD recordings automatically each morning before the user starts their day.

**Plugin version:** 1.1.0 (8 skills)

---

## Available Skills Catalog

---

### 1. comm-inbox-triage

**What it does:** Processes a batch of emails, categorizes every item into four urgency tiers (Urgent / Important / Low / Ignore), drafts responses for critical items, surfaces action items, and logs unsubscribe candidates. The flagship scheduling skill — runs daily as the Executive Inbox Agent.

**Preferences collected at activation:**
- Name and business
- Email accounts to triage
- Response time expectation (same day / 24h / 48h)
- VIP list (senders whose emails are always urgent)
- Ignore list (senders or types to always deprioritize)
- Preferred output format (digest summary / item-by-item breakdown)

**Suggested schedule:** Daily, 6:00–7:00 AM — before the user's workday begins.

**Natural pairings:** comm-email-drafter (for urgent response drafts), bizops-follow-up (action items routed to follow-up tracker), bizops-daily-brief (urgent items surfaced in morning briefing).

---

### 2. comm-email-drafter

**What it does:** Drafts professional emails for any situation — cold outreach, follow-ups, proposals, introductions, thank-yous, negotiation, investor outreach — written in the user's voice and tone.

**Preferences collected at activation:**
- Name and title
- Business name and one-sentence description
- Default email tone (warm / professional / direct / conversational)
- Standard email signature elements
- Anything to always include or always avoid

**Suggested schedule:** On-demand — triggered when drafting specific emails. Can also run in batch mode to draft multiple follow-ups at once.

**Natural pairings:** comm-inbox-triage (drafts urgent responses), comm-meeting-prep (follow-up email template), comm-negotiation-prep (negotiation email drafting).

---

### 3. comm-meeting-prep

**What it does:** Generates a complete pre-meeting intelligence brief — attendee research, agenda, talking points, anticipated objections with responses, and a follow-up template.

**Preferences collected at activation:**
- Name, title, and business
- Primary role in meetings (seller / buyer / consultant / employee / investor)
- Preferred meeting structure (agenda-first / rapport-first)
- Default follow-up style

**Suggested schedule:** On-demand — triggered before each significant meeting. Can be scheduled to run automatically the evening before any calendar event.

**Natural pairings:** comm-meeting-transcript (post-meeting debrief links back to prep brief), comm-email-drafter (pre-built follow-up template).

---

### 4. comm-meeting-transcript

**What it does:** Processes meeting transcripts or recordings — extracts decisions, action items, follow-ups, open questions, and key insights into a structured debrief. Compares against prep brief if one exists.

**Preferences collected at activation:**
- Output format preference (full debrief / action items only / executive summary)

**Suggested schedule:** On-demand — triggered after each meeting. Pairs with comm-meeting-prep as Phase 1 to its Phase 0.

**Natural pairings:** comm-meeting-prep (cross-references planned vs. actual), comm-meeting-actions (faster action-item-only version), bizops-follow-up (routes action items to follow-up tracker).

---

### 5. comm-meeting-actions

**What it does:** Converts meeting notes into a structured task list with owners, due dates, and a shareable summary block. Faster and more focused than comm-meeting-transcript — purpose-built for action item extraction.

**Preferences collected at activation:**
None — every input changes every run. No preferences layer.

**Suggested schedule:** On-demand — triggered immediately after any meeting where notes were taken.

**Natural pairings:** bizops-follow-up (add action items to tracker), bizops-project-tracker (route project-related actions to project milestones).

---

### 6. comm-negotiation-prep

**What it does:** Builds a complete negotiation strategy — BATNA analysis, leverage map, counterparty research, objection scripts, concession strategy, and a structured conversation flow.

**Preferences collected at activation:**
- Name, role, and business
- Default negotiation style
- Industries or deal types most commonly negotiated

**Suggested schedule:** On-demand — triggered before any significant negotiation.

**Natural pairings:** comm-meeting-prep (if the negotiation is in a meeting), comm-email-drafter (post-negotiation summary email).

---

### 7. comm-plaud-sync

**What it does:** Automatically syncs AI-generated summaries from PLAUD voice recordings into Cloud Brain — classifying each recording by domain (professional, personal, project-specific, research), extracting action items and insights, and routing notes to the correct brain location. Includes a guided first-time setup for new PLAUD users. Designed to run on a daily or weekly schedule as part of the Communications Agent workflow.

**Preferences collected at activation:**
- Name (for note attribution)
- Default sync window in days (default: 7)
- Active project keywords for recording classification
- Output format preference (full notes / compact notes)

**Connectors required:** Playwright MCP (for browser-based access to web.plaud.ai)

**Suggested schedule:** Daily, 6:00 AM with `--days 1` — or weekly, Monday morning with `--days 7`.

**Natural pairings:** comm-inbox-triage (both run as part of the morning Communications Agent), bizops-daily-brief (PLAUD action items surface in the daily briefing), comm-meeting-actions (deeper extraction for formal meeting recordings).

---

### 8. comm-imessage

**What it does:** Sends iMessages to individuals or groups via BlueBubbles MCP. Always shows message for confirmation before sending.

**Preferences collected at activation:**
- Name for sign-offs
- Frequently messaged contacts or groups (optional shortcuts)

**Connector required:** BlueBubbles MCP

**Suggested schedule:** On-demand — triggered when texting someone.

**Natural pairings:** comm-inbox-triage (quick follow-up texts to urgent contacts), comm-meeting-prep (reminder text to attendees before meeting).

---

## Preferences Registry

All preferences save to: `brain/preferences/comm-preferences.md`

Skills share this single preference file. system-04 collects all fields in one interview.

| Field | Used By | Type | Notes |
|---|---|---|---|
| name | all skills | identity | User's name for email/message sign-off |
| title | drafter, meeting-prep, negotiation | identity | Professional title |
| business_name | all skills | identity | Business name |
| business_description | drafter, meeting-prep | identity | One-sentence description |
| email_accounts | inbox-triage | identity | List of accounts to triage |
| response_time | inbox-triage | identity | Same day / 24h / 48h |
| vip_list | inbox-triage | identity | Names/emails always treated as urgent |
| ignore_list | inbox-triage | identity | Names/emails always deprioritized |
| triage_output_format | inbox-triage | identity | Digest or item-by-item |
| email_tone | drafter | identity | Warm / professional / direct / conversational |
| email_signature | drafter | identity | Signature elements to include |
| email_avoid | drafter | identity | Things to never include in emails |
| meeting_role | meeting-prep | identity | Seller / buyer / consultant / etc. |
| meeting_structure | meeting-prep | identity | Agenda-first / rapport-first |
| followup_style | meeting-prep | identity | Formal email / casual / action items |
| transcript_output_format | meeting-transcript | identity | Full / actions-only / summary |
| negotiation_style | negotiation-prep | identity | Collaborative / competitive / principled |
| negotiation_domains | negotiation-prep | identity | Deal types most commonly negotiated |
| imessage_contacts | imessage | identity | Saved contact shortcuts |
| plaud_sync_days | plaud-sync | identity | Default lookback window in days (default: 7) |
| plaud_project_keywords | plaud-sync | identity | Active project names/keywords for recording classification |
| plaud_output_format | plaud-sync | identity | Full notes or compact (summary + actions only) |

---

## Suggested Agent Configurations

### Configuration 1 — Solo: Executive Inbox Agent
The most popular single-agent setup. One agent handles all communications.

**Agent name:** Executive Assistant (or name it: "Alex", "Jordan", etc.)
**Skills assigned:** comm-inbox-triage, comm-email-drafter, comm-meeting-prep, comm-meeting-transcript, comm-meeting-actions, comm-negotiation-prep
**Scheduled tasks:**
- Daily triage: inbox-triage every morning at 6:30 AM
- Weekly digest: inbox pattern summary every Friday at 5:00 PM
**On-demand tasks:** All other skills triggered as needed

---

### Configuration 2 — Two Agents: Inbox Agent + Meeting Agent
Separates daily communications management from meeting intelligence.

**Agent 1 — Inbox Manager**
Skills: comm-inbox-triage, comm-email-drafter, comm-imessage
Schedule: Daily 6:30 AM triage

**Agent 2 — Meeting Intelligence**
Skills: comm-meeting-prep, comm-meeting-transcript, comm-meeting-actions, comm-negotiation-prep
Schedule: On-demand; optionally scheduled to prep the night before calendar events

---

### Configuration 3 — Integrated: Comms + BizOps Agent
Combines this plugin with bizops for a full executive assistant agent.

Recommended if the client also has `bizops` installed. Pair:
- comm-inbox-triage + bizops-daily-brief → unified morning briefing
- comm-meeting-actions + bizops-follow-up → action items automatically added to follow-up tracker
- comm-meeting-prep + bizops-people → attendee context pulled from people notes

---

## Recommended Schedules Table

| Skill | Recommended Schedule | Trigger | Notes |
|---|---|---|---|
| comm-inbox-triage | Daily, 6:00–7:00 AM | Scheduled | Core Executive Inbox Agent task |
| comm-inbox-triage (weekly digest) | Weekly, Friday 5 PM | Scheduled | Pattern summary — which senders are noisy |
| comm-email-drafter | On-demand | User trigger | Batch mode available for follow-up sets |
| comm-meeting-prep | On-demand or night before | User trigger | Optional: auto-trigger from calendar events |
| comm-meeting-transcript | On-demand | User trigger | Run immediately after meetings |
| comm-meeting-actions | On-demand | User trigger | Run immediately after meetings |
| comm-negotiation-prep | On-demand | User trigger | Run before any significant negotiation |
| comm-plaud-sync | Daily, 6:00 AM (`--days 1`) | Scheduled | Pairs with inbox triage in the morning Communications Agent |
| comm-plaud-sync (weekly) | Weekly, Monday 7:00 AM (`--days 7`) | Scheduled | Alternative for lower-volume PLAUD users |
| comm-imessage | On-demand | User trigger | Always requires user confirmation before send |

---

## Instructions for system-03 and system-04

**system-03 (Agent Designer):**
- The Executive Inbox Agent is the primary suggested configuration — lead with it for any client who mentions email overwhelm, inbox problems, or communications management
- This plugin pairs naturally with `bizops` — if both are installed, suggest the integrated Configuration 3
- `comm-imessage` requires the BlueBubbles MCP connector — flag this if the client doesn't have it connected
- `comm-plaud-sync` requires the Playwright MCP connector — flag this if not connected; the skill has a built-in onboarding flow that guides first-time setup including Playwright install, PLAUD account verification, and initial login

**system-04 (Agent Activator):**
- All comm preferences share one file: `brain/preferences/comm-preferences.md` — collect all fields in a single interview, not one per skill
- The daily inbox-triage schedule is the most valuable task to set up — prioritize it
- `comm-meeting-actions` has no preferences — skip preference collection for this skill
- After collecting preferences, confirm the daily triage schedule time with the client (default 6:30 AM but many clients prefer 7:00 AM or before they check their phone)
- For `comm-plaud-sync`: if the client uses PLAUD, add it to the morning Communications Agent schedule alongside inbox triage. If they're new to PLAUD, note the Playwright MCP requirement and that the skill walks through full setup on first run.
