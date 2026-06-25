# 背景说明

## 适用范围

本 Skill 面向微信视频号、电商短视频、品牌内容种草、AI 视频生成前置脚本等场景。

## 核心概念

- 内容化营销：用真实场景、生活经验或情绪洞察承载卖点，而不是直接硬广。
- 分镜脚本：按镜头拆解画面、时长、口播、Prompt 和互动引导。
- AI Prompt：给视频生成模型使用的英文画面指令。
- 黄金 15 秒：用短时长完成吸睛、植入、互动钩子三个阶段。

## 工具关系

- `video-script-generator/video_skill.py`：脚本生成核心逻辑。
- `video-script-generator/app.py`：Streamlit 图形界面。
- `video-script-generator/main.py`：命令行入口。
- `.agents/skills/video-script-generator/`：符合录入标准的可复用 Skill 说明层。
