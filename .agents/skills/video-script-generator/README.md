# 视频号内容化营销脚本生成器

## 基础信息

- 提交人：zhulisha
- 维护人：zhulisha
- 来源：video-script-generator 仓库、本地 `video_skill.py` 实现、录入 Skill 标准 PDF
- 所属业务域：营销域 / 多媒体内容域
- 当前状态：进行中 v0.1

## 用途

这个 Skill 用于把产品、场景或营销节点转化为 10-15 秒微信视频号内容化营销短视频脚本，输出可直接给即梦、Lovart、视频生成模型或人工剪辑团队使用的分镜 JSON。

## 适用场景

- 为电商大促、节日节点、品牌活动快速生成视频号短视频脚本。
- 将产品卖点包装成生活提案、经验分享、场景化种草内容。
- 为 AI 视频生成工具准备英文画面 Prompt、中文口播、镜头时长和互动引导。
- 需要在生成内容中规避夸大宣传、极限词和硬广开头。

## 输入

用户需要提供：

- 产品或场景描述。
- 营销节点，可选，例如 618、双11、年货节。
- 视觉风格，可选，默认真实场景拍摄。
- API provider 和 API Key，可选，默认推荐 Poe API。

## 输出

Skill 会产出标准 JSON 数组，每个元素是一条分镜，包含：

- `scene_no`：镜头编号。
- `duration`：镜头时长。
- `visual_description`：中文画面描述。
- `ai_prompt`：英文视频生成 Prompt。
- `voiceover`：中文口播文案，重要词用 `*重音*` 标注。
- `action_hint`：互动或行动引导。

## 依赖资料

- `references/rules.md`：脚本生成规则、敏感词约束、输出格式标准。
- `examples/input-01.md`：示例输入。
- `examples/output-01.md`：标准输出样例。
- `video-script-generator/video_skill.py`：可运行的 Python 实现。

## 边界和风险

- 不生成医疗、金融、功效承诺等高风险断言。
- 不使用“秒杀”“最”“第一”“全网最低”等敏感或极限表达。
- 不承诺真实库存、价格、销量、平台认证或官方背书。
- 输出脚本用于创意生产，发布前必须由业务、法务或运营人工审核。

## 可选补充

- 体验方式：`streamlit run app.py`
- 命令行方式：`python main.py --node "年货节" --product "产品描述" --provider poe`
