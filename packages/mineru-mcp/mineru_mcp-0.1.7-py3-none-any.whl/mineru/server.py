"""MinerU File转Markdown转换的FastMCP服务器实现。"""

import re
import json
import signal
import os  # 添加导入
import contextlib
from pathlib import Path
from typing import Dict, Any, List, Annotated
from pydantic import Field
import aiohttp

from fastmcp import FastMCP
from . import config
from .api import MinerUClient
from .language import get_language_list


# 创建一个自定义的 lifespan 上下文管理器
@contextlib.asynccontextmanager
async def lifespan(app=None):
    # 启动阶段
    print("MinerU File转Markdown转换服务启动...")
    try:
        yield  # 应用运行阶段
    finally:
        # 关闭阶段，无论如何都会执行
        global _client_instance
        if _client_instance is not None:
            # 清理客户端资源
            _client_instance = None
        print("\n😊 感谢使用MinerU服务！服务正在退出...")


# 初始化 FastMCP 服务器
mcp = FastMCP(
    name="MinerU File to Markdown Conversion",
    instructions="""
    一个将文档转化工具，可以将文档转化成Markdown、Latex、Docx等格式，支持多种文件格式，包括PDF、Word、Excel、PPT以及图片格式（JPG、PNG、JPEG）。

    使用前必须先调用status://api检查当前API状态，谨慎直接使用！！！

    系统工具:
    convert_file_url: 转换URL中的文件
    convert_file_path: 转换本地文件
    local_parse_file: 使用本地自己搭建的API解析文件
    get_ocr_languages: 获取OCR支持的语言列表
    read_converted_file: 读取转换后的文件内容
    """,
    lifespan=lifespan,  # 使用自定义 lifespan
)


# 注册信号处理器
def handle_signals():
    def signal_handler(sig, frame):
        print("\n😊 感谢使用MinerU服务！服务正在退出...")
        os._exit(0)  # 使用 os._exit(0) 强制退出进程，不执行任何清理代码

    # 直接注册强制退出的处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


# Singleton instance for the client
_client_instance = None


def get_client() -> MinerUClient:
    """获取 MinerUClient 的单例实例。如果尚未初始化，则进行初始化。"""
    global _client_instance
    if _client_instance is None:
        _client_instance = MinerUClient()  # Initialization happens here
    return _client_instance


# Markdown 文件的输出目录
output_dir = config.DEFAULT_OUTPUT_DIR


def set_output_dir(dir_path: str):
    """设置转换后文件的输出目录。"""
    global output_dir
    output_dir = dir_path
    config.ensure_output_dir(output_dir)
    return output_dir


def parse_list_input(input_str: str) -> List[str]:
    """
    解析可能包含由逗号或换行符分隔的多个项目的字符串输入。

    Args:
        input_str: 可能包含多个项目的字符串

    Returns:
        解析出的项目列表
    """
    if not input_str:
        return []

    # 按逗号、换行符或空格分割
    items = re.split(r"[,\n\s]+", input_str)

    # 移除空项目并处理带引号的项目
    result = []
    for item in items:
        item = item.strip()
        # 如果存在引号，则移除
        if (item.startswith('"') and item.endswith('"')) or (
            item.startswith("'") and item.endswith("'")
        ):
            item = item[1:-1]

        if item:
            result.append(item)

    return result


