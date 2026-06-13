# COMM-Plaud-Sync
## PLAUD Voice Recording Sync

---

## Overview

This skill syncs AI-generated summaries from PLAUD voice recordings into your Cloud Brain — automatically classifying each recording by domain, extracting action items and insights, and routing notes to the right place. Designed to run on a daily or weekly schedule as part of a communications agent workflow.

**How it works:** Uses the Playwright MCP to access your PLAUD web account at `web.plaud.ai`, pulls the AI-generated summary for each recent recording, analyzes and classifies it, then saves structured notes to Cloud Brain. Full transcripts are not pulled — only summaries, keeping notes concise.

**Connectors required:**
- **Playwright MCP** — for browser-based access to web.plaud.ai
- **Cloud Brain MCP** — for saving notes (included with all MBG plugins)

**No regulated disclaimer required for this skill.**

---

## First-Time Setup (New Clients)

Run this section on first use. It walks through everything needed before syncing can happen automatically.

### Step 1 — Check for Saved Preferences

Search Cloud Brain: `search_notes` with query "plaud preferences"

If preferences are found: confirm in ONE line — "Syncing PLAUD for [Name], [N]-day window, correct?"
- If yes: skip to Pre-Flight
- If no: continue setup

If no preferences found: run the full onboarding below.

---

### Step 2 — PLAUD Device & App Setup

Ask the client:

> "Before we connect your PLAUD recordings, let's make sure everything is set up. Do you already have a PLAUD device and an active account at web.plaud.ai?"

**If yes:** Proceed to Step 3.

**If no, or if they're unsure:** Provide this onboarding overview:

```
PLAUD SETUP OVERVIEW

PLAUD is an AI voice recorder that automatically transcribes and summarizes
your meetings, ideas, and voice notes. Here's what you need:

HARDWARE:
  PLAUD NOTE — pocket-sized card that attaches to your phone (most common)
  PLAUD NotePin — wearable clip-on recorder

MOBILE APP:
  Download "PLAUD" from the App Store or Google Play
  Create an account at web.plaud.ai (same login works on web and mobile)

RECORDING WORKFLOW:
  1. Press the button on your PLAUD device to start recording
  2. When done, the recording syncs to the PLAUD app automatically
  3. PLAUD generates an AI summary within a few minutes
  4. This skill then pulls those summaries into your Cloud Brain

SUBSCRIPTION NOTE:
  PLAUD's AI summary feature requires a PLAUD subscription.
  Free accounts get limited AI processing per month.
  Check plaud.ai/pricing for current plan details.

Once you have your device and account set up, come back and we'll
connect the sync.
```

Stop here if the client needs to get their PLAUD set up first. Tell them: "Once your PLAUD account is active and you have some recordings, come back and say 'plaud sync' to continue setup."

---

### Step 3 — Playwright MCP Check

Check whether the Playwright MCP is available by attempting to use `mcp__playwright__browser_navigate`.

**If Playwright MCP is not available:**

```
PLAYWRIGHT MCP REQUIRED

The Playwright MCP enables this skill to access your PLAUD web account
automatically — no manual exporting needed.

TO CONNECT:
1. Open Cowork Settings → Connectors
2. Search for "Playwright" and install it
3. Restart Cowork
4. Come back and say "plaud sync" to continue

Once connected, this skill can run automatically on a schedule —
syncing your recordings to your brain every morning without you
lifting a finger.
```

Stop here if Playwright is not connected.

---

### Step 4 — PLAUD Web Login

Navigate to the PLAUD file list:
```
https://web.plaud.ai/file-list?categoryId=allFiles
```

Wait 3 seconds for page load, then take a snapshot to check auth state.

**If the page shows a login form or redirects to `/login`:**

```
PLAUD LOGIN NEEDED

I've opened web.plaud.ai in the browser. Please:
  1. Sign in with your email/password, Google, or Apple account
  2. Once you can see your recordings list, tell me "I'm logged in"

I'll never touch your login credentials — you sign in yourself,
and your session stays active in the browser for future syncs.
```

Stop and wait for the user to confirm they're logged in. Resume when they say so.

**If the file list is visible:** Proceed — login is active.

---

### Step 5 — Save Preferences

Collect the following in ONE message:

- **Your name** — for attribution in notes
- **Default sync window** — how many days back to pull on each run (default: 7)
- **Project keywords** — any active project names or keywords you want recordings matched against (e.g., "Acme deal", "Q3 launch", "coaching program")
- **Output format** — Full notes with all sections, or compact notes (summary + action items only)?

Save to Cloud Brain: `brain/preferences/comm-preferences.md` (appended to existing comm preferences if they exist, or created fresh).

Show confirmation: "Setup complete — preferences saved. Running your first sync now..."

Proceed to Core Flow.

---

## Pre-Flight (Returning Users)

### 1. Load Preferences

Search Cloud Brain for `plaud preferences`. Apply saved settings:
- Sync window (days)
- Project keywords
- Output format preference

### 2. Get Current Timestamp

