import logging
import os
from .server import serve
import asyncio
from .common.constant import ENV_BASE


def main() -> None:
    """Foxit Cloud API MCP server."""

    if ENV_BASE != "prod":
        logging.basicConfig(
            filename="./temp/debug.log",
            level=logging.INFO,
        )
    asyncio.run(serve())


if __name__ == "__main__":
    main()
