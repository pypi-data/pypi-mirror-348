"""
uv run test.py
_ENV_BASE=devcn uv run test.py
"""

import logging
from typing import Union
from src.mcp_server_foxit_cloudapi.action.combine_pdf import combine_pdf
from src.mcp_server_foxit_cloudapi.action.compare_pdf import compare_pdf
from src.mcp_server_foxit_cloudapi.action.compress_pdf import compress_pdf
from src.mcp_server_foxit_cloudapi.action.create_pdf_from_html import create_pdf_from_html
from src.mcp_server_foxit_cloudapi.action.create_pdf import create_pdf
from src.mcp_server_foxit_cloudapi.action.extract_pdf import extract_pdf
from src.mcp_server_foxit_cloudapi.action.flatten_pdf import flatten_pdf
from src.mcp_server_foxit_cloudapi.action.linearize_pdf import linearize_pdf
from src.mcp_server_foxit_cloudapi.action.manipulation_pdf import manipulation_pdf
from src.mcp_server_foxit_cloudapi.action.protect_pdf import protect_pdf
from src.mcp_server_foxit_cloudapi.action.remove_password import remove_password
from src.mcp_server_foxit_cloudapi.action.split_pdf import split_pdf
import asyncio

logging.basicConfig(
    filename="./temp/debug.log",
    level=logging.INFO,
)

client_id = (
    "0b0a248c2c877cd3797d1180cfa69206"
)
mode = "CLOUD"

# asyncio.run(
#     combine_pdf(
#         # {"path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/2docs.zip"},
#         {
#             "path": [
#                 "https://gitee.com/wtw/dev-file/raw/master/2%20pages.pdf",
#                 "https://gitee.com/wtw/dev-file/raw/master/1%20page.pdf",
#             ]
#         },
#         {"clientId": client_id, "mode": mode},
#     )
# )

# asyncio.run(
#     compare_pdf(
#         {
#             "basePath": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide.pdf",
#             "comparePath": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide compare.pdf",
#         },
#         {"clientId": client_id, "mode": mode},
#     )
# )

# asyncio.run(
#     compress_pdf(
#         {"path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide.pdf"},
#         {"clientId": client_id, "mode": mode},
#     )
# )

asyncio.run(
    create_pdf_from_html(
        # {"format": "html", "path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/dev.html"},
        {"format": "url", "url": "https://www.baidu.com"},
        {"clientId": client_id, "mode": mode},
    )
)

exit()

asyncio.run(
    create_pdf(
        {"path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/dev.docx", "format": "word"},
        {"clientId": client_id, "mode": mode},
    )
)

asyncio.run(
    extract_pdf(
        {
            "path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide.pdf",
            "mode": "extractText",
        },
        {"clientId": client_id, "mode": mode},
    )
)

asyncio.run(
    flatten_pdf(
        {"path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide.pdf"},
        {"clientId": client_id, "mode": mode},
    )
)

asyncio.run(
    linearize_pdf(
        {"path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide.pdf"},
        {"clientId": client_id, "mode": mode},
    )
)

asyncio.run(
    manipulation_pdf(
        {
            "path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide.pdf",
            "config": {"pageAction": "delete", "pages": [0]},
        },
        {"clientId": client_id, "mode": mode},
    )
)

asyncio.run(
    protect_pdf(
        {
            "path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide.pdf",
            "passwordProtection": {"userPassword": "123456"},
        },
        {"clientId": client_id, "mode": mode},
    )
)

asyncio.run(
    remove_password(
        {"path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/user123.pdf", "password": "123"},
        {"clientId": client_id, "mode": mode},
    )
)

asyncio.run(
    split_pdf(
        {
            "path": "/Users/wutianwei/Documents/GitDemo/dev-file-gitee/FoxitPDFSDKforWeb_DemoGuide.pdf",
            "config": {"pageCount": 2},
        },
        {"clientId": client_id, "mode": mode},
    )
)