Run `date '+%Y-%m-%d %H:%M'` via Bash. Store for use in note metadata. Never fabricate timestamps.

### 3. Auth Check

Navigate to `https://web.plaud.ai/file-list?categoryId=allFiles`. Wait 3 seconds. Take a snapshot.

- **If file list visible:** Proceed.
- **If login screen:** Prompt the user to sign in manually (same message as Step 4 above). Wait for confirmation.

### 4. Parse Arguments

- `--days N` — Override saved sync window for this run only
- `--project filter` — Only process recordings matching this keyword
- `--dry-run` — Show routing plan without writing any notes

---

## Core Flow

### Step 1 — List Recent Recordings

The browser should be on `web.plaud.ai/file-list?categoryId=allFiles`.

Use `mcp__playwright__browser_evaluate` to extract visible recording items:

```javascript
() => {
  const items = document.querySelectorAll(
    '[class*="file-list"] [class*="item"], [class*="fileList"] [class*="item"], tr[class*="row"], [data-testid*="file-list-item"]'
  );
  if (items.length === 0) {
    const allLinks = document.querySelectorAll('a[href*="/file/"]');
    return Array.from(allLinks).map(a => ({
      id: a.href.split('/file/')[1]?.split('?')[0] || '',
      title: a.textContent?.trim() || '',
      href: a.href,
      raw: a.closest('[class*="item"], tr, li')?.textContent?.trim()?.substring(0, 200) || ''
    }));
  }
  return Array.from(items).map(item => {
    const link = item.querySelector('a[href*="/file/"]');
    const id = link?.href?.split('/file/')[1]?.split('?')[0] ||
               item.dataset?.testid?.replace('file-list-item-', '') || '';
    return {
      id: id,
      title: item.querySelector('[class*="title"], [class*="name"], h3, h4')?.textContent?.trim() || '',
      duration: item.querySelector('[class*="duration"], [class*="time"]')?.textContent?.trim() || '',
      date: item.querySelector('[class*="date"], time')?.textContent?.trim() || '',
      raw: item.textContent?.trim()?.substring(0, 200) || ''
    };
  });
}
```

If JS extraction returns empty, fall back to `mcp__playwright__browser_snapshot` and parse the accessibility tree.

**Scrolling for older recordings:** Recordings are sorted newest-first and lazy-load on scroll. If the sync window requires older recordings:
- Use `browser_evaluate` to scroll: `() => { window.scrollBy(0, 1000); return document.querySelectorAll('a[href*="/file/"]').length; }`
- Wait 2 seconds. Re-extract.
- Stop when the oldest visible recording date is outside the sync window.
- Limit to 10 scroll iterations to avoid infinite loops.

Filter the extracted list to recordings within the sync window. If none found, report and exit:
```
No PLAUD recordings found in the past [N] days. Nothing to sync.
```

---

### Step 2 — Deduplication

For each recording ID, use `mcp__cloud-brain__search_notes` with query `plaud_file_id:[id]`.

If a note with that `plaud_file_id` already exists — skip it.

If all recordings are already synced, report and exit:
```
All PLAUD recordings from the past [N] days have already been synced. Nothing new to import.
```

---

### Step 3 — Process Each Recording

#### 3a — Fetch Summary via Playwright

For each new recording:

1. Navigate to `https://web.plaud.ai/file/{id}`. Wait 3 seconds.

2. Extract metadata (title, duration, date) from the page header using `browser_snapshot` or `browser_evaluate`.

3. Click the **Summary** tab (look for text "Summary" or "AI Summary"):
   ```
   mcp__playwright__browser_click -> ref: [ref from snapshot matching Summary tab]
   ```
   Wait 2 seconds.

4. Extract summary content:
   ```javascript
   () => {
     const area = document.querySelector(
       '[class*="summary"], [class*="content"], [class*="ai-summary"]'
     );
     return area ? area.textContent?.trim() : '';
   }
   ```
   Fall back to `browser_snapshot` accessibility tree if JS extraction fails.

5. Wait 1–2 seconds between recordings to avoid server throttling.

6. After each navigation, verify the page didn't redirect to login. If it did, stop and prompt re-authentication.

Full transcripts are intentionally skipped — summaries only, keeping notes concise.

---

#### 3b — Domain Classification

Use `mcp__cloud-brain__search_notes` with query "project" to find active projects. Collect names, slugs, and keywords.

**Classification rules:**

| Domain | Signals |
|--------|---------|
| `project-specific` | Matches an active project (requires 2+ signals: name + context, or multiple keyword hits) |
| `professional` | Work-related, not tied to a specific project |
| `personal` | Personal reflections, life planning, relationships, health |
| `research` | Market data, competitor info, statistics, learning |
| `mixed` | Spans multiple domains, or confidence < 70% |

A recording can match at most one project. If ambiguous between projects, default to `professional`. When confidence < 70%, classify as `mixed`.

---

#### 3c — Content Analysis

