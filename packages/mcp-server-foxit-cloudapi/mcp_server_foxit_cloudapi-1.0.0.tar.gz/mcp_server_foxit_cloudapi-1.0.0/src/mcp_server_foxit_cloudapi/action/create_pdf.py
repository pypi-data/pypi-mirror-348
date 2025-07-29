import logging
import os
from mcp.types import TextContent
from jsonschema import validate
from ..common.service import request_create, request_task, save_file


create_pdf_input_schema = {
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "转换文件的绝对路径或URL地址"},
        "format": {
            "type": "string",
            "enum": ["word", "excel", "ppt", "image", "text"],
            "description": "输入的文件类型",
        },
    },
    "required": ["path", "format"],
}


async def create_pdf(args: dict, env: dict) -> list[TextContent]:
    logger = logging.getLogger("create_pdf")
    logger.info(f"CALL TOOL create_pdf, args: {args}, env: {env}")

    validate(args, create_pdf_input_schema)

    res = request_create({"clientId": env["clientId"], **args})
    doc = await request_task(res, {"clientId": env["clientId"]})
    doc["value"] = f"{os.path.splitext(os.path.basename(args['path']))[0]}-create_pdf.pdf"

    result_path = save_file({"doc": doc, "path": args["path"]}, env)

    return [TextContent(type="text", text=f"PDF文档创建成功：{result_path}")]
