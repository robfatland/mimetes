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


## mimetes to do list


- Coordinate the existing makefile for building html decks with a bulk copy that renames `slides.html` to `~/D/slidesTopicword.html`
- Verify that the relocated/renamed html decks run properly in Chrome including rendering all images


## Marp → Google Slides

**Goal:** Present Marp slide decks via Google Slides.

**Current approach (show-don't-edit):**

```bash
marp slides.md -o slides.pptx --allow-local-files --html
```

Upload the `.pptx` to Google Drive → open with Google Slides. Each slide is
rendered as a flat image — presentable but not editable in Slides.

**If editability is needed later:** The `marp2pptx` Python package
(`pip install marp2pptx`) produces PPTX with native text objects rather than
rasterized images. Import to Google Slides preserves editable text/code blocks.

**Status:** Using Option 1 (flat image export) for now.
