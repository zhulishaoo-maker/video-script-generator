# 视频号内容化营销脚本生成规则

## 核心定位

将产品或场景包装成微信视频号适用的内容化营销短视频脚本。脚本要像生活经验、使用提案或真实场景观察，而不是传统硬广。

## 视频结构

默认生成 10-15 秒脚本，建议 3-5 个镜头。

1. 吸睛开头，第 1-3 秒：
   - 用视觉冲突、生活痛点、反常识观察或强场景切入。
   - 禁止上来就喊促销、价格、福利。
2. 场景植入，第 4-10 秒：
   - 展示产品如何进入真实生活场景。
   - 让卖点通过动作、细节、对比、用户状态变化自然出现。
3. 强力钩子，第 11-15 秒：
   - 引导评论、收藏、了解、试试同款做法。
   - 避免强迫购买和夸张承诺。

## 视觉风格

支持以下默认风格：

1. 真实场景拍摄：realistic photography, on-location shooting, natural lighting, authentic atmosphere
2. 3D 黏土风格：3D Claymorphism, clay animation style, cute sculptural characters, soft textures, vibrant colors
3. 产品静帧展示：product photography, clean background, studio lighting, minimalist composition
4. 手绘插画风：hand-drawn illustration style, watercolor texture, animated brush strokes, artistic
5. 生活纪录片：documentary style, handheld camera, natural color grading, slice-of-life, candid

## 字段标准

- `scene_no`：使用“第1镜”“第2镜”等编号。
- `duration`：使用“2秒”“3秒”等中文时长。
- `visual_description`：中文，描述具体画面、动作、人物、环境或产品出现方式。
- `ai_prompt`：英文，包含主体、动作、场景、镜头、光线、风格关键词。
- `voiceover`：中文，口语化，重点词用 `*重音*` 标注。
- `action_hint`：中文，轻量互动引导。

## 文案风格

- 口语化，像朋友在微信里分享。
- 使用“生活提案”“经验分享”“我发现一个办法”的语气。
- 重点表现生活变化，不堆砌参数。
- 优先写具体场景，不写空泛价值观。

## 敏感词和风险表达

严禁使用：

- 秒杀
- 最
- 第一
- 全网最低
- 销量冠军
- 后悔药
- 亏本
- 立即抢购
- 限时特价
- 库存有限
- 买到就是赚到
- 无敌
- 顶级

避免使用：

- 保证、永久、彻底、根治、官方认证、平台背书。
- 未经用户提供依据的销量、排名、价格、成分功效和医学效果。
- 诱导式购买压力和过度焦虑表达。

## 验收标准

- JSON 可解析，无 Markdown 代码围栏时也能直接导入工具。
- 总时长合理，镜头之间有清晰起承转合。
- 每个镜头都能被视频生成模型理解。
- 没有敏感词、极限词或不可证实承诺。
- 输出内容符合视频号内容化营销语气。