@mcp.tool()
async def convert_file_url(
    url: Annotated[
        str,
        Field(
            description='文件URL，支持以下格式: - 单个URL: "https://example.com/document.pdf" - 多个URL(逗号分隔): "https://example.com/doc1.pdf, https://example.com/doc2.docx" - 字典配置: {"url": "https://example.com/document.pdf", "is_ocr": true} - 字典列表: [{"url": "url1", "is_ocr": true}, {"url": "url2", "is_ocr": false}] (支持pdf、ppt、pptx、doc、docx以及图片格式jpg、jpeg、png)'
        ),
    ],
    enable_ocr: Annotated[bool, Field(description="启用OCR识别")] = False,
    enable_formula: Annotated[bool, Field(description="启用公式识别")] = True,
    enable_table: Annotated[bool, Field(description="启用表格识别")] = True,
    language: Annotated[
        str, Field(description='文档语言，默认"auto"，可选"zh"中文,"en"英文等')
    ] = "auto",
    extra_formats: Annotated[
        List[str] | None,
        Field(description='额外导出格式，例如["docx", "html", "latex"]'),
    ] = None,
    page_ranges: Annotated[
        str | None,
        Field(
            description='指定页码范围，格式为逗号分隔的字符串。例如："2,4-6"：表示选取第2页、第4页至第6页；"2--2"：表示从第2页一直选取到倒数第二页。'
        ),
    ] = None,
) -> Dict[str, Any]:
    """
    **使用前必须先调用status://api检查当前API状态，谨慎直接使用！！！**
    从URL转换文件到Markdown格式。支持单个或多个URL处理。

    返回:
        成功: {"status": "success", "result_path": "输出目录路径"}
        失败: {"status": "error", "error": "错误信息"}

    示例:
        # 基本用法
        result = await convert_file_url(url="https://example.com/document.pdf")

        # 处理多个URL
        result = await convert_file_url(url="https://example.com/doc1.pdf, https://example.com/doc2.pdf")

        # 高级选项
        result = await convert_file_url(
            url="https://example.com/document.pdf",
            enable_ocr=True,
            language="en",
            extra_formats=["docx", "html"],
            page_ranges="1-5,8,10-15"
        )
    """
    urls_to_process = None

    # 检查是否为字典或字典列表格式的URL配置
    if isinstance(url, dict):
        # 单个URL配置字典
        urls_to_process = url
    elif isinstance(url, list) and len(url) > 0 and isinstance(url[0], dict):
        # URL配置字典列表
        urls_to_process = url
    elif isinstance(url, str):
        # 检查是否为 JSON 字符串格式的多URL配置
        if url.strip().startswith("[") and url.strip().endswith("]"):
            try:
                # 尝试解析 JSON 字符串为URL配置列表
                url_configs = json.loads(url)
                if not isinstance(url_configs, list):
                    raise ValueError("JSON URL配置必须是列表格式")

                urls_to_process = url_configs
            except json.JSONDecodeError:
                # 不是有效的 JSON，继续使用字符串解析方式
                pass

    if urls_to_process is None:
        # 解析普通URL列表
        urls = parse_list_input(url)

        if not urls:
            raise ValueError("未提供有效的 URL")

        if len(urls) == 1:
            # 单个URL处理
            urls_to_process = {"url": urls[0], "is_ocr": enable_ocr}
        else:
            # 多个URL，转换为URL配置列表
            urls_to_process = []
            for url_item in urls:
                urls_to_process.append(
                    {
                        "url": url_item,
                        "is_ocr": enable_ocr,
                    }
                )

    # 使用submit_file_url_task处理URLs
    try:
        result_path = await get_client().process_file_to_markdown(
            lambda urls, o: get_client().submit_file_url_task(
                urls,
                o,
                enable_formula=enable_formula,
                enable_table=enable_table,
                language=language,
                extra_formats=extra_formats,
                page_ranges=page_ranges,
            ),
            urls_to_process,
            enable_ocr,
            output_dir,
            enable_formula=enable_formula,
            enable_table=enable_table,
            language=language,
            extra_formats=extra_formats,
            page_ranges=page_ranges,
        )
        return {"status": "success", "result_path": result_path}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
