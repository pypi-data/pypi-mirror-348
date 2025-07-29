import logging
import os
from mcp.types import TextContent
from jsonschema import validate
from ..common.service import request_split, request_task, save_file


split_pdf_input_schema = {
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "PDF文档的绝对路径或URL地址"},
        "config": {
            "type": "object",
            "properties": {"pageCount": {"type": "number", "description": "拆分后的页数"}},
            "description": "配置项",
        },
    },
    "required": ["path", "config"],
}


async def split_pdf(args: dict, env: dict) -> list[TextContent]:
    logger = logging.getLogger("split_pdf")
    logger.info(f"CALL TOOL split_pdf, args: {args}, env: {env}")

    validate(args, split_pdf_input_schema)

    res = request_split({"clientId": env["clientId"], **args})
    doc = await request_task(res, {"clientId": env["clientId"]})
    doc["value"] = f"{os.path.splitext(os.path.basename(args['path']))[0]}-split_pdf.zip"

    result_path = save_file({"doc": doc, "path": args["path"]}, env)

    return [TextContent(type="text", text=f"PDF文档拆分成功：{result_path}")]
