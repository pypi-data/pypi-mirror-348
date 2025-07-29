import logging
import os
from mcp.types import TextContent
from jsonschema import validate
from ..common.service import request_compress, request_task, save_file


compress_pdf_input_schema = {
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "PDF文档的绝对路径或URL地址"},
        "compressionLevel": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "description": "压缩级别",
            "default": "low",
        },
    },
    "required": ["path"],
}


async def compress_pdf(args: dict, env: dict) -> list[TextContent]:
    logger = logging.getLogger("compress_pdf")
    logger.info(f"CALL TOOL compress_pdf, args: {args}, env: {env}")

    validate(args, compress_pdf_input_schema)
    args["compressionLevel"] = args.get("compressionLevel", "low")

    res = request_compress({"clientId": env["clientId"], **args})
    doc = await request_task(res, {"clientId": env["clientId"]})
    doc["value"] = f"{os.path.splitext(os.path.basename(args['path']))[0]}-compress_pdf.pdf"

    result_path = save_file({"doc": doc, "path": args["path"]}, env)

    return [TextContent(type="text", text=f"PDF文档压缩成功：{result_path}")]
