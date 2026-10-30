# OfficeCLI 独立技能仓库

2026-10-30 本地快照，包含以下三个独立技能。每个技能保留自己的名称、`SKILL.md` 和所需文件，可以分别安装；本仓库不是一个合并后的技能。

| 技能 | 用途 | 随包文件 |
| --- | --- | --- |
| `officecli` | Word、Excel、PowerPoint 的 CLI 操作入口 | `SKILL.md` |
| `officecli-docx` | Word 的结构、编辑、域、渲染与交付检查 | `SKILL.md` |
| `officecli-thesis-gate` | 中文论文及用户明确指定的测试交付文档格式门禁 | `SKILL.md`、两个 SVG 处理脚本 |

仓库：[`CurtisJiang3/officecli-skills`](https://github.com/CurtisJiang3/officecli-skills)，公开开源，任何人都可以查看、克隆并分别安装三个技能。

三个独立安装路径分别为：

- [`skills/officecli`](https://github.com/CurtisJiang3/officecli-skills/tree/main/skills/officecli)
- [`skills/officecli-docx`](https://github.com/CurtisJiang3/officecli-skills/tree/main/skills/officecli-docx)
- [`skills/officecli-thesis-gate`](https://github.com/CurtisJiang3/officecli-skills/tree/main/skills/officecli-thesis-gate)

本包保留本地技能正文，未用网上最新版覆盖。文件清单和 SHA-256 见 `manifest.json`。本机核对时的 OfficeCLI 版本为 **1.0.159**；这是核对环境记录，不是对其他版本的兼容性保证。命令语法以实际安装版本的 `officecli help` 为准。

## 换一台电脑需要什么

**本包已经包含 officecli 技能，无需再单独下载同名技能。OfficeCLI 可执行程序仍需在每台电脑安装。** `git pull` 只更新仓库文件，不会自动安装程序，也不会自动把普通 `skills/` 目录注册成全局技能。

| 依赖 | 何时需要 |
| --- | --- |
| OfficeCLI 可执行程序及可用的 PATH | 读取、创建、编辑、校验 Office 文件 |
| Codex 能发现的技能目录 | 使用本包的工作流和格式规范 |
| Python 3 | 运行论文技能的两个 SVG 处理脚本；脚本仅使用标准库，无需 pip 安装依赖 |
| 文档要求的字体 | 保证宋体、黑体、Times New Roman 等字体的实际显示和分页 |
| Windows + Microsoft Word | 本论文规范要求的 Word 原生分页、域更新和逐页视觉核验；其他环境可编辑文件，但不能据此宣称通过这一门禁 |
| draw.io 或相应 MCP 工具 | 需要绘制、修改可编辑 draw.io 插图时；此包不包含 MCP 配置 |

### 1. 安装或验证 OfficeCLI 程序

先执行 `officecli --version`。缺少程序时，按 [OfficeCLI 官方安装说明](https://github.com/iOfficeAI/OfficeCLI#for-developers--see-it-live-in-30-seconds) 安装：

Windows PowerShell：

```powershell
irm https://d.officecli.ai/install.ps1 | iex
officecli --version
```

macOS / Linux：

```bash
curl -fsSL https://d.officecli.ai/install.sh | bash
officecli --version
```

若安装后当前终端仍找不到命令，打开新终端再验证。官方安装流程可能部署上游技能；随后再安装本包，确保加载的是本次快照。无需额外运行会配置所有 Agent/MCP 的 `officecli install`。

### 2. 安装本包技能

先下载本仓库，或用 Git 克隆；读取公开仓库无需登录 GitHub：

```bash
git clone https://github.com/CurtisJiang3/officecli-skills.git
cd officecli-skills
```

Windows：在仓库或完整包所在目录运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

默认复制到当前用户的 `~/.agents/skills`。已有同名技能会先备份到 `~/.agents/skill-backups`，然后整体替换，避免上游旧版的额外文件混入。脚本支持 `-WhatIf` 预览，以及 `-TargetRoot` 指定目录；不会安装程序或改动 MCP 配置。

只安装其中一个技能时使用 `-Skill`；例如：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Skill officecli-thesis-gate
```

也可只下载所需技能的完整目录，并放入 `~/.agents/skills/`。论文门禁是 OfficeCLI 的补充规范；单独安装它不会附带 OfficeCLI 程序或另外两个技能。

macOS / Linux：把 `skills/` 中三个完整目录安装到 `~/.agents/skills/`；如果已有同名目录，先将旧目录备份到技能扫描目录之外，再复制。不要只复制论文技能的 `SKILL.md`，否则会缺两个脚本。

Codex 的全局用户目录和仓库内目录规则见 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。若只希望当前项目使用，可将三个完整目录放入该项目的 `.agents/skills/`。不要在多个扫描目录同时保留同名技能；Codex 不会把它们合并。新技能未出现时，重启 Codex。

### 3. 日常更新

拉取本包所在仓库的新版本后，再运行安装脚本，将更新复制到用户技能目录。若采用项目内 `.agents/skills/` 的版本管理方式，拉取就会更新技能文件，但程序、字体等环境依赖仍需单独具备。

## 配合使用

- 普通 Word 文件：使用 OfficeCLI 操作规则与 DOCX 指南，保留原模板和本次任务要求。
- 中文论文或明确指定按论文规范排版的测试交付文档：再应用 `officecli-thesis-gate` 的专用规范。其标题字号、三线表、目录等具体规则优先于通用 DOCX 的默认设计建议。
- OfficeCLI 自带的 `load_skill` 按主技能的路由规则选择一种对应的格式或场景指南；论文门禁是附加格式规范，不代替命令帮助。
- 本包中的 Bash 示例不应直接粘贴到 PowerShell。Windows 下使用 PowerShell 等价写法，并在参数不确定时查询 CLI help。

## 本次整理范围与历史依据

这是这三个技能的首次 Git 提交，内容来自本机已安装版本。已找到 2026-09-28 创建论文门禁的聊天记录及当日导出快照；当前论文门禁相对该快照新增或细化了：

- 目录二级条目常规字重、一个汉字宽的缩进，以及更新目录后的复查。
- 二级标题的中西文字体，以及表格居中、表头和数据行行距、跨页续表要求。
- 章节导语、本章小结及单一主题短章节的例外。
- 插图必要性、黑白制图、符号、箭头落点、Word 中的物理字号与 SVG 处理。
- 分页、页尾留白及逐页核验。

此次将当前三个独立技能、两个 SVG 脚本和安装说明首次纳入版本管理。上述历史比较依据是本地导出快照，不是之前的 Git 提交差异。后续更新可通过本仓库提交记录追溯。

## SVG 脚本调用

```bash
python skills/officecli-thesis-gate/scripts/prepare_drawio_svg.py exported.svg clean.svg
python skills/officecli-thesis-gate/scripts/style_drawio_svg.py clean.svg word.svg --word-width-cm 15 --font-pt 12
```

`--word-width-cm` 必须等于图片在 Word 中的实际宽度。保留原始 `.drawio` 和导出 SVG；两个脚本都禁止原地覆盖输入。脚本成功仅表示预处理完成，最终仍需在 Word 页面中核验。

## 打包验证

三个技能均通过 skill-creator 的结构校验；五个技能与脚本文件和本机原件逐字节一致。已在隔离临时目录验证 Windows 安装、更新备份、旧文件隔离、`-WhatIf` 和源目录重叠保护。两个 SVG 脚本已用样例验证提示层清理、原件保留、实际白底、中西文字体和插入宽度对应的物理字号。此处验证的是技能包及其辅助脚本，不代表某份论文已经通过门禁。

## 开源许可与上游来源

本仓库采用 **Apache-2.0** 开源许可，见 [`LICENSE`](LICENSE)。本地自定义论文规范、辅助脚本、安装脚本和说明也按此许可提供，归属声明见 [`NOTICE`](NOTICE)。

OfficeCLI 的上游项目是 [iOfficeAI/OfficeCLI](https://github.com/iOfficeAI/OfficeCLI)。保留上游的原始许可和归属声明，分别见 `LICENSE-OfficeCLI.txt` 与 `NOTICE-OfficeCLI.txt`。
