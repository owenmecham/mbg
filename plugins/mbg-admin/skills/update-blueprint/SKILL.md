---
name: update-blueprint
description: >
  Checks for a newer version of the AI Unity Agent Platform, validates license, and applies a non-destructive update. Use when someone says "update blueprint", "check for updates", "update AI OS", "update my skills", "is there a newer version", "upgrade my AI OS", or wants to check for and apply updates to the MBG platform.
---

# Update Blueprint

## Overview

Checks if a newer version of the AI Unity Agent Platform is available, downloads it, validates the local license, and applies a non-destructive update. User data is never overwritten — only skill files and structural templates are updated.

---

## Execution Steps

### Step 1: Read Current Version

First, search Cloud Brain using `mcp__cloud-brain__search_notes` with keyword `version`. If found, use `mcp__cloud-brain__read_note` to get the version info.

As a fallback, read `~/.claude/brain/version.json` to get the currently installed version.

If neither source has version info, report: "No version file found — this might be an older installation. Run the full installer to get version tracking."

Store the current version number.

### Step 2: Check for Updates

Fetch the latest version info from the update endpoint:

```
GET https://mybusinessgenie.ai/api/blueprint-version.json
```

Expected response:
```json
{
  "version": "1.1.0",
  "buildDate": "2026-04-01T00:00:00Z",
  "downloadUrl": "https://mybusinessgenie.ai/downloads/aios-blueprint-payload.tar.gz",
  "changelog": "Added 3 new skills, updated brain templates"
}
```

Compare the remote version to the local version. If the remote version is the same or older, report: "You're already on the latest version (vX.X.X)." and stop.

### Step 3: Validate License

Read `~/.claude/.aios-license.json` and verify:
1. The file exists
2. It contains a valid `keyPrefix`, `machineId`, `tierId`, and `activatedAt`

If the license receipt is missing or invalid, report: "License not found. Please run the AI Unity Agent Platform installer to activate your license." and stop.

### Step 4: Download Update Payload

Download the new payload from the `downloadUrl` in the version response. Extract it to a temporary directory.

```bash
curl -fsSL "<downloadUrl>" -o /tmp/aios-blueprint-update.tar.gz
mkdir -p /tmp/aios-blueprint-update
tar -xzf /tmp/aios-blueprint-update.tar.gz -C /tmp/aios-blueprint-update
```

### Step 5: Apply Non-Destructive Update

Follow these update rules:

**Skills (`~/.claude/skills/`):**
- For each skill folder in the update payload:
  - **Always overwrite** — skills get the latest version
  - This ensures clients always have the most current skill logic

**Brain (Cloud Brain + `~/.claude/brain/`):**
- **Merge mode only:**
  - For each file in the update payload's brain/:
    - Copy only if the destination file does NOT already exist
    - Always overwrite `README.md` and `_TEMPLATE.md` files (structural)
    - Never overwrite user data files (goals.md, daily logs, project files, etc.)
  - User data is primarily stored in Cloud Brain; filesystem brain/ files are structural templates only

**CLAUDE.md:**
- **Never overwrite** `~/CLAUDE.md`
- If the update includes a new CLAUDE.md template, save it as `~/CLAUDE.md.mbg-template-vX.X.X` so the client can review changes

**HOW-TO-ADD-SKILLS.md:**
- Always overwrite at `~/.claude/HOW-TO-ADD-SKILLS.md`

**version.json:**
- Always overwrite at `~/.claude/brain/version.json`
- Also update the version note in Cloud Brain using `mcp__cloud-brain__write_note` with title "version" at path `system/version`

### Step 6: Cleanup and Report

Remove the temporary download files.

Print a summary:
```
============================================
   MBG AI PLATFORM — UPDATE COMPLETE
============================================

Previous version:  vX.X.X
New version:       vY.Y.Y

Skills updated:    XX
Brain files:       XX new, XX skipped (user data preserved)
CLAUDE.md:         Not modified (template saved as ~/CLAUDE.md.mbg-template-vY.Y.Y)
version.json:      Updated

Changelog:
  [changelog text from version response]

============================================
```

### Error Handling

- If the download fails, report the error and do not modify any files
- If extraction fails, report and stop
- If any file copy fails, log a warning and continue with remaining files
- Always clean up temp files, even on failure
