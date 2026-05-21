import streamlit as st
import json
import os
import subprocess
from video_skill import create_skill, VISUAL_STYLES, MODEL_CONFIG

# ========== 自定义样式 ==========
st.markdown("""
<style>
    :root {
        --primary: #FF6B6B;
        --secondary: #4ECDC4;
        --accent: #FFE66D;
        --dark: #2C3E50;
        --light: #F7F9FC;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2C3E50;
        text-align: center;
        padding: 1rem 0;
    }
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
    }
    .tag {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
    }
    .scene-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .stButton > button {
        border-radius: 25px;
        font-weight: 600;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,107,107,0.4);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F7F9FC 0%, #EEF1F5 100%);
    }
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ddd, transparent);
    }
    .script-item {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 5px solid #FF6B6B;
    }
    .ai-prompt {
        background: #1a1a2e;
        color: #00ff88;
        font-family: 'Courier New', monospace;
        padding: 1rem;
        border-radius: 10px;
        font-size: 0.85rem;
    }
    .voiceover {
        background: linear-gradient(135deg, #fff5f5, #fff0f0);
        border-left: 4px solid #FF6B6B;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
        font-weight: 500;
    }
    .video-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    .status-success { color: #27ae60; font-weight: 600; }
    .status-pending { color: #f39c12; font-weight: 600; }
    .status-fail { color: #e74c3c; font-weight: 600; }
    div[data-testid="stHorizontalBlock"] button {
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    div[data-testid="stHorizontalBlock"] button:focus,
    div[data-testid="stHorizontalBlock"] button:active {
        border-color: #FF6B6B !important;
        background: linear-gradient(135deg, #FF6B6B, #FF8E53) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="🎬 视频号脚本生成器",
    page_icon="🎬",
    layout="wide"
)

# ========== 标题区 ==========
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 2.8rem; font-weight: 800; color: #2C3E50; margin: 0;">
        🎬 视频号内容化营销脚本生成器
    </h1>
    <p style="color: #7f8c8d; font-size: 1.1rem; margin-top: 0.5rem;">
        AI 驱动的短视频脚本创作平台 | 支持多模型生成 | 即梦视频直出
    </p>
</div>
""", unsafe_allow_html=True)


