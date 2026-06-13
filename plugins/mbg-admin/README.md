# MBG Admin

**Version:** 1.1.0
**Author:** MyBusinessGenie
**Skills:** 3

---

## What This Plugin Does

MBG Admin keeps your MBG AI system running well between major setup sessions. Three lightweight skills — one for staying aligned on your goals, one for keeping the platform current, and one for publishing results to your cloud dashboard.

Install this after MBG Foundation. All skills are designed to run on a recurring schedule via an agent, or on demand any time you want a quick check-in.

---

## The Two Skills

### Goals Pulse
A 5–10 minute goal alignment check-in. Compares what you actually worked on this week to your quarterly priorities and keystone goal. Flags drift without judgment. Ends with one specific, actionable closing insight.

**Trigger phrases:** "pulse check", "am I on track", "quick goals check", "how am I doing on my goals", "goals check-in", "check my progress", "weekly goals check", "are my daily actions matching my goals"

**Requires:** A goal hierarchy saved by 01 Goal Architect (MBG Foundation). If none exists, Goals Pulse will prompt you to run Goal Architect first.

**Recommended cadence:** Weekly, Monday morning before the week starts

---

### Update Blueprint
Checks whether a newer version of the AI Unity Agent Platform is available, validates your license, and applies a non-destructive update. Skills get the latest version; your personal data (goals, preferences, project notes) is never touched.

**Trigger phrases:** "update blueprint", "check for updates", "update AI OS", "update my skills", "is there a newer version", "upgrade my AI OS"

**Recommended cadence:** Monthly, first of the month

---

### Publish Dashboard
Publishes any skill output to your cloud dashboard at mybusinessgenie.ai as a report card. Pairs automatically with Goals Pulse and Update Blueprint — after either skill runs, say "send to dashboard" and the output appears as a card on your dashboard. Previous runs are automatically archived so you always see the latest.

**Trigger phrases:** "publish this", "send to dashboard", "add to my dashboard", "share to cloud"

**Requires:** cloud-dashboard MCP connected with your API key from mybusinessgenie.ai settings.

**Recommended use:** Pair with scheduled Goals Pulse and Update Blueprint runs so every result is automatically visible on the web.

---

## Setting Up Automatic Scheduling

Both skills are excellent candidates for scheduled automation. To set up recurring runs:

1. Run **03 Agent Designer** (from MBG Foundation) to design your agent team if you haven't already
2. Run **Agent Activator** to activate an agent (e.g., Executive Assistant)
3. During activation, assign Goals Pulse as a weekly Monday task and Update Blueprint as a monthly task
4. Run **Agent Reporter** to configure where the output goes (in-chat, dashboard, etc.)

Or, to schedule manually without an agent:
- Say "schedule Goals Pulse weekly" and Claude will set up a recurring scheduled task
- Say "schedule Update Blueprint monthly" for the platform update check

---

## What Gets Read from Your Brain

| Skill | Reads From | Cloud Brain Path |
|---|---|---|
| Goals Pulse | Goal hierarchy, quarterly priorities, language preferences | `goals/goal-hierarchy`, `goals/quarterly-priorities`, `preferences/language-and-frameworks` |
| Update Blueprint | Version info | `system/version` |

Goals Pulse is read-only except for optional small updates to quarterly priorities (e.g., marking a completed priority done). It never modifies your goal hierarchy without being explicitly asked.

---

## How These Skills Grow in Value Over Time

**Goals Pulse** gets smarter as your goal hierarchy evolves. After each annual Goal Architect session, the pulse check automatically reflects your new priorities — no reconfiguration needed.

**Update Blueprint** ensures every skill you've installed stays current with the latest MBG improvements. Run it monthly and your platform is always on the latest version.

---

## What's in This Version

**v1.1.0** — Added Publish Dashboard skill. Goals Pulse and Update Blueprint now pair with the dashboard connector to push results to mybusinessgenie.ai.

**v1.0.0** — Initial release. Goals Pulse and Update Blueprint packaged together as the MBG Admin plugin.

---

## Companion Plugin

This plugin works alongside **MBG Foundation**. Goals Pulse requires a goal hierarchy from 01 Goal Architect. If you haven't run MBG Foundation yet, start there.
