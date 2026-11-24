# ygo-1103-old-rulings 安装说明

查证游戏王 OCG「1103」卡池（2011 年 3 月禁限环境、大师规则 2，706 服的旧裁定），并给出可核对的原始出处（yugioh-wiki 历史版本、寒波亭 1103 裁定整理等）。主体是 `SKILL.md`；`references/` 是来源说明、已查证的例子和 1103 卡池数据；`scripts/` 是三个只用 Python 标准库的查询工具。

## 需要的网络

查证要能访问 `yugioh-wiki.net` 和 `note.com`（需要时还有 `yugipedia.com`、`ocg-rule.readthedocs.io`）。访问不了时，AI 只能引用 `references/examples.md` 里已核对过的结论，并会注明“本次未能重新核对”。

## 网页版 Claude（claude.ai）

1. 「设置 → 功能（Settings → Capabilities）」里打开代码执行，把本仓库打包成 ZIP 后在 Skills 处上传（或下载 GitHub Release / Code → Download ZIP 后保留包含 `SKILL.md` 的文件夹打包上传）。
2. 同一页的允许域名（allowed domains）里加上 `yugioh-wiki.net`、`note.com`。个人付费版自己设置；Team／Enterprise 由管理员在组织设置里加；免费版只能放行软件包源，加不了这两个网站。
3. **新开一个对话**再用——已开着的对话沿用旧的网络设置。

## Claude Code

把本仓库文件夹放到 `~/.claude/skills/ygo-1103-old-rulings/`（个人）或项目的 `.claude/skills/ygo-1103-old-rulings/` 下即可。本机能联网时脚本直接可用；需要代理就设置 `HTTPS_PROXY`。

## ChatGPT（自定义 GPT 或项目）

1. 把 `SKILL.md` 的全文贴进「指令」。
2. 把 `references/sources.md`、`references/examples.md`、`references/cards-1103.tsv` 作为知识文件上传。
3. 打开「网页搜索」。`scripts/` 下的 Python 脚本是可选的，只有代码环境能联网时才用得上。

## 其他 AI

让它先读 `SKILL.md`，按里面的流程做；没有代码环境时按“网络受限时”一节手动打开链接。

## 说明

- `references/local-paths.md` 是空白模板，按自己的环境填写，不填也能用。
- 结论和出处会被写进公开记录，所以 skill 要求宁可写“未找到出处”，也不给对不上原文的链接。发现例子或规则有误，欢迎反馈给维护者。
