"""
视频号内容化营销脚本生成 Skill
Video Script Generator for WeChat Video Account
"""

import google.generativeai as genai
import json
import re
from typing import Dict, List

DEFAULT_MODEL = "gemini-3.1-flash"

VISUAL_STYLES: Dict[str, Dict[str, str]] = {
    "1": {
        "name": "真实场景拍摄",
        "prompt_keywords": "realistic photography, on-location shooting, natural lighting, authentic atmosphere"
    },
    "2": {
        "name": "3D 黏土风格",
        "prompt_keywords": "3D Claymorphism, clay animation style, cute sculptural characters, soft textures, vibrant colors"
    },
    "3": {
        "name": "产品静帧展示",
        "prompt_keywords": "product photography, clean background, studio lighting, minimalist composition"
    },
    "4": {
        "name": "手绘插画风",
        "prompt_keywords": "hand-drawn illustration style, watercolor texture, animated brush strokes, artistic"
    },
    "5": {
        "name": "生活纪录片",
        "prompt_keywords": "documentary style, handheld camera, natural color grading, slice-of-life, candid"
    }
}

SENSITIVE_WORDS = [
    "秒杀", "最", "第一", "全网最低", "销量冠军",
    "后悔药", "亏本", "立即抢购", "限时特价",
    "库存有限", "买到就是赚到", "无敌", "顶级"
]


class VideoScriptSkill:
    """视频号内容化营销脚本生成 Skill"""

    def __init__(self, api_key: str, model_name: str = DEFAULT_MODEL):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def get_styles(self) -> Dict[str, str]:
        """返回所有视觉风格选项"""
        return {k: v["name"] for k, v in VISUAL_STYLES.items()}

    def get_style_info(self, style_key: str) -> Dict[str, str]:
        """返回指定风格的详细信息"""
        return VISUAL_STYLES.get(style_key, VISUAL_STYLES["1"])

    def _clean_response(self, text: str) -> str:
        """清理 AI 返回内容，提取干净 JSON"""
        text = text.strip()
        if text.startswith("```"):
            parts = text.split("```")
            for part in parts:
                if part.strip().startswith("["):
                    return part.strip()
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return match.group(0)
        raise ValueError("无法解析 AI 返回内容")

    def _build_prompt(self, product_info: str, style: Dict[str, str]) -> str:
        """构建生成脚本的 Prompt"""
        return f"""
角色：你是一个深谙微信视频号生态的内容化营销导演。

任务：为以下产品/场景制作 10-15 秒的内容化营销短视频脚本。
产品/场景：{product_info}

【视觉风格】
风格名称：{style['name']}
AI 生成关键词：{style['prompt_keywords']}

【视频结构 - 黄金 15 秒】
1. 吸睛开头（第1-3秒）：视觉冲突或生活痛点切入，禁止硬广开头
2. 场景植入（第4-10秒）：展示产品如何解决具体场景问题
3. 强力钩子（第11-15秒）：行动指令，引导互动

【语言风格】
- 口语化，像老朋友在微信聊天
- 以"生活提案"或"经验分享"口吻
- 口播文案标注*重音*点

【敏感词约束】
严禁出现：{', '.join(SENSITIVE_WORDS)}

【输出格式】
返回标准 JSON 数组：
[
    {{
        "scene_no": "第1镜",
        "duration": "2秒",
        "visual_description": "具体视觉动作",
        "ai_prompt": "英文 Prompt，融入{style['name']}风格",
        "voiceover": "口播文案，标注*重音*",
        "action_hint": "互动引导"
    }}
]
"""

    def generate(self, product_info: str, style_key: str = "1") -> List[Dict]:
        """
        生成视频脚本

        Args:
            product_info: 产品/场景描述
            style_key: 视觉风格编号，默认 "1"

        Returns:
            脚本列表，每个元素是一个分镜
        """
        style = self.get_style_info(style_key)
        prompt = self._build_prompt(product_info, style)

        response = self.model.generate_content(prompt)
        json_str = self._clean_response(response.text)

        return json.loads(json_str)

    def generate_with_retry(self, product_info: str, style_key: str = "1", max_retries: int = 3) -> List[Dict]:
        """带重试的生成方法"""
        for attempt in range(max_retries):
            try:
                return self.generate(product_info, style_key)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"⚠️ 生成失败，尝试第 {attempt + 2} 次...")
        return []


def create_skill(api_key: str, model_name: str = DEFAULT_MODEL) -> VideoScriptSkill:
    """创建 Skill 实例的便捷函数"""
    return VideoScriptSkill(api_key=api_key, model_name=model_name)