async def convert_file_path(
    file_path: Annotated[
        str,
        Field(
            description='文件路径，支持以下格式: - 单个路径: "/path/to/file.pdf" - 多个路径(逗号分隔): "/path/to/file1.pdf, /path/to/file2.pdf" - 字典配置: {"path": "/path/to/file.pdf", "is_ocr": true} - 字典列表: [{"path": "/path/file1.pdf", "is_ocr": true}, {"path": "/path/file2.pdf", "is_ocr": false}] (支持pdf、ppt、pptx、doc、docx以及图片格式jpg、jpeg、png)'
        ),
    ],
    enable_ocr: Annotated[bool, Field(description="启用OCR识别")] = False,
    enable_formula: Annotated[bool, Field(description="启用公式识别")] = True,
    enable_table: Annotated[bool, Field(description="启用表格识别")] = True,
    language: Annotated[
        str, Field(description='文档语言，默认"auto"，可选"zh"中文,"en"英文等')
    ] = "auto",
    extra_formats: Annotated[
        List[str] | None,
        Field(description='额外导出格式，例如["docx", "html", "latex"]'),
    ] = None,
    page_ranges: Annotated[
        str | None,
        Field(
            description='指定页码范围，格式为逗号分隔的字符串。例如："2,4-6"：表示选取第2页、第4页至第6页；"2--2"：表示从第2页一直选取到倒数第二页。'
        ),
    ] = None,
) -> Dict[str, Any]:
    """
    **使用前必须先调用status://api检查当前API状态，谨慎直接使用！！！**
    将本地文件转换为Markdown格式。支持单个或多个文件批量处理。

    返回:
        成功: {"status": "success", "result_path": "输出目录路径"}
        失败: {"status": "error", "error": "错误信息"}

    示例:
        # 基本用法
        result = await convert_file_path(file_path="/path/to/document.pdf")

        # 处理多个文件
        result = await convert_file_path(file_path="/path/to/file1.pdf, /path/to/file2.pdf")

        # 高级选项
        result = await convert_file_path(
            file_path="/path/to/document.pdf",
            enable_ocr=True,
            language="zh",
            extra_formats=["docx"],
            page_ranges="1-10,15,20-30"
        )
    """

    files_to_process = None

    # 检查是否为字典或字典列表格式的文件配置
    if isinstance(file_path, dict):
        # 单个文件配置字典
        files_to_process = file_path
    elif (
        isinstance(file_path, list)
        and len(file_path) > 0
        and isinstance(file_path[0], dict)
    ):
        # 文件配置字典列表
        files_to_process = file_path
    elif isinstance(file_path, str):
        # 检查是否为 JSON 字符串格式的多文件配置
        if file_path.strip().startswith("[") and file_path.strip().endswith("]"):
            try:
                # 尝试解析 JSON 字符串为文件配置列表
                file_configs = json.loads(file_path)
                if not isinstance(file_configs, list):
                    raise ValueError("JSON 文件配置必须是列表格式")

                files_to_process = file_configs
            except json.JSONDecodeError:
                # 不是有效的 JSON，继续使用字符串解析方式
                pass

    if files_to_process is None:
        # 解析普通文件路径列表
        file_paths = parse_list_input(file_path)

        if not file_paths:
            raise ValueError("未提供有效的文件路径")

        if len(file_paths) == 1:
            # 单个文件处理
            files_to_process = {
                "path": file_paths[0],
                "is_ocr": enable_ocr,
            }
        else:
            # 多个文件路径，转换为文件配置列表
            files_to_process = []
            for i, path in enumerate(file_paths):
                files_to_process.append(
                    {
                        "path": path,
                        "is_ocr": enable_ocr,
                    }
                )

    # 使用submit_file_task处理文件
    try:
        result_path = await get_client().process_file_to_markdown(
            lambda files, o: get_client().submit_file_task(
                files,
                o,
                enable_formula=enable_formula,
                enable_table=enable_table,
                language=language,
                extra_formats=extra_formats,
                page_ranges=page_ranges,
            ),
            files_to_process,
            enable_ocr,
            output_dir,
            enable_formula=enable_formula,
            enable_table=enable_table,
            language=language,
            extra_formats=extra_formats,
            page_ranges=page_ranges,
        )
        return {"status": "success", "result_path": result_path}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
