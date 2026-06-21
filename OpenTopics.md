# Open Topics

## Templating Kiro Workspaces

**Context:** Migrating many projects to Kiro, each needing a workspace with steering,
hooks, and permissions. Want a template that auto-populates for both new and existing
workspaces.

**Kiro does not have a built-in workspace template mechanism.** Approaches:

1. **Shell script** — Run once per project to stamp `.kiro/steering/`, `.kiro/settings/`,
   and hook files from a template. Works for new and existing workspaces.

2. **User-level steering** — Files in `~/.kiro/steering/` apply to all workspaces
   automatically. Good for universal rules (coding standards, preferred tools).

3. **Combine both** — Universal rules at user level; a script for project-specific
   structure (hooks, MCP config, project-specific steering).

**To build this, need to decide:**

- What goes in the template? (steering rules, hooks, MCP servers, folder structure)
- What varies per project vs. what's universal?
- Invocation method? (shell script, Makefile target, git hook)

**Status:** Parked. Revisit when ready to define the standard workspace setup.
