import logging
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from .action.combine_pdf import combine_pdf, combine_pdf_input_schema
from .action.compare_pdf import compare_pdf, compare_pdf_input_schema
from .action.compress_pdf import compress_pdf, compress_pdf_input_schema
from .action.convert_pdf import convert_pdf, convert_pdf_input_schema
from .action.create_pdf import create_pdf, create_pdf_input_schema
from .action.create_pdf_from_html import create_pdf_from_html, create_pdf_from_html_input_schema
from .action.extract_pdf import extract_pdf, extract_pdf_input_schema
from .action.flatten_pdf import flatten_pdf, flatten_pdf_input_schema
from .action.linearize_pdf import linearize_pdf, linearize_pdf_input_schema
from .action.manipulation_pdf import manipulation_pdf, manipulation_pdf_input_schema
from .action.protect_pdf import protect_pdf, protect_pdf_input_schema
from .action.remove_password import remove_password, remove_password_input_schema
from .action.split_pdf import split_pdf, split_pdf_input_schema


async def serve() -> None:
    logger = logging.getLogger(__name__)

    CLIENT_ID = os.getenv("CLIENT_ID")
    if CLIENT_ID is None:
        raise ValueError("CLIENT_ID environment variable is not set.")

    env = {
        "mode": os.getenv("MODE", "LOCAL"),
        "clientId": CLIENT_ID,
    }
    logger.info(f"env: {env}")

    server = Server("foxit_cloudapi")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="combine_pdf",
                description="""将压缩或归档文件中的多个PDF文档，合并为一个PDF文档。
                使用示例1：把<absolute_path/file_name.zip>中的PDF文档合并为一个PDF。
                使用示例2：把<url/file_name.pdf>, <url/file_name1.pdf>合并为一个PDF。""",
                inputSchema=combine_pdf_input_schema,
            ),
            Tool(
                name="compare_pdf",
                description="""逐页比较一个PDF文档（作为“基准文档”）与另一个PDF文档（作为“比较文档”）。
                使用示例1：把<absolute_path/file_name.pdf>与<absolute_path/file_name.pdf>进行比较。
                使用示例2：把<absolute_path/file_name.pdf>与<absolute_path/file_name.pdf>进行比较，比较结果为：pdf。
                使用示例3：把<url/file_name.pdf>与<url/file_name.pdf>进行比较。""",
                inputSchema=compare_pdf_input_schema,
            ),
            Tool(
                name="compress_pdf",
                description="""使用指定的压缩级别压缩PDF文档。
                使用示例1：压缩<absolute_path/file_name.pdf>。
                使用示例2：压缩<absolute_path/file_name.pdf>，压缩级别为：high。
                使用示例3：压缩<url/file_name.pdf>。""",
                inputSchema=compress_pdf_input_schema,
            ),
            Tool(
                name="convert_pdf",
                description="""转换PDF文档到其他格式，支持格式：word, excel, ppt, image, text, html。
                使用示例1：把<absolute_path/file_name.pdf>转换为word。
                使用示例2：把<absolute_path/file_name.pdf>转换为text。
                使用示例3：把<url/file_name.pdf>转换为excel。""",
                inputSchema=convert_pdf_input_schema,
            ),
            Tool(
                name="create_pdf",
                description="""从其他格式，创建或转换为PDF文档，支持格式：word，excel，ppt，image，text。
                使用示例1：把<absolute_path/file_name.docx>转换为PDF。
                使用示例2：把<absolute_path/file_name.txt>转换为PDF。
                使用示例3：把<url/file_name.png>转换为PDF。""",
                inputSchema=create_pdf_input_schema,
            ),
            Tool(
                name="create_pdf_from_html",
                description="""从HTML文件或指定站点URL创建PDF。
                使用示例1：把<absolute_path/file_name.html>转换为PDF。
                使用示例2：把<url>转换为PDF。
                使用示例3：把<url>转换为PDF，页面模式为：单页。
                使用示例4：把<url/flie_name.html>转换为PDF，输入格式为：html。""",
                inputSchema=create_pdf_from_html_input_schema,
            ),
            Tool(
                name="extract_pdf",
                description="""提取PDF文档中的文本或图像。
                使用示例1：提取<absolute_path/file_name.pdf>中的文本。
                使用示例2：提取<absolute_path/file_name.pdf>中的图片。
                使用示例3：提取<url/file_name.pdf>中的文本。""",
                inputSchema=extract_pdf_input_schema,
            ),
            Tool(
                name="flatten_pdf",
                description="""使PDF文档页面扁平化，使注释和表单字段成为页面内容的一部分。
                使用示例1：把<absolute_path/file_name.pdf>扁平化。
                使用示例2：把<url/file_name.pdf>扁平化。""",
                inputSchema=flatten_pdf_input_schema,
            ),
            Tool(
                name="linearize_pdf",
                description="""线性化PDF文档。
                使用示例1：把<absolute_path/file_name.pdf>线性化。
                使用示例2：把<url/file_name.pdf>线性化。""",
                inputSchema=linearize_pdf_input_schema,
            ),
            Tool(
                name="manipulation_pdf",
                description="""操作PDF文档，例如删除页面，旋转页面，移动页面。
                使用示例1：删除<absolute_path/file_name.pdf>的第1页。
                使用示例2：把<absolute_path/file_name.pdf>的第2页移到第1页。
                使用示例3：删除<url/file_name.pdf>的第1页。""",
                inputSchema=manipulation_pdf_input_schema,
            ),
            Tool(
                name="protect_pdf",
                description="""使用用户或/和所有者密码保护PDF文档，并对某些功能设置限制。
                使用示例1：给<absolute_path/file_name.pdf>设置用户密码，密码为：123456。
                使用示例2：给<absolute_path/file_name.pdf>设置所有者密码，密码为：123456，权限设置为：不允许修改PDF内容。
                使用示例3：给<url/file_name.pdf>设置用户密码，密码为：123456。""",
                inputSchema=protect_pdf_input_schema,
            ),
            Tool(
                name="remove_password",
                description="""从PDF文档中删除密码安全性。
                使用示例1：移除<absolute_path/file_name.pdf>的用户密码，密码为：123456。
                使用示例2：移除<absolute_path/file_name.pdf>的所有者密码，密码为：123456。
                使用示例3：移除<url/file_name.pdf>的用户密码，密码为：123456。""",
                inputSchema=remove_password_input_schema,
            ),
            Tool(
                name="split_pdf",
                description="""将PDF文档拆分为多个较小的文档。
                使用示例1：把<absolute_path/file_name.pdf>拆分为多个文档，拆分后的页数为：3。
                使用示例2：把<url/file_name.pdf>拆分为多个文档，拆分后的页数为：2。""",
                inputSchema=split_pdf_input_schema,
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        match name:
            case "combine_pdf":
                return await combine_pdf(arguments, env)
            case "compare_pdf":
                return await compare_pdf(arguments, env)
            case "compress_pdf":
                return await compress_pdf(arguments, env)
            case "convert_pdf":
                return await convert_pdf(arguments, env)
            case "create_pdf":
                return await create_pdf(arguments, env)
            case "create_pdf_from_html":
                return await create_pdf_from_html(arguments, env)
            case "extract_pdf":
                return await extract_pdf(arguments, env)
            case "flatten_pdf":
                return await flatten_pdf(arguments, env)
            case "linearize_pdf":
                return await linearize_pdf(arguments, env)
            case "manipulation_pdf":
                return await manipulation_pdf(arguments, env)
            case "protect_pdf":
                return await protect_pdf(arguments, env)
            case "remove_password":
                return await remove_password(arguments, env)
            case "split_pdf":
                return await split_pdf(arguments, env)
            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