async def local_parse_file(
    file_path: Annotated[
        str,
        Field(
            description="要解析的文件路径，支持 pdf、ppt、pptx、doc、docx以及图片格式jpg、jpeg、png"
        ),
    ],
    parse_method: Annotated[str, Field(description="解析方法")] = "auto",
    is_json_md_dump: Annotated[
        bool, Field(description="以JSON格式导出Markdown")
    ] = False,
    output_dir: Annotated[
        str | None,
        Field(
            description="输出目录路径(这里不是MCP所在主机的输出目录，而是本地API所在服务器的输出目录)"
        ),
    ] = None,
    return_layout: Annotated[bool, Field(description="是否返回布局信息")] = False,
    return_info: Annotated[bool, Field(description="是否返回基本信息")] = False,
    return_content_list: Annotated[bool, Field(description="是否返回内容列表")] = False,
    return_images: Annotated[bool, Field(description="是否返回图片")] = False,
) -> Dict[str, Any]:
    """
    **使用前必须先调用status://api检查当前API状态，谨慎直接使用！！！**
    根据环境变量设置使用本地或远程API解析文件。

    返回:
        成功: {"status": "success", "result": 处理结果} 或 {"status": "success", "result_path": "输出目录路径"}
        失败: {"status": "error", "error": "错误信息"}

    示例:
        # 基本用法
        result = await local_parse_file(file_path="/path/to/document.pdf")

        # 高级用法
        result = await local_parse_file(
            file_path="/path/to/document.pdf",
            parse_method="auto",
            is_json_md_dump=True,
            output_dir="/path/to/output",
            return_layout=True
        )
    """
    file_path = Path(file_path)

    # 默认和环境变量配置一致，但是要注意，这里output_dir是本地API所在服务器的
    # 输出目录而不是MCP所在主机的输出目录
    if output_dir is None:
        output_dir = config.DEFAULT_OUTPUT_DIR

    # 检查文件是否存在
    if not file_path.exists():
        return {"status": "error", "error": f"文件不存在: {file_path}"}

    try:
        # 根据环境变量决定使用本地API还是远程API
        if config.USE_LOCAL_API:
            config.logger.info(f"使用本地API: {config.LOCAL_MINERU_API_BASE}")
            return await _parse_file_local(
                file_path=str(file_path),
                parse_method=parse_method,
                is_json_md_dump=is_json_md_dump,
                output_dir=output_dir,
                return_layout=return_layout,
                return_info=return_info,
                return_content_list=return_content_list,
                return_images=return_images,
            )
        else:
            return {"status": "error", "error": "远程API未配置"}
    except Exception as e:
        config.logger.error(f"解析文件时出错: {str(e)}")
        return {"status": "error", "error": str(e)}


@mcp.tool()
async def get_ocr_languages() -> Dict[str, Any]:
    """
    获取 OCR 支持的语言列表。

    Returns:
        Dict[str, Any]: 包含所有支持的OCR语言列表的字典
    """
    try:
        # 从language模块获取语言列表
        languages = get_language_list()
        return {"status": "success", "languages": languages}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
async def read_converted_file(
    file_path: Annotated[str, Field(description="要读取的文件路径")],
) -> Dict[str, Any]:
    """
    读取解析后的文件内容。主要支持Markdown和其他文本文件格式。

    返回:
        成功: {"status": "success", "content": "文件内容"}
        失败: {"status": "error", "error": "错误信息"}

    示例:
        # 基本用法
        result = await read_converted_file(file_path="/path/to/converted.md")

    > 注意：如果文件是Markdown格式,一般调用远程API获得的解析结果的路径是./downloads/xxx/文件名/full.md 或 ./downloads/xxx/full.txt
    """
    try:
        target_file = Path(file_path)
        parent_dir = target_file.parent
        suffix = target_file.suffix.lower()

        # 支持的文本文件格式
        text_extensions = [".md", ".txt", ".json", ".html", ".tex", ".latex"]

        if suffix not in text_extensions:
            return {
                "status": "error",
                "error": f"不支持的文件格式: {suffix}。目前仅支持以下格式: {', '.join(text_extensions)}",
            }

        if not target_file.exists():
            if not parent_dir.exists():
                return {"status": "error", "error": f"目录 {parent_dir} 不存在"}

            # 递归搜索所有子目录下的同后缀文件
            similar_files_paths = [
                str(f) for f in parent_dir.rglob(f"*{suffix}") if f.is_file()
            ]

            if similar_files_paths:
                if len(similar_files_paths) == 1:
                    # 如果只找到一个文件，直接读取并返回内容
                    alternative_file = similar_files_paths[0]
                    try:
                        with open(alternative_file, "r", encoding="utf-8") as f:
                            content = f.read()
                        return {
                            "status": "success",
                            "content": content,
                            "message": f"未找到文件 {target_file.name}，但找到了 {Path(alternative_file).name}，已返回其内容",
                        }
                    except Exception as e:
                        return {
                            "status": "error",
                            "error": f"尝试读取替代文件时出错: {str(e)}",
                        }
                else:
                    # 如果找到多个文件，提供建议列表
                    suggestion = f"你是否在找: {', '.join(similar_files_paths)}?"
                    return {
                        "status": "error",
                        "error": f"文件 {target_file.name} 不存在。在 {parent_dir} 及其子目录下找到以下同类型文件。{suggestion}",
                    }
            else:
                return {
                    "status": "error",
                    "error": f"文件 {target_file.name} 不存在，且在目录 {parent_dir} 及其子目录下未找到其他 {suffix} 文件。",
                }

        # 以文本模式读取
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "content": content}

    except Exception as e:
        config.logger.error(f"读取文件时出错: {str(e)}")
        return {"status": "error", "error": str(e)}


