import streamlit as st
import json
import os
from video_skill import create_skill, VISUAL_STYLES

st.set_page_config(
    page_title="视频号脚本生成器",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 视频号内容化营销脚本生成器")
st.markdown("---")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    # 自动从环境变量读取 API Key
    default_key = os.environ.get("GEMINI_API_KEY", "")
    api_key = st.text_input("API Key", value=default_key, type="password", help="输入 Gemini API Key 或设置环境变量 GEMINI_API_KEY")

    st.header("📤 上传")
    uploaded_file = st.file_uploader("上传脚本 JSON", type=["json"], help="上传已有的脚本文件")

    if uploaded_file:
        try:
            uploaded_script = json.load(uploaded_file)
            st.success(f"✅ 已加载 {len(uploaded_script)} 个分镜")
        except:
            st.error("❌ JSON 格式错误")

# 主界面 - Tabs
tab1, tab2 = st.tabs(["📝 脚本生成", "✏️ 脚本编辑"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        node = st.text_input("📌 营销节点", placeholder="如：618、双11、年货节")
    with col2:
        style_options = {k: v["name"] for k, v in VISUAL_STYLES.items()}
        style_key = st.selectbox("🎨 视觉风格", options=list(style_options.keys()), format_func=lambda x: style_options[x])

    product = st.text_area("📝 产品/场景描述", placeholder="描述产品特点或使用场景...", height=80)

    if st.button("🚀 AI 生成脚本", type="primary", use_container_width=True):
        if not api_key:
            st.error("⚠️ 请先输入 API Key")
        elif not product:
            st.error("⚠️ 请输入产品描述")
        else:
            with st.spinner("🚀 正在生成脚本..."):
                try:
                    skill = create_skill(api_key=api_key)
                    script = skill.generate(product, style_key)
                    st.session_state["current_script"] = script
                    st.success("✅ 脚本生成成功！")
                except Exception as e:
                    st.error(f"❌ 生成失败：{str(e)}")

with tab2:
    st.subheader("✏️ 脚本编辑区")

    # 初始化 session_state
    if "current_script" not in st.session_state:
        st.session_state["current_script"] = []

    # 从上传文件加载
    if uploaded_file:
        try:
            st.session_state["current_script"] = uploaded_script
        except:
            pass

    # 脚本编辑器
    if st.session_state["current_script"]:
        edited_script = []
        for i, scene in enumerate(st.session_state["current_script"]):
            with st.expander(f"📹 {scene.get('scene_no', f'第{i+1}镜')}", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    scene["scene_no"] = st.text_input("镜头序号", value=scene.get("scene_no", ""), key=f"no_{i}")
                    scene["duration"] = st.text_input("时长", value=scene.get("duration", ""), key=f"dur_{i}")
                    scene["visual_description"] = st.text_area("画面描述", value=scene.get("visual_description", ""), height=60, key=f"vis_{i}")
                    scene["voiceover"] = st.text_input("口播文案", value=scene.get("voiceover", ""), key=f"vo_{i}")
                with col_b:
                    scene["ai_prompt"] = st.text_area("AI 指令", value=scene.get("ai_prompt", ""), height=100, key=f"ai_{i}")
                    scene["action_hint"] = st.text_input("行动引导", value=scene.get("action_hint", ""), key=f"act_{i}")
                edited_script.append(scene)

        st.session_state["current_script"] = edited_script

        # 操作按钮
        col1, col2, col3 = st.columns(3)
        with col1:
            json_str = json.dumps(edited_script, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 下载 JSON",
                data=json_str,
                file_name=f"视频脚本_{node or '编辑'}.json",
                mime="application/json"
            )
        with col2:
            if st.button("🗑️ 清空脚本"):
                st.session_state["current_script"] = []
                st.rerun()
        with col3:
            if st.button("➕ 添加分镜"):
                st.session_state["current_script"].append({
                    "scene_no": f"第{len(edited_script)+1}镜",
                    "duration": "2秒",
                    "visual_description": "",
                    "ai_prompt": "",
                    "voiceover": "",
                    "action_hint": ""
                })
                st.rerun()
    else:
        st.info("👆 暂无脚本，请先 AI 生成或上传 JSON 文件")

# 底部说明
st.markdown("---")
st.caption("💡 提示：口播文案中的 *文字* 表示重音节点 | 视频时长：10-15秒 | 上传 JSON 可直接编辑")
