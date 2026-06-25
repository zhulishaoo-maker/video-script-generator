---
name: video-script-generator
description: Generate WeChat Video Account content-marketing short video scripts from product or campaign inputs, including scene breakdowns, voiceover, English AI video prompts, visual style selection, and compliance checks for Chinese marketing language.
---

# 视频号内容化营销脚本生成器

## 触发条件

当用户要求生成、改写、优化或批量生产以下内容时，使用本 Skill：

- 微信视频号、短视频、种草视频、内容化营销脚本。
- 电商节点视频脚本，例如 618、双11、年货节、开学季。
- 可交给即梦、Lovart、Sora、Veo、Seedance、Wan 等视频生成工具的分镜 Prompt。
- 包含镜头时长、画面描述、口播、互动引导的 JSON 脚本。

## 任务边界

本 Skill 负责创意脚本和结构化分镜，不负责：

- 直接发布内容。
- 代替法务、平台规则、广告审核结论。
- 生成具体价格、库存、销量、疗效、资质承诺，除非用户提供了可核验素材且仍需标注人工审核。

## 读取顺序

1. 先读用户输入，识别产品、场景、营销节点、目标人群、视觉风格和输出格式。
2. 如需详细规则，读取 `references/rules.md`。
3. 如用户要求标准样例或格式对齐，读取 `examples/output-01.md`。
4. 如需要运行本地工具，使用仓库中的 `video-script-generator/main.py` 或 `video-script-generator/app.py`。

## 执行步骤

1. 明确产品或场景的生活痛点，避免硬广开头。
2. 选择视觉风格；未指定时使用“真实场景拍摄”。
3. 按黄金 15 秒结构拆分 3-5 个镜头：
   - 第 1-3 秒：吸睛开头，用视觉冲突或真实痛点切入。
   - 第 4-10 秒：场景植入，展示产品如何解决具体问题。
   - 第 11-15 秒：强力钩子，引导互动、收藏、评论或进一步了解。
4. 为每个镜头生成中文画面描述、英文 AI Prompt、中文口播和行动引导。
5. 检查敏感词、极限词和不可证实承诺。
6. 输出标准 JSON 数组；除非用户要求解释，否则不要在 JSON 外添加长篇说明。

## 输出要求

默认输出 JSON 数组：

```json
[
  {
    "scene_no": "第1镜",
    "duration": "2秒",
    "visual_description": "具体视觉动作",
    "ai_prompt": "English video generation prompt with selected visual style",
    "voiceover": "中文口播，标注*重音*",
    "action_hint": "互动引导"
  }
]
```

质量标准：

- 总时长控制在 10-15 秒。
- 每个镜头动作具体，可拍摄、可生成、可剪辑。
- `ai_prompt` 使用英文，并包含主体、场景、动作、镜头、光线、风格。
- 口播自然口语化，像朋友分享经验。
- 互动引导克制，不使用强迫下单式语言。

## 禁止事项

- 不使用：秒杀、最、第一、全网最低、销量冠军、后悔药、亏本、立即抢购、限时特价、库存有限、买到就是赚到、无敌、顶级。
- 不写“保证有效”“永久解决”“官方认证”“平台第一”等无法证明的表达。
- 不把产品直接写成医疗、金融或安全承诺。
- 不输出无法解析的 JSON，除非用户明确要求 Markdown 表格或普通文案。

## 本地工具

如果需要调用仓库实现：

```bash
cd video-script-generator
python3 main.py --node "年货节" --product "产品描述" --provider poe
```

默认推荐环境变量：

```bash
export POE_API_KEY="your-api-key"
```