@mcp.resource("status://api")
def api_status() -> str:
    """展示 API 状态信息。"""
    api_config = config.validate_api_config()

    # 添加本地API配置信息
    api_config["use_local_api"] = config.USE_LOCAL_API
    if config.USE_LOCAL_API:
        api_config["local_api_base"] = config.LOCAL_MINERU_API_BASE

    # 格式化为易读格式
    status_lines = [
        "# MinerU API 配置状态",
        "",
        f"- API 基础 URL: {api_config['api_base']}",
        f"- API 密钥设置: {'已设置' if api_config['api_key_set'] else '未设置'}",
        f"- 输出目录: {api_config['output_dir']}",
        f"- 使用本地 API: {'是' if api_config['use_local_api'] else '否'}",
    ]

    # 仅当使用本地API时显示本地API基础URL
    if api_config["use_local_api"]:
        status_lines.append(f"- 本地 API 基础 URL: {api_config['local_api_base']}")

    return "\n".join(status_lines)


@mcp.resource("help://usage")
def usage_help() -> str:
    """提供 MinerU MCP 服务使用说明的帮助文档。"""
    return """
# MinerU-MCP 服务使用说明

MinerU-MCP 是一个桥接 MinerU File 转 Markdown API 的 MCP 服务。支持本地API和远程API两种模式。

## 工具选择指南

在使用任何工具前，**请先检查当前API状态**：
```
await client.get_resource("status://api")
```

### API模式与推荐工具

1. **远程API模式** (USE_LOCAL_API=false)：
   - 推荐工具: `convert_file_url`, `convert_file_path`
   - 不推荐工具: `local_parse_file` (虽然可用，但在远程模式下不是最优选择)

2. **本地API模式** (USE_LOCAL_API=true)：
   - 推荐工具: `local_parse_file`
   - 不推荐工具: `convert_file_url`, `convert_file_path` (这些工具始终使用远程API)

## 可用的工具

### 1. convert_file_url [仅限远程API]

从 URL 转换文件到 Markdown 格式。**注意：此工具始终使用远程API，与环境设置无关**。

**基本用法**:
```
await client.call("convert_file_url", url="https://example.com/document.pdf")
```

**选项**:
- `url`: 文件的URL (必需)
- `enable_ocr`: 是否启用OCR (默认: False)
- `enable_formula`: 是否启用公式识别 (默认: True)
- `enable_table`: 是否启用表格识别 (默认: True)
- `language`: 文档语言 (默认: "auto")
- `extra_formats`: 额外导出格式 (默认: None)
- `page_ranges`: 指定页码范围，如 "1-5,8,10-15" (默认: None)

**支持的文件格式**:
- 文档: PDF, DOCX, DOC, PPT, PPTX
- 图片: JPG, JPEG, PNG

### 2. convert_file_path [仅限远程API]

从本地文件路径转换文件到 Markdown 格式。**注意：此工具始终使用远程API，与环境设置无关**。

**基本用法**:
```
await client.call("convert_file_path", file_path="/path/to/document.pdf")
```

**选项**:
- `file_path`: 文件的路径 (必需)
- `enable_ocr`: 是否启用OCR (默认: False)
- `enable_formula`: 是否启用公式识别 (默认: True)
- `enable_table`: 是否启用表格识别 (默认: True)
- `language`: 文档语言 (默认: "auto")
- `extra_formats`: 额外导出格式 (默认: None)
- `page_ranges`: 指定页码范围，如 "1-5,8,10-15" (默认: None)

**支持的文件格式**:
- 文档: PDF, DOCX, DOC, PPT, PPTX
- 图片: JPG, JPEG, PNG

### 3. local_parse_file [本地API优先]

根据环境变量配置，使用本地或远程API解析文件。**当USE_LOCAL_API=true时使用本地API，否则使用远程API**。

**基本用法**:
```
await client.call("local_parse_file", file_path="/path/to/document.pdf")
```

**选项**:
- `file_path`: 文件的路径 (必需)
- `parse_method`: 解析方法 (默认: "auto")
- `is_json_md_dump`: 是否以JSON格式导出Markdown (默认: False)
- `output_dir`: 输出目录 (默认: None)
- `return_layout`: 是否返回布局信息 (默认: False)
- `return_info`: 是否返回信息 (默认: False)
- `return_content_list`: 是否返回内容列表 (默认: False)
- `return_images`: 是否返回图片 (默认: False)

**支持的文件格式**:
- 文档: PDF, DOCX, DOC, PPT, PPTX
- 图片: JPG, JPEG, PNG

### 4. get_ocr_languages

获取OCR支持的语言列表。

**基本用法**:
```
await client.call("get_ocr_languages")
```

### 5. read_converted_file

读取解析后的文件内容，主要支持Markdown和其他文本文件格式。

**基本用法**:
```
await client.call("read_converted_file", file_path="/path/to/converted.md")
```

**选项**:
- `file_path`: 文件的路径 (必需)

**支持的文件格式**:
- Markdown (.md)
- 文本文件 (.txt)
- JSON文件 (.json)
- HTML文件 (.html)
- TeX/LaTeX文件 (.tex, .latex)

## 环境变量配置

- `MINERU_API_KEY`: MinerU API的密钥（必需）
- `MINERU_API_BASE`: MinerU API的基础URL（默认为 "https://mineru.net"）
- `OUTPUT_DIR`: 结果输出目录（默认为 "./downloads"）
- `USE_LOCAL_API`: 是否使用本地API（true/false）
- `LOCAL_MINERU_API_BASE`: 本地API基础URL（默认为 "http://localhost:8080"）

## 资源

- `status://api`: 显示当前API配置状态（**重要：在使用工具前请先检查此状态**）
- `help://usage`: 显示此帮助文档
"""


