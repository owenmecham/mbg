# MBG Foundation — AGENTS.md

*Read by Agent Designer and Agent Activator to understand what this plugin provides.*

---

## About This Plugin

MBG Foundation is the starting point for every MBG client. It contains three guided skills that help a client get clear on where they're headed (01 Goal Architect), map their business for AI automation (02 Biz Blueprint), and design their AI agent team (03 Agent Designer).

These are setup skills. They are designed to be run in sequence on first install, and revisited at major milestones (annual planning, business pivots, new ventures). They are not scheduling-oriented — each skill is a one-time or annual workflow, not a daily or weekly task.

---

## Skills Catalog

| Skill | Trigger Phrases | What It Does |
|---|---|---|
| `goal-architect` | "run 01", "goal architect", "set my goals", "build my goal hierarchy", "where do I want to be in 5 years", "I don't know what I'm working toward", "life planning", "reverse engineer my goals" | Guided coaching interview → 5-level goal hierarchy → conflict analysis → keystone goal → saved to Cloud Brain |
| `biz-blueprint` | "run 02", "biz blueprint", "map my business", "automate my business", "how can AI help my business", "business automation plan", "what should I automate" | Business automation discovery interview → agentic workflow recommendations → implementation roadmap |
| `agent-designer` | "run 03", "agent designer", "design my agent team", "what agents should I have", "build my AI staff", "design my team", "set up agents for my company" | Guided team design interview → visual org chart → saved team roster in Cloud Brain → activation roadmap |

---

## Preferences Registry

| Skill | Preferences Saved | Path |
|---|---|---|
| `goal-architect` | EOS language preference, coaching style, goal mode (full/business) | `preferences/language-and-frameworks` |
| `biz-blueprint` | None — all inputs are job-specific | — |
| `agent-designer` | Agent team roster per company | `agent-teams/{company-slug}` |

---

## Suggested Configuration

### First-Time Client Setup (recommended sequence)
Run these in order on first install for the clearest, most connected experience:

1. **01 Goal Architect** — establishes what the client is building toward; this context flows into all future work
2. **02 Biz Blueprint** — maps the business and identifies the highest-impact automation opportunities
3. **03 Agent Designer** — reads the business blueprint and designs a tailored AI team based on what was discovered in steps 1 and 2

No sequence enforcement — clients can run any skill independently at any time.

### Annual Revisit
- **01 Goal Architect** annually (choose "Annual review" when prompted)
- **03 Agent Designer** when the business grows and needs new agents

---

## Schedules Table

These skills are setup and planning tools, not recurring tasks. They are not typically scheduled via Agent Activator. The exception is if a client wants an annual reminder to revisit their goal hierarchy.

| Task | Skill | Suggested Schedule |
|---|---|---|
| Annual goal hierarchy review reminder | `goal-architect` | Once per year (typically set via 01 Goal Architect's built-in scheduler) |

For ongoing system health (weekly goal check-ins, platform updates), see the **MBG Admin** plugin.
