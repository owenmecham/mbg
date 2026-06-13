# MBG Admin — AGENTS.md

*Read by Agent Designer and Agent Activator to understand what this plugin provides.*

---

## About This Plugin

MBG Admin keeps the MBG AI system running well between major setup sessions. It contains two recurring skills: Goals Pulse for weekly goal alignment check-ins, and Update Blueprint for monthly platform health checks. Both are designed to run on a schedule as part of an agent's recurring task list.

---

## Skills Catalog

| Skill | Trigger Phrases | What It Does |
|---|---|---|
| `goals-pulse` | "pulse check", "am I on track", "quick goals check", "how am I doing on my goals", "goals check-in", "weekly goals check", "are my daily actions matching my goals" | 5–10 minute goal alignment check-in — compares current week's activity to quarterly priorities and keystone goal; flags drift; surfaces one closing insight |
| `update-blueprint` | "update blueprint", "check for updates", "update AI OS", "update my skills", "is there a newer version", "upgrade my AI OS" | Checks for a newer version of the AI Unity Agent Platform, validates license, and applies a non-destructive update |
| `publish-dashboard` | "publish this", "send to dashboard", "add to my dashboard", "share to cloud" | Publishes any skill output to the client's cloud dashboard on mybusinessgenie.ai as a report card; pairs automatically with Goals Pulse and Update Blueprint |

---

## Preferences Registry

| Skill | Preferences Read | Path |
|---|---|---|
| `goals-pulse` | Goal hierarchy, quarterly priorities, language/framework preference | `goals/goal-hierarchy`, `goals/quarterly-priorities`, `preferences/language-and-frameworks` |
| `update-blueprint` | Version info, license | System files (version.json, .aios-license.json) |

No skill in this plugin maintains its own standalone preferences file. Goals Pulse reads from the goal hierarchy established by MBG Foundation's 01 Goal Architect. Publish Dashboard reads the agent persona via the cloud-dashboard MCP at publish time.

---

## Suggested Configuration

### Configuration A — Weekly + Monthly Automation with Dashboard (recommended)
Assign all three skills to an Executive Assistant agent or a dedicated Admin Agent:

- **Goals Pulse** — every Monday morning, before the week starts → output published to dashboard automatically
- **Update Blueprint** — first of the month, early morning → result published to dashboard
- **Publish Dashboard** — runs at the end of each Goals Pulse and Update Blueprint session

This creates a lightweight "AI OS maintenance" cadence that keeps goals and the platform current, with results always visible on the mybusinessgenie.ai dashboard.

### Configuration B — On-Demand Only
Clients who prefer manual control can run any skill any time by typing the trigger phrase. No scheduling required.

### Configuration B — On-Demand Only
Clients who prefer manual control can run either skill any time by typing the trigger phrase. No scheduling required.

---

## Schedules Table

| Task | Skill | Suggested Schedule | Notes |
|---|---|---|---|
| Weekly goal alignment check-in | `goals-pulse` | Weekly, Monday 7:00 AM | Requires goal hierarchy from 01 Goal Architect to be set up first |
| Monthly platform update check | `update-blueprint` | Monthly, 1st of month, 6:00 AM | Non-destructive — skips if already on latest version |
| Publish Goals Pulse to dashboard | `publish-dashboard` | After each Goals Pulse run | Paired — runs at end of Goals Pulse automatically |
| Publish Update Blueprint to dashboard | `publish-dashboard` | After each Update Blueprint run | Paired — runs at end of Update Blueprint automatically |
