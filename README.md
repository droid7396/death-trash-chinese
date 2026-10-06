# 死亡垃圾-简体中文MOD

非官方社区简体中文翻译,基于官方语言 MOD 系统制作,覆盖游戏全部 6,878 条文本(对话、任务、物品、书籍、界面)。

- 目标版本:Death Trash v0.14.6.1(Steam 抢先体验)
- 当前状态:全量翻译完成,并经过术语一致性与占位符完整性校对
- 平台:Windows / Linux(Steam Deck)/ Mac,文本 MOD 无平台差异

> 本 MOD 仅替换文本,不修改任何游戏文件,不影响存档;停用后游戏恢复英文。

## 安装

1. 下载本仓库 `ChineseLanguageMod` 文件夹(可从 Release 下载打包版);
2. 将其复制到游戏数据目录:

   ```
   C:\Users\<用户名>\AppData\LocalLow\Crafting Legends\Death Trash\Mods\ChineseLanguageMod\
   ```

   快速打开:按 `Win + R` 输入 `%userprofile%\AppData\LocalLow\Crafting Legends\Death Trash\Mods`
3. 启动游戏 → 主菜单 **Mods** → 启用 **Simplified Chinese Translation**;
4. 若文本仍为英文,在语言设置中切换到中文。

详细说明(含目录结构图)见 [ChineseLanguageMod/安装说明.md](ChineseLanguageMod/安装说明.md)。

## 已知限制

- **字体**:游戏自带动态字体为韩文/日文字体(Noto Sans KR、PixelMplus12),不含全部简体字形。Windows 下系统字体可兜底,个别简体字可能缺失;Steam Deck 上依赖 Proton/SteamOS 字体回退,显示效果不保证。字体补丁在计划中。

## 跟进游戏更新

游戏每次更新会新增文本。重新生成与补译流程已工具化:

```bash
# 1. 游戏内(调试控制台 Shift+F10)导出最新语言文件 newLanguage.tsv
# 2. 重新划分批次(会重置未翻译状态,已翻译内容自动保留)
python prepare_batches.py
# 3. 补译新增批次(写入 translations/trans_XXX.json)
# 4. 重新构建 MOD 文件
python build_mod4.py
# 5. 术语与格式校对
python proofread.py
```

构建脚本按行索引精确回写译文(`build_mod4.py`),并自动校验原文一致性。

## 参与贡献

欢迎 PR:

- **校对**:直接修改 `translations/trans_XXX.json` 中对应条目的 `dst`(索引 `si/ei` 与 `structure.json` 对应原文),改完运行 `build_mod4.py` 重新生成;
- **术语**:术语表见 [glossary.md](glossary.md),世界观设定见 [worldview.md](worldview.md),新增译名请同步更新;
- 翻译风格:口语化、黑色幽默适度保留;摩罗肉铺用破碎的全大写语体,圣主优雅家长式,失败改造人电报断句,圣主之塔改造人复读尾词——这些刻意的语体请在译文中保留。

## 许可

- 本仓库中的脚本以 [MIT License](LICENSE) 发布;
- `chinese.tsv` 中保留的英文原文版权归 [Crafting Legends](https://www.deathtrash.com) 所有;
- 本 MOD 为非官方作品,与 Crafting Legends 无隶属关系;使用后果自负。
