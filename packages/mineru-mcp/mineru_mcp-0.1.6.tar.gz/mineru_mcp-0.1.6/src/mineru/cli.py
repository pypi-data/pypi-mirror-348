"""MinerU File转Markdown服务的命令行界面。"""

import sys
import argparse
import atexit

from . import config
from . import server


def signal_handler(sig, frame):
    """处理信号中断，以优雅地退出程序。"""
    print("\n😊 感谢使用MinerU服务！服务正在优雅退出...")
    sys.exit(0)


def cleanup():
    """退出前的清理操作。"""
    print("✨ 已关闭所有连接，资源已释放。")


def main():
    """命令行界面的入口点。"""
    # 设置退出时的清理函数
    atexit.register(cleanup)

    parser = argparse.ArgumentParser(description="MinerU File转Markdown转换服务")

    parser.add_argument(
        "--output-dir", "-o", type=str, help="保存转换后文件的目录 (默认: ./downloads)"
    )

    parser.add_argument(
        "--transport", "-t", type=str, help="协议类型 (默认: stdio,可选: sse)"
    )

    args = parser.parse_args()

    # 验证API密钥 - 移动到这里，以便 --help 等参数可以无密钥运行
    if not config.MINERU_API_KEY:
        print(
            "错误: 启动服务需要 MINERU_API_KEY 环境变量。"
            "\\n请检查是否已设置该环境变量，例如："
            "\\n  export MINERU_API_KEY='your_actual_api_key'"
            "\\n或者，确保在项目根目录的 `.env` 文件中定义了该变量。"
            "\\n\\n您可以使用 --help 查看可用的命令行选项。",
            file=sys.stderr,  # 将错误消息输出到 stderr
        )
        sys.exit(1)

    # 如果提供了输出目录，则进行设置
    if args.output_dir:
        server.set_output_dir(args.output_dir)

    # 默认使用stdio协议
    transport = "stdio"
    if args.transport:
        transport = args.transport

    # 打印配置信息
    print("MinerU File转Markdown转换服务启动...")
    print(f"API 基础 URL: {config.MINERU_API_BASE}")
    print(f"API 密钥: {'已设置' if config.MINERU_API_KEY else '未设置'}")
    print(f"输出目录: {server.output_dir}")
    print("按 Ctrl+C 可以优雅地退出服务")

    try:
        # 运行服务器
        server.mcp.run(transport=transport)
    except KeyboardInterrupt:
        # 这可能不会被触发，因为信号处理器会先捕获，但作为额外保障
        print("\n😊 感谢使用MinerU服务！服务正在优雅退出...")
    except Exception as e:
        print(f"\n❌ 服务异常退出: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
