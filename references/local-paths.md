# 本机路径（按自己的环境填写；没有的可以不填）

skill 不依赖这里的任何路径也能用：卡名和卡片数据用打包的 `cards-1103.tsv`，查 wiki 和寒波亭只需要能联网。下面这些是可选的。

| 用途 | 路径 |
| --- | --- |
| 1103 四语卡库（`cards.py --db <目录>`，目录下有 zh-CN、ja-JP、en-US、ko-KR，各含 cards.cdb） | （可选） |
| 旧裁定覆盖脚本仓库 specials（GitHub `301zrg/specials`，`706-meta/CHANGELOG.md` 含全部历史出处） | （可选，本地克隆的位置） |
| 修旧裁定问题时用的测试客户端（放残局、改脚本） | （可选） |
| 代理（脚本访问 wiki／note 直连失败时） | （可选，例如 `HTTPS_PROXY=http://127.0.0.1:<端口>`） |

示例：

```
python scripts/cards.py 27821104 荒行
python scripts/cards.py --set 0x103d --main --atk 1000
python scripts/wiki.py show 27821104 "確認|デッキ"
```