Extract from the summary:
- **Key Themes** — 3–5 primary topics discussed
- **Insights** — Notable realizations or conclusions
- **Action Items** — Tasks and commitments, attributed to the person who owns each one. Use names from the recording when available; use "Unassigned" when ownership is unclear.
- **Decisions** — Any decisions stated or implied
- **People Mentioned** — Names and their context in the conversation
- **Questions Raised** — Open questions or things to investigate

---

#### 3d — Generate Note

```markdown
---
type: "plaud-note"
domain: "[personal|professional|project-specific|research|mixed]"
project: "[project-slug or empty]"
date: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:MM"
plaud_file_id: "[file-id]"
recording_started: "YYYY-MM-DD HH:MM"
recording_duration: "[duration in minutes]"
themes: ["theme1", "theme2", "theme3"]
tags: ["plaud", "voice-note", "[domain-tag]"]
status: "captured"
---

# PLAUD Note: [Descriptive Title from Content]

## Summary
[AI-generated summary from PLAUD]

## Key Themes
1. **[Theme]:** [description]
2. **[Theme]:** [description]
3. **[Theme]:** [description]

## Insights
- [Notable insight]
- [Notable insight]

## Action Items
- [ ] [Action item] — [Owner]
- [ ] [Action item] — [Owner]

## Decisions
- [Decision with context]

## People Mentioned
- **[Name]:** [context of mention]

## Questions Raised
- [Open question]

## Domain Classification
- **Primary Domain:** [domain] ([confidence]%)
- **Reasoning:** [brief rationale]

---
*Synced from PLAUD via Communications Suite — Plaud Sync*
```

YAML frontmatter rules: all strings quoted with double quotes; arrays use quoted strings; numbers unquoted unless they are string identifiers.

---

### Step 4 — Save to Cloud Brain

All notes saved using `mcp__cloud-brain__write_note`.

#### Primary Note

- **Path:** `brain/communications/plaud/plaud-[YYYY-MM-DD]-[descriptive-slug].md`
- **Content:** Full structured note from Step 3d

Include `[[Entity Name]]` wiki-links for all people mentioned and projects referenced.

#### Cross-Reference Updates

| Condition | Also update |
|-----------|-------------|
| All recordings | Append entry to `brain/daily/log-[YYYY-MM-DD].md` with a link to the primary note |
| `project-specific` | Find the project note with `mcp__cloud-brain__search_notes`, append a cross-reference link |
| `research` | Save or update a topic note under `brain/research/` |

#### People Mentioned

For each new person with substantive context (role, company, relationship):
1. Check `mcp__cloud-brain__search_notes` for an existing people entry
2. If new: create a note at `brain/people/[firstname-lastname].md` with context and a link back to the PLAUD note

---

### Step 5 — Sync Summary

After all recordings are processed:

```
PLAUD SYNC COMPLETE — [Date]

| # | Recording | Domain | Duration |
|---|-----------|--------|----------|
| 1 | [title]   | Professional | 12 min |
| 2 | [title]   | Project: [name] | 8 min |
| 3 | [title]   | Personal | 5 min |

Imported: [N] new recordings
Skipped:  [N] (already synced)
Total audio processed: [N] minutes
Brain notes updated: [list any daily logs, project notes, research notes touched]
```

If any recordings failed, list them with the file ID and error details.

**After sync, you may want to run:**
- **Bizops Daily Brief** — see how new recordings connect to today's priorities
- **Comm-Meeting-Actions** — extract deeper action items from any formal meeting recording
- **Comm-Meeting-Transcript** — full debrief processing for high-stakes calls

---

## Scheduling — Run Automatically

This skill is designed to run on a schedule without manual triggering. Recommended setups:

**Daily (most current):** Run each morning at 6:00 AM with `--days 1` — catches only yesterday's recordings and delivers the digest before you start your day.

**Weekly (less noise):** Run Monday mornings with `--days 7` — reviews the full prior week in one batch.

To set up automated syncing, run the **AI Agents** plugin and assign Plaud Sync to your Communications Agent with your preferred schedule.

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Not logged in to PLAUD | Prompt manual sign-in via the browser. Stop until confirmed. Never touch credentials. |
| Session expired mid-sync | Detect login redirect, prompt re-auth, stop |
| Playwright MCP not connected | Show connector setup instructions. Stop. |
| web.plaud.ai unreachable | "Could not reach web.plaud.ai — check your internet connection." |
| Empty file list page | Take a screenshot for debugging. Report to user. |
| Recording has no summary yet | Create a minimal note with metadata only. Flag: "⚠️ Summary not yet available — re-sync later." |
| Summary tab missing | Same as above — create minimal entry, note that AI processing may still be in progress |
| JS extraction returns empty | Fall back to `browser_snapshot` accessibility tree. If that also fails, screenshot and report. |
| Dry run | Show the full routing plan (which notes would be created, which brain notes updated) without writing anything |

---

## Deduplication Rules

- Always deduplicate by `plaud_file_id`, never by title or date alone
- A recording is a duplicate if and only if its exact `plaud_file_id` exists in any Cloud Brain note's frontmatter
- Re-running the skill is always safe — it will skip everything already synced