@mcp.prompt()
def conversion_prompt(
    input_content: Annotated[
        str, Field(description="用户输入的内容，可能包含文件路径或URL")
    ] = "",
) -> str:
    """
    创建文件转Markdown处理提示，指导AI如何使用转换工具。

    Returns:
        指导AI使用转换工具的提示字符串
    """
    return f"""
Please convert the following file(s) to Markdown format according to the request below:

{input_content}

First, check the current API mode using the status resource:
```
await client.get_resource("status://api")
```

Then select the appropriate tool based on API mode and input type:

For Remote API mode (USE_LOCAL_API=false):
- If it is a URL or multiple URLs, use the convert_file_url tool
- If it is a local file path or multiple file paths, use the convert_file_path tool

For Local API mode (USE_LOCAL_API=true):
- Prefer local_parse_file tool for all local file conversions
- Note that convert_file_url and convert_file_path will still use the remote API regardless of local mode

If both URLs and local files are included, please use the above tools separately for each part.

Tool usage guidelines:
1. Batch processing is supported - you can convert multiple URLs or file paths
at once (separated by commas, spaces, or newlines)
2. OCR is disabled by default, but can be enabled for better handling of scanned files
3. The converted Markdown files will be saved in the specified output directory
4. For URLs, the system will automatically download and clean up temporary files after processing

After conversion, you can read the contents of the converted file using:
```
result = await client.call("read_converted_file", file_path="/path/to/converted.md")
```
This tool supports reading Markdown (.md), text (.txt), JSON (.json), HTML (.html), and TeX/LaTeX (.tex, .latex) files.

Advanced parameters available:
- enable_ocr: Whether to enable OCR (default: False)
- enable_formula: Whether to enable formula recognition (default: True)
- enable_table: Whether to enable table recognition (default: True)
- language: Document language code or 'auto' for automatic detection
- extra_formats: Additional export formats (options: ['docx', 'html', 'latex'])
- page_ranges: Specify page ranges, e.g., "1-5,8,10-15" (selects pages 1-5, 8, and 10-15)

Supported file formats:
- Documents: PDF, DOCX, DOC, PPT, PPTX
- Images: JPG, JPEG, PNG

Example input formats:
- URL: https://example.com/document.pdf
- Local file: /path/to/document.pdf
- Multiple URLs: https://example.com/doc1.pdf, https://example.com/doc2.pdf
- Multiple files: /path/to/doc1.pdf, /path/to/doc2.pdf

If you have special requirements for the conversion process, please specify the relevant parameters when using the tool.
"""


