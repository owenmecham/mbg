# Communications Suite
### Version 1.0.0 — MyBusinessGenie

---

## What This Plugin Does

The Communications Suite is an AI-powered toolkit that handles the most time-consuming parts of professional communication: processing your inbox, drafting emails in your voice, walking into every meeting prepared, extracting decisions from transcripts, and building negotiation strategies on demand.

The flagship use case is the **Executive Inbox Agent** — a scheduled agent that triages your inbox every morning before you start your day. You wake up to a structured digest: what's urgent, what can wait, what to ignore — with draft responses ready for critical items.

---

## Skills in This Plugin

### Comm-Inbox-Triage
**Trigger phrases:** "triage my inbox," "process my email," "inbox zero," "what needs a response," "email triage," "clear my inbox"

Processes a batch of emails and categorizes every item into four tiers:
- 🚨 **Urgent / Action Required** — needs a response today
- ⚡ **Important / Respond This Week** — needs attention but not today
- 📋 **Low / Read or File** — informational, no reply needed
- 🗑️ **Ignore / Unsubscribe Candidate** — noise to eliminate

Drafts responses for urgent items. Surfaces action items. Flags repeat noise senders for unsubscribing. Designed to run on a daily schedule — this is the core skill of the Executive Inbox Agent.

---

### Comm-Email-Drafter
**Trigger phrases:** "draft an email," "write an email to," "cold outreach email," "follow-up email," "proposal email," "write this email for me"

Drafts professional emails for any situation in your tone and voice. Handles cold outreach, follow-ups, proposals, introductions, thank-yous, negotiation emails, investor outreach, and client check-ins. Delivers the draft ready to send, with structure notes and alternate versions.

---

### Comm-Meeting-Prep
**Trigger phrases:** "prep for my meeting," "meeting prep," "meeting with [name]," "talking points for," "prepare for my call"

Generates a complete pre-meeting intelligence brief: attendee research, structured agenda, key talking points, anticipated objections with scripts, questions to ask, and a follow-up email template — ready before you walk in the door.

---

### Comm-Meeting-Transcript
**Trigger phrases:** "process this transcript," "meeting transcript," "what did we decide," "summarize this recording," "debrief this call"

Paste a transcript or recording summary and get a structured debrief: decisions made, action items with owners, follow-ups needed, open questions, and key insights. Cross-references against your prep brief if one was saved.

---

### Comm-Meeting-Actions
**Trigger phrases:** "extract action items," "action items from this meeting," "who owns what," "parse these meeting notes"

The fast-path version of Meeting-Transcript, purpose-built for converting notes into a task list. Paste meeting notes and get structured action items with owners, due dates, and a shareable summary block ready to paste into Slack or email.

---

### Comm-Negotiation-Prep
**Trigger phrases:** "negotiation prep," "negotiation strategy," "how should I negotiate," "prep for this deal," "contract negotiation," "salary negotiation"

Builds a complete negotiation strategy: BATNA analysis, leverage map, counterparty research, objection scripts, concession strategy, and a structured conversation flow guide. Works for any negotiation — salary, vendor contracts, deal terms, partnerships, pricing.

---

### Comm-iMessage *(requires BlueBubbles connector)*
**Trigger phrases:** "send a text," "iMessage," "text someone," "send an iMessage"

Send iMessages from your AI to individuals or groups via BlueBubbles. Always shows the message for your confirmation before sending. Requires the BlueBubbles app and MCP connector.

---

## The Executive Inbox Agent

The highest-value use of this plugin is setting up an **Executive Inbox Agent** using the `ai-agents` system:

1. Run **system-03 (Agent Designer)** and choose the "Executive Inbox Agent" configuration
2. Run **system-04 (Agent Activator)** to set your preferences and schedule the daily 6:30 AM triage
3. Every morning you'll receive a triage digest before you open your laptop — urgent items with draft responses, everything else categorized and cleared

Optionally add `bizops-daily-brief` to the same agent to combine your inbox triage with your daily priorities into one unified morning briefing.

---

## Preferences Setup

On first run, each skill collects your preferences in one message and saves them to your Cloud Brain. All comm skills share a single preference file, so you only set up once.

**What gets saved:**
- Your name, title, and business
- Email accounts and triage settings (VIP list, ignore list, response time)
- Email tone and signature
- Meeting and follow-up style preferences
- Negotiation style and domains

**To update your preferences at any time:** Tell any comm skill "update my communications preferences" and it will walk you through the changes.

---

## Memory Paths

| Data | Cloud Brain Path |
|---|---|
| Preferences | `brain/preferences/comm-preferences.md` |
| Daily triage logs | `brain/communications/triage/triage-[date].md` |
| Email drafts | `brain/communications/drafts/draft-[slug]-[date].md` |
| Meeting prep briefs | `brain/communications/meetings/prep-[slug]-[date].md` |
| Meeting debriefs | `brain/communications/meetings/debrief-[slug]-[date].md` |
| Negotiation strategies | `brain/communications/meetings/negotiation-prep-[slug]-[date].md` |

---

## Pairs Well With

- **bizops** — Route meeting action items to the Follow-Up Tracker; combine inbox triage with the Daily Brief for a unified morning briefing
- **ai-agents** — Set up the Executive Inbox Agent with a daily triage schedule
- **research-intelligence** — Meeting Prep uses deep research for high-stakes attendee profiles

---

## Version History

### v1.0.0 — 2026-06-12
Initial release. Seven skills: inbox triage, email drafting, meeting prep, meeting transcript processing, meeting action extraction, negotiation prep, and iMessage. Shared preferences layer. Executive Inbox Agent configuration in AGENTS.md.

---

*MyBusinessGenie — communications-suite v1.0.0*
