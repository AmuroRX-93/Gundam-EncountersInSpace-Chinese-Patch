# Encounter in Space ALLPLATFORM 1.0

《机动战士高达 相逢在宇宙》中文 **1.0 正式发布版**。PS2 日版 SLPS-25062，原盘修订 1.03。

[下载正式版 1.0](https://github.com/AmuroRX-93/Gundam-EncountersInSpace-Chinese-Patch/releases/tag/v1.0)

## 下载与安装

**下载下面所有 `Encounter_in_Space_ALLPLATFORM_1.0_Delta.7z.00x` 分卷，放在同一目录，从 `.001` 解压。** `SHA256SUMS.txt` 为各分卷校验值；不要把 GitHub 自动生成的 Source code 当成完整安装包。

这是从日版原盘一次升级至 1.0 的累计差分，不需要安装 0.1.0。Windows/macOS/Linux 附 x64/ARM64 六套内置 Python、安装脚本、许可和完整说明，不需自行安装 Python/pip。安卓附标准 XDelta 路径，也可导入电脑合成的 ISO；PS2 实机部署同一份 ISO。

1. 完整解压，Windows 双击 `Windows_安装.cmd`，macOS 双击 `macOS_安装.command`，Linux 执行 `sh run.sh`。
2. 选 1，选择匹配校验值的日版原盘 ISO，等待生成与完整校验。
3. 新 ISO 默认生成在原盘旁边，名称为 `Encounter_in_Space_ALLPLATFORM_1.0.iso`。选择新 ISO 正常开机，保留原记忆卡，不使用旧即时存档判断新补丁。

## 本次内容

沿用菜单/说明与部分 UI 中文化、影片中文字幕、67 人物片资源/72 段出击字幕及战斗通讯字幕；更新后的 ADI 字幕共 4703 条。相对旧发布基线修订 50 条字幕，补一处空字幕为近似笑声，并新增“羽”“躺”字形。保留原日语音频、每行 16 全角字宽/两行分页、出击字幕延长及结算文字修订。

## 验证边界

电脑内置 Apple Silicon Python 和标准 XDelta 两条路径均从原盘完整重建，目标 SHA256 一致；安装保护检查、压缩包干净解压及每个文件摘要校验通过。其他五种电脑架构提供运行环境及入口，但未在对应机器实跑。安卓大文件修补和 PS2 实机运行未实测。

本次按正式版发布，未完成全关卡、全模式运行测试；部分短喊声/近音台词按现有听辨结果定稿，不能视为全部语音人工听审通过。欢迎在 Issues 提交关卡、触发步骤、截图/短片，继续修订漏译、译文和字幕时序。

## ISO 指纹

输入、输出均为 4,643,094,528 字节。大于 4 GiB，不能直接写入 FAT32；7z 分卷不是可运行的游戏分片。

- 原盘：`12860f3d66fccdcecc2b7fbdbbe98082e94a769b4f573b9b88050ec103fab46a`
- 中文 1.0：`69c2250dd91cdfd55cd44921419196a4d8fae379009adfd550143149c5e9c6e0`

旧汉化、其他修订、其他地区或 CHD 不作为本差分输入。公开仓库仅提供差分、工具与说明，不上传完整游戏 ISO、BIOS 或个人存档。字体与 Python 来源及许可随包保留。汉化使用 AI 辅助转写、校对和工程处理。

详细中文说明与安装器源码见 [releases/v1.0](releases/v1.0)。源码浏览不替代包含载荷和运行环境的 Release 附件。
