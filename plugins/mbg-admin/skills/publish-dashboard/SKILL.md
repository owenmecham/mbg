---
name: publish-dashboard
description: >
  Publish a report to your cloud dashboard on mybusinessgenie.ai. Use this skill when a scheduled task completes, when the user says "publish this", "send to dashboard", "add to my dashboard", "share to cloud", or when any skill produces output that should be visible on the web dashboard as a report card. Automatically pairs with Goals Pulse and Update Blueprint to push their output to the dashboard.
argument-hint: "[task name] [content to publish]"
allowed-tools: [Read, Glob, Grep]
---

# Publish to Dashboard

Publish AI-generated reports from scheduled skill runs to the client's cloud dashboard on mybusinessgenie.ai. Each report appears as a card showing the latest run of that task. Previous runs are automatically archived.

## When This Skill Applies

- A Goals Pulse or Update Blueprint run completes and the client wants results on the dashboard
- A scheduled task completes (any MBG skill running on a cadence)
- Client says "publish this", "send to dashboard", "add to my dashboard"
- Any skill produces output the client wants visible on the web

## How It Works

### Step 1: Determine What to Publish

Look at the current conversation for publishable content:
- Output from a completed skill run (Goals Pulse, Update Blueprint, or any other MBG skill)
- A report or analysis just generated
- Explicit content the client provides

### Step 2: Get the Agent's Persona

Before publishing, retrieve the agent's communication style:

```
mcp__cloud-dashboard__get_agent_persona()
```

This returns the agent's name and persona description. **Apply this persona to shape the tone, style, and formatting of the report content.** If no persona is configured, use your default style.

### Step 3: Publish the Report

Call the `mcp__cloud-dashboard__publish_report` MCP tool:

```
mcp__cloud-dashboard__publish_report(
  taskName: "kebab-case-task-id",
  taskLabel: "Human-Readable Task Name",
  category: "briefing|email|social|real-estate|crm|research|custom",
  content: "full markdown report content",
  summary: "1-2 sentence preview for the card",
  actionRequired: true|false,
  actionCount: 0,
  tags: ["relevant", "tags"],
  links: [{ label: "View Details", url: "https://..." }],
  ttlDays: 30
)
```

### Step 4: Confirm to Client

After publishing, confirm:
- What was published (task label + category)
- That the previous run was archived (if applicable)

## Category Guide for MBG Admin Skills

**IMPORTANT:** Always use the exact `taskName` below. Using different names for the same task creates duplicate cards on the dashboard.

| Skill / Task | taskName | category |
|---|---|---|
| Goals Pulse (weekly check-in) | `goals-pulse` | `briefing` |
| Update Blueprint (platform update) | `update-blueprint` | `custom` |
| Morning Briefing / Daily Brief | `morning-briefing` | `briefing` |
| Email Digest / Inbox Triage | `email-digest` | `email` |
| Social Trends / Content Calendar | `social-trends` | `social` |
| Lead Pipeline / CRM New Leads | `lead-pipeline` | `crm` |
| Deal Analysis / Property Research | `deal-analysis` | `real-estate` |
| Market Research / Competitor Analysis | `market-research` | `research` |
| Financial Snapshot / KPI Dashboard | `financial-snapshot` | `research` |
| Generic / Custom output | `custom-report` | `custom` |

## Publishing Goals Pulse Output

When Goals Pulse completes, publish its output like this:

```
mcp__cloud-dashboard__publish_report(
  taskName: "goals-pulse",
  taskLabel: "Goals Pulse",
  category: "briefing",
  content: "<full pulse check output>",
  summary: "<one sentence: alignment score + key insight from the session>",
  actionRequired: <true if any priorities are at risk>,
  actionCount: <number of at-risk priorities>,
  tags: ["goals", "weekly-check-in"]
)
```

## Publishing Update Blueprint Output

When Update Blueprint completes, publish its output like this:

```
mcp__cloud-dashboard__publish_report(
  taskName: "update-blueprint",
  taskLabel: "Platform Update",
  category: "custom",
  content: "<full update summary>",
  summary: "<one sentence: version installed or 'already on latest'>",
  actionRequired: false,
  actionCount: 0,
  tags: ["platform", "update"]
)
```

## Action Items

If the report contains action items:
- Set `actionRequired: true`
- Set `actionCount` to the number of items
- The dashboard card will show an action indicator

## Integration with Scheduled Tasks

When a scheduled task runs Goals Pulse or Update Blueprint, publish its output automatically at the end of the skill run. The previous run's card is automatically archived — only the latest shows on the dashboard.

## Error Handling

- **MCP server not connected:** Tell the client to configure the cloud-dashboard MCP server with their API key from mybusinessgenie.ai settings.
- **API key invalid:** Tell the client to generate a new API key in the portal settings.
