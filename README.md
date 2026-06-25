# 视频号内容化营销脚本生成器

基于 AI 的视频号营销脚本生成工具，支持：

- 🎬 AI 生成视频脚本（Poe / Gemini / OpenAI / Anthropic / MiniMax）
- 🎨 多种视觉风格选择
- ✏️ 脚本在线编辑
- 📤 JSON 导入导出
- 📹 支持即梦、Lovart 等视频生成工具

## 本地运行

```bash
pip install -r requirements.txt

# 设置 API Key（推荐 Poe）
export POE_API_KEY="your-api-key"

# 启动网页应用
streamlit run app.py
```

命令行生成：

```bash
python main.py \
  --node "年货节" \
  --product "强效洗衣液，去除顽固污渍，适合有孩子的家庭" \
  --provider poe
```

也可以继续使用其他服务商：

```bash
export GEMINI_API_KEY="your-api-key"
python main.py --node "618" --product "产品描述" --provider gemini
```

## 在线部署

一键部署到 Streamlit Cloud：

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

## 视觉风格

1. 真实场景拍摄
2. 3D 黏土风格
3. 产品静帧展示
4. 手绘插画风
5. 生活纪录片

## 视频结构

- 吸睛开头（第1-3秒）
- 场景植入（第4-10秒）
- 强力钩子（第11-15秒）
