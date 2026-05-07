---
name: find-skills
description: Helps users discover and install agent skills. Searches ClawHub, Vercel skills, and other sources. Use when user asks "find a skill for X", "how do I do X", "is there a skill that can...", or wants to extend agent capabilities.
---

# Find Skills — OpenClaw Edition

Discover and install agent skills from multiple sources: ClawHub, Vercel skills, and community repositories.

## When to Use

- User asks "find a skill for X" or "is there a skill for X"
- User asks "how do I do X" where X might have an existing skill
- User wants to extend agent capabilities
- User searches for tools, templates, or workflows

## Search Strategy

### 1. ClawHub (Primary source for OpenClaw)
```bash
# Search ClawHub for skills
npx clawhub search <query>

# Install from ClawHub
npx clawhub install <skill-name>

# List installed skills
npx clawhub list
```

Browse at: https://clawhub.ai

### 2. Vercel Skills (Cross-platform)
```bash
# Search Vercel skills
npx skills find <query>

# Install from Vercel
npx skills add <owner/repo@skill> -g -y
```

Browse at: https://skills.sh

### 3. Community Sources
- GitHub: Search for "openclaw skill" or "claude code skill"
- awesome-claude-skills: https://github.com/ComposioHQ/awesome-claude-skills
- awesome-openclaw-skills: https://github.com/openclaw/awesome-openclaw-skills

## Installation

### From ClawHub (preferred for OpenClaw)
```bash
npx clawhub install <skill-name>
```

### From GitHub
```bash
# Clone to skills directory
git clone https://github.com/<owner>/<repo>.git ~/.openclaw/workspace/skills/<skill-name>

# Or use clawhub if available
npx clawhub install <owner>/<repo>
```

### From Vercel Skills
```bash
npx skills add <owner/repo@skill> -g -y
```

## Verification

After installation:
1. Read the skill's SKILL.md
2. Check for required dependencies
3. Verify the skill works with `openclaw status`
4. Test the skill with a simple query

## Common Categories

| Category | Example Queries |
|----------|----------------|
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Documentation | docs, readme, changelog, api-docs |
| Code Quality | review, lint, refactor, best-practices |
| Design | ui, ux, design-system, accessibility |
| Productivity | workflow, automation, git |
| AI/ML | ml, model, training, inference |
| IoT | sensors, mqtt, embedded, hardware |
| Agriculture | agronomy, viticulture, farming, crops |

## Response Format

When presenting found skills:

```
I found these skills that might help:

1. **skill-name** — Brief description
   Source: ClawHub | Installs: 1.2K
   Install: `npx clawhub install skill-name`

2. **other-skill** — Brief description
   Source: Vercel | Installs: 5K
   Install: `npx skills add owner/repo@skill`
```

If no skills found:
```
I searched for skills related to "X" but didn't find matches.
I can still help you directly! Would you like me to proceed?
```
