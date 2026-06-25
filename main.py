import sys
import argparse
import os
from video_skill import create_skill, VISUAL_STYLES, MODEL_CONFIG

def main():
    parser = argparse.ArgumentParser(description="视频号大促脚本制作工具")
    parser.add_argument("--node", required=True, help="营销节点（如：618、双11、年货节）")
    parser.add_argument("--product", required=True, help="产品描述")
    parser.add_argument("--style", default="1", help=f"视觉风格编号 (1-{len(VISUAL_STYLES)})，默认 1")
    parser.add_argument(
        "--provider",
        default="poe",
        choices=MODEL_CONFIG.keys(),
        help="AI 服务商，默认 poe"
    )
    parser.add_argument("--model", help="模型名称，默认使用所选 provider 的配置")
    parser.add_argument("--api-key", help="API Key；不传时读取 provider 对应环境变量")

    args = parser.parse_args()
    provider_config = MODEL_CONFIG[args.provider]
    api_key = args.api_key or os.environ.get(provider_config["env_key"])

    if not api_key:
        print(f"❌ 缺少 API Key：请设置 {provider_config['env_key']} 或传入 --api-key")
        sys.exit(1)

    print(f"\n📌 营销节点：{args.node}")
    print(f"📌 产品：{args.product}")
    print(f"🎨 视觉风格：{args.style}")
    print(f"🤖 AI 模型：{provider_config['name']} / {args.model or provider_config['model']}")
    print("\n🚀 正在生成脚本...\n")

    try:
        skill = create_skill(
            api_key=api_key,
            provider=args.provider,
            model_name=args.model
        )
        script = skill.generate(args.product, args.style)

        print("=" * 50)
        print("📋 生成的视频脚本")
        print("=" * 50)

        for scene in script:
            print(f"\n📹 {scene['scene_no']}（{scene.get('duration', 'N/A')}）")
            print(f"   画面：{scene['visual_description']}")
            print(f"   口播：{scene['voiceover']}")
            print(f"   AI指令：{scene['ai_prompt']}")
            if scene.get('action_hint'):
                print(f"   行动：{scene['action_hint']}")

        print("\n" + "=" * 50)
        print("✅ 完成")

    except Exception as e:
        print(f"❌ 生成失败：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
