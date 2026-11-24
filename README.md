# ygo-1103-old-rulings

> **中文简介**：用于查证**游戏王 OCG 1103 环境**（2011 年 3 月禁限卡表、大师规则 2）旧裁定与勘误前卡文的 AI Skill 和 Python 查询脚本，可自动查找 `yugioh-wiki.net` 历史版本与寒波亭 1103 裁定整理并给出可核对的原始出处。本仓库按现状提供，不承诺持续维护。
> - 安装与使用：[中文安装说明（README.zh-CN.md）](README.zh-CN.md)
> - 不用 AI 也能查：[三步查清 OCG 1103 旧裁定（中文教程）](docs/how-to-check-old-rulings.zh-CN.md)

An AI agent skill and Python standard-library toolkit for verifying historical **Yu-Gi-Oh! OCG 1103** (March 2011 Forbidden & Limited list, Master Rule 2) card rulings and pre-errata texts with verifiable primary sources (yugioh-wiki backup revisions, Kanpatei's 1103 ruling compilation, Yugipedia errata history, etc.).

> **Status: Provided as-is, with no commitment to ongoing maintenance.**
> This repository was packaged directly from the internal tooling used to maintain old-ruling override scripts for the 706 / OCG 1103 Nexus server. Issues or PRs may not receive timely responses. Feel free to fork and adapt it for your own format or workflow.

## Human-Readable Guide (No AI Required)

If you just want to look up 1103 rulings yourself without running an AI skill, see the 3-step manual guide:

- **English**: [docs/how-to-check-old-rulings.en.md](docs/how-to-check-old-rulings.en.md)
- **中文（可直接用于 Wiki）**: [docs/how-to-check-old-rulings.zh-CN.md](docs/how-to-check-old-rulings.zh-CN.md)

For Chinese installation instructions, see [README.zh-CN.md](README.zh-CN.md).

## About `SKILL.md`

`SKILL.md` is intentionally kept in **Chinese** (the original authoring language) and is not translated into English. Modern LLMs follow Chinese skill instructions reliably even when you chat in English or Japanese, and keeping a single source avoids translation drift in ruling terminology.

## Repository Contents

| Path | Description |
| --- | --- |
| `SKILL.md` | Main verification workflow, evidence-grade table, cutoff-date rules, and script-checking pitfalls (Chinese) |
| `references/cards-1103.tsv` | OCG 1103 card pool table (card IDs, 4-language names, basic stats) |
| `references/sources.md` | Primary source URL patterns, archive caveats, and limitations |
| `references/examples.md` | Verified ruling examples and citation format templates |
| `references/local-paths.md` | Optional local-environment path template (works out of the box without editing) |
| `scripts/cards.py` | Query `cards-1103.tsv` (or a local `cards.cdb`) by ID, name, archetype, or stats |
| `scripts/wiki.py` | Query `yugioh-wiki.net` backup revision lists and fetch specific `&age=N` snapshots |
| `scripts/kanpa.py` | Fetch and search Kanpatei's 1103 ruling compilation on `note.com` |
| `docs/` | Human-readable 3-step ruling verification guides (EN & ZH) |

All helper scripts use **Python 3 standard library only** (no third-party packages required).

## Quick Setup

### Network Requirements

Live verification needs access to `yugioh-wiki.net` and `note.com` (and optionally `yugipedia.com` and `ocg-rule.readthedocs.io`). If network access is unavailable, the skill falls back to `references/examples.md` and explicitly notes that sources could not be re-verified. Set `HTTPS_PROXY` if your local environment requires a proxy.

### Claude Code / Agent Skills CLI

Copy this directory into your skills folder:

- Personal: `~/.claude/skills/ygo-1103-old-rulings/`
- Project: `.claude/skills/ygo-1103-old-rulings/`

### Claude.ai (Web)

1. Enable **Code Execution** in **Settings → Capabilities** and upload a zip of this repository under **Skills**.
2. Add `yugioh-wiki.net` and `note.com` to **Allowed Domains** on the same page (requires a paid plan; Team/Enterprise admins configure this at the org level).
3. Start a **new conversation** so the updated network settings take effect.

### Other AI Assistants

Point the assistant to `SKILL.md` first and let it run `scripts/*.py` if it has a Python shell, or follow the manual link-opening fallback section inside `SKILL.md`.

## Adapting to Other Formats

### Other OCG Historical Eras (e.g., 2004, 2008, 2012, 2014)

The workflow is straightforward to adapt to other OCG eras:

1. **Parameterize the cutoff date**: Replace the hardcoded `2011-09-01` ruling cutoff in `SKILL.md` (and `scripts/wiki.py` filters) with the end date of your target banlist period.
2. **Swap the card pool table**: Regenerate `references/cards-1103.tsv` from a `cards.cdb` matching your target era's card pool.
3. **Expect lower evidence grades without a community compilation**: For OCG 1103, Kanpatei's compilation (`note.com/sabae5280/n/n95ba4b085cf6`) fills gaps where `yugioh-wiki.net` has no 2011 archive or ambiguous Q&As. Non-1103 OCG eras generally lack an equivalent curated compilation, so you will have to rely primarily on `yugioh-wiki.net` historical revisions and general OCG rules—meaning more rulings will fall into lower evidence grades (indirect evidence, analogy, or post-cutoff fallback) and should be labeled accordingly.

### TCG Historical Formats (e.g., Goat, Edison, Tengu Plant)

**TCG is out of scope for this repository** and will not be added here. If you want to build a similar skill for TCG eras, the main areas to replace are:

- **Primary sources**: Replace `yugioh-wiki.net` and Kanpatei with TCG-specific archives such as Yugipedia revision history / `Card_Errata` (English/pre-PSCT text), archived UDE/KDE rulings, Pojo/Judge-list archives, and community format resources (e.g., Format Library / Edison Format ruling compilations).
- **Card pool & text**: Use a TCG card database with release dates and pre-PSCT / era-accurate English card texts, as TCG/OCG rulings diverged significantly (e.g., Ignition Effect Priority, Trigger Effects in hand/GY, and TCG-exclusive cards).
- **Scripts**: Replace `scripts/wiki.py` and `scripts/kanpa.py` with fetchers for your chosen TCG archives, keeping the same two-step principle (verify the ruling date first, then cite the exact archived revision URL).

## License

MIT License. See [LICENSE](LICENSE).