async def _parse_file_local(
    file_path: str,
    parse_method: str = "auto",
    is_json_md_dump: bool = False,
    output_dir: str = None,
    return_layout: bool = False,
    return_info: bool = False,
    return_content_list: bool = False,
    return_images: bool = False,
) -> Dict[str, Any]:
    """
    使用本地API解析文件。

    Args:
        file_path: 要解析的文件路径
        parse_method: 解析方法
        is_json_md_dump: 是否以JSON格式导出Markdown
        output_dir: 输出目录
        return_layout: 是否返回布局信息
        return_info: 是否返回信息
        return_content_list: 是否返回内容列表
        return_images: 是否返回图片

    Returns:
        Dict[str, Any]: 包含解析结果的字典
    """
    # API URL路径
    api_url = f"{config.LOCAL_MINERU_API_BASE}/file_parse"

    # 使用Path对象确保文件路径正确
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件二进制数据
    with open(file_path_obj, "rb") as f:
        file_data = f.read()

    # 构建URL查询参数
    params = {
        "parse_method": parse_method,
        "is_json_md_dump": str(is_json_md_dump).lower(),
        "return_layout": str(return_layout).lower(),
        "return_info": str(return_info).lower(),
        "return_content_list": str(return_content_list).lower(),
        "return_images": str(return_images).lower(),
    }

    # 如果提供了输出目录，添加到参数中
    if output_dir:
        params["output_dir"] = output_dir

    # 准备用于上传文件的表单数据
    file_type = file_path_obj.suffix.lower()
    form_data = aiohttp.FormData()
    form_data.add_field(
        "file", file_data, filename=file_path_obj.name, content_type=file_type
    )

    config.logger.debug(f"发送本地API请求到: {api_url}")
    config.logger.debug(f"请求参数: {params}")
    config.logger.debug(f"上传文件: {file_path_obj.name} (大小: {len(file_data)} 字节)")

    # 发送请求
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, data=form_data, params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    config.logger.error(
                        f"API返回错误状态码: {response.status}, 错误信息: {error_text}"
                    )
                    raise RuntimeError(f"API返回错误: {response.status}, {error_text}")

                result = await response.json()

                config.logger.debug(f"本地API响应: {result}")

                # 处理响应
                if "error" in result:
                    return {"status": "error", "error": result["error"]}

                return {"status": "success", "result": result}
    except aiohttp.ClientError as e:
        error_msg = f"与本地API通信时出错: {str(e)}"
        config.logger.error(error_msg)
        raise RuntimeError(error_msg)


def run_server(mode=None):
    """运行 FastMCP 服务器。"""
    # 确保输出目录存在
    config.ensure_output_dir(output_dir)

    # 检查是否设置了 API 密钥
    if not config.MINERU_API_KEY:
        print("警告: MINERU_API_KEY 环境变量未设置。")
        print("使用以下命令设置: export MINERU_API_KEY=your_api_key")

    try:
        # 运行服务器
        if mode:
            mcp.run(mode)
        else:
            mcp.run()
    except KeyboardInterrupt:
        print("\n😊 感谢使用MinerU服务！服务正在优雅退出...")
    except Exception as e:
        print(f"\n❌ 服务异常退出: {str(e)}")