def run_dreamina(cmd: list) -> tuple:
    """执行 dreamina 命令，返回 (success, output)"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return True, result.stdout
        return False, result.stderr
    except Exception as e:
        return False, str(e)


def parse_submit_id(output: str) -> str:
    """从输出中提取 submit_id"""
    import re
    match = re.search(r'submit_id["\s:]+([a-zA-Z0-9-]+)', output)
    if match:
        return match.group(1)
    match = re.search(r'id["\s:]+([a-zA-Z0-9-]+)', output)
    if match:
        return match.group(1)
    return ""


# ========== 主界面 ==========
col_side, col_main = st.columns([1, 3])

with col_side:
    st.markdown("### ⚙️ 配置")

    # 模型选择
    provider_options = {k: v["name"] for k, v in MODEL_CONFIG.items()}
    provider = st.selectbox("🤖 AI 模型", options=list(provider_options.keys()), format_func=lambda x: provider_options[x])

    # API Key
    env_key = MODEL_CONFIG[provider]["env_key"]
    default_key = os.environ.get(env_key, "")
    api_key = st.text_input(f"🔑 API Key", value=default_key, type="password", help=f"设置 {env_key} 环境变量或直接输入")

    st.markdown("---")

    # 即梦积分
    st.markdown("### 💰 即梦积分")
    success, output = run_dreamina(["dreamina", "user_credit"])
    if success:
        # 解析积分输出
        lines = output.strip().split('\n')
        for line in lines:
            if 'credit' in line.lower() or '积分' in line:
                st.info(line)
                break
        else:
            st.text(output[:200])
    else:
        st.warning("请先登录即梦：dreamina login")

    st.markdown("---")

    # 上传
    st.markdown("### 📤 脚本管理")
    uploaded_file = st.file_uploader("上传 JSON", type=["json"], help="上传已有脚本")

    if uploaded_file:
        try:
            uploaded_script = json.load(uploaded_file)
            st.success(f"✅ 已加载 {len(uploaded_script)} 个分镜")
        except:
            st.error("❌ JSON 格式错误")

with col_main:
    tab1, tab2, tab3 = st.tabs(["🎬 脚本生成", "✏️ 脚本编辑", "🎥 视频生成"])

    with tab1:
        st.markdown("#### 📝 输入产品信息")

        col1, col2 = st.columns([2, 1])
        with col1:
            product = st.text_area(
                "产品/场景描述",
                placeholder="描述产品特点或使用场景，例如：强效洗衣液，去除顽固污渍，适合有孩子的家庭...",
                height=100,
                label_visibility="collapsed"
            )
        with col2:
            node = st.text_input("营销节点", placeholder="如：618、年货节", label_visibility="collapsed")

        # 风格选择
        st.markdown("##### 🎨 视觉风格")
        if "selected_style" not in st.session_state:
            st.session_state["selected_style"] = "1"
        style_cols = st.columns(5)
        for idx, (key, style) in enumerate(VISUAL_STYLES.items()):
            with style_cols[idx]:
                is_selected = st.session_state["selected_style"] == key
                btn_type = "primary" if is_selected else "secondary"
                if st.button(f"🎯 {style['name']}", key=f"style_{key}", type=btn_type, use_container_width=True):
                    st.session_state["selected_style"] = key
                    st.rerun()

        st.markdown("---")

        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            generate_btn = st.button("🚀 一键生成脚本", type="primary", use_container_width=True)

        if generate_btn:
            if not api_key:
                st.error("⚠️ 请先输入 API Key")
            elif not product:
                st.error("⚠️ 请输入产品描述")
            else:
                with st.spinner("🔮 AI 正在创作..."):
                    try:
                        skill = create_skill(api_key=api_key, provider=provider)
                        script = skill.generate(product, st.session_state["selected_style"])
                        st.session_state["current_script"] = script
                        st.session_state["current_provider"] = provider

                        st.success(f"✅ 脚本生成成功！使用 {MODEL_CONFIG[provider]['name']}")

                        st.markdown("#### 📋 生成结果")
                        for scene in script:
                            with st.container():
                                st.markdown(f"""
                                <div class="script-item">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <h4 style="margin: 0; color: #2C3E50;">📹 {scene.get('scene_no', '第X镜')}</h4>
                                        <span style="background: #FF6B6B; color: white; padding: 0.2rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                                            ⏱️ {scene.get('duration', 'N/A')}
                                        </span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.markdown("**🖼️ 画面描述**")
                                    st.info(scene.get('visual_description', ''))
                                    st.markdown("**🎤 口播文案**")
                                    st.markdown(f"<div class='voiceover'>{scene.get('voiceover', '')}</div>", unsafe_allow_html=True)

                                with col_b:
                                    st.markdown("**✨ AI 指令**")
                                    prompt_text = scene.get('ai_prompt', '')
                                    st.code(prompt_text, language="")
                                    if st.button(f"🎬 生成视频", key=f"gen_{scene.get('scene_no', '')}"):
                                        with st.spinner("⏳ 提交到即梦..."):
                                            cmd = ["dreamina", "text2video", f"--prompt={prompt_text}", "--ratio=16:9", "--duration=5"]
                                            success, output = run_dreamina(cmd)
                                            if success and "submit_id" in output:
                                                submit_id = parse_submit_id(output)
                                                st.session_state["last_submit_id"] = submit_id
                                                st.success(f"✅ 视频生成任务已提交！ID: {submit_id}")
                                                # 存储到场景
                                                if "video_tasks" not in st.session_state:
                                                    st.session_state["video_tasks"] = {}
                                                st.session_state["video_tasks"][scene.get('scene_no', '')] = submit_id
                                            else:
                                                st.error(f"❌ 提交失败：{output[:200]}")

                                if scene.get('action_hint'):
                                    st.markdown(f"**👆 行动引导**：{scene.get('action_hint', '')}")

                                st.markdown("---")

                        json_str = json.dumps(script, ensure_ascii=False, indent=2)
                        st.download_button("📥 下载完整脚本 JSON", data=json_str, file_name=f"视频脚本_{node or '通用'}.json", mime="application/json")

                    except Exception as e:
                        st.error(f"❌ 生成失败：{str(e)}")

    with tab2:
        st.markdown("#### ✏️ 脚本编辑区")

        if "current_script" not in st.session_state:
            st.session_state["current_script"] = []

        if uploaded_file:
            try:
                st.session_state["current_script"] = uploaded_script
            except:
                pass

        if st.session_state.get("current_script"):
            edited_script = []
            for i, scene in enumerate(st.session_state["current_script"]):
                with st.expander(f"📹 {scene.get('scene_no', f'第{i+1}镜')} - {scene.get('duration', '')}", expanded=True):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        scene["scene_no"] = st.text_input("镜头", value=scene.get("scene_no", ""), key=f"no_{i}")
                        scene["duration"] = st.text_input("时长", value=scene.get("duration", ""), key=f"dur_{i}")
                        scene["visual_description"] = st.text_area("画面", value=scene.get("visual_description", ""), height=70, key=f"vis_{i}")
                        scene["voiceover"] = st.text_input("口播", value=scene.get("voiceover", ""), key=f"vo_{i}")
                    with col_b:
                        scene["ai_prompt"] = st.text_area("AI指令", value=scene.get("ai_prompt", ""), height=90, key=f"ai_{i}")
                        scene["action_hint"] = st.text_input("行动", value=scene.get("action_hint", ""), key=f"act_{i}")
                    edited_script.append(scene)

            st.session_state["current_script"] = edited_script

            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                json_str = json.dumps(edited_script, ensure_ascii=False, indent=2)
                st.download_button("📥 下载", data=json_str, file_name="视频脚本.json", mime="application/json")
            with col2:
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
            with col3:
                if st.button("📋 复制全部"):
                    st.code(json_str, language="json")
            with col4:
                if st.button("🗑️ 清空"):
                    st.session_state["current_script"] = []
                    st.rerun()
        else:
            st.info("👆 暂无脚本，请先在「脚本生成」中创建或上传 JSON 文件")

    with tab3:
        st.markdown("#### 🎥 视频生成管理")

        # 检查登录状态
        success, output = run_dreamina(["dreamina", "user_credit"])
        if not success:
            st.warning("⚠️ 请先在终端登录即梦：`dreamina login`")
        else:
            st.success("✅ 已登录即梦")

        # 查看最近任务
        st.markdown("##### 📜 最近任务")
        success, output = run_dreamina(["dreamina", "list_task", "--gen_status=success", "--limit=5"])
        if success:
            st.text(output[:500] if len(output) > 500 else output)
        else:
            st.info("暂无成功任务")

        # 查询最后一个任务
        if "last_submit_id" in st.session_state:
            st.markdown(f"##### 🔍 查询任务: {st.session_state['last_submit_id']}")
            if st.button("查询结果"):
                with st.spinner("查询中..."):
                    success, output = run_dreamina(["dreamina", "query_result", f"--submit_id={st.session_state['last_submit_id']}"])
                    if success:
                        st.json(output) if output.startswith('{') else st.text(output)
                    else:
                        st.error(output[:200])

        # 手动输入 submit_id 查询
        st.markdown("##### 🔍 手动查询")
        submit_id_input = st.text_input("输入 submit_id", placeholder="粘贴任务ID...")
        if st.button("查询"):
            with st.spinner("查询中..."):
                success, output = run_dreamina(["dreamina", "query_result", f"--submit_id={submit_id_input}"])
                if success:
                    if "video_url" in output or "url" in output:
                        # 提取视频URL
                        import re
                        url_match = re.search(r'https?://[^\s]+', output)
                        if url_match:
                            st.success(f"🎬 视频链接：{url_match.group()}")
                        else:
                            st.text(output[:300])
                    else:
                        st.text(output[:500] if len(output) > 500 else output)
                else:
                    st.error(output[:200])

# ========== 底部说明 ==========
st.markdown("""
---
<div style="text-align: center; color: #95a5a6; font-size: 0.85rem;">
    <p>💡 提示：口播文案中的 <b>*文字*</b> 表示重音节点 | 视频时长：10-15秒 | 支持 Gemini / OpenAI / Anthropic / MiniMax</p>
    <p>🎬 视频号内容化营销脚本生成器 v1.1 | 即梦视频直出</p>
</div>
""", unsafe_allow_html=True)