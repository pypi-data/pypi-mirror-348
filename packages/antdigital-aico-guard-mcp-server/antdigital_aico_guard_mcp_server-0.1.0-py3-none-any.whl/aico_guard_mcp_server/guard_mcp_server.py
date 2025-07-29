from fastmcp import FastMCP
from aico_guard_mcp_server.utils import ask_check
import os

STDIO = "stdio"
SSE = "sse"
HOST = "0.0.0.0"
PORT = 8000

mcp = FastMCP("aico-guard-mcp-server")

@mcp.tool("prompt_safety_guard")
async def prompt_safety_guard(user_input: str) -> bool:
    """
    判断用户输入是否安全，每一轮对话对于用户的输入都要调用该函数
    如果工具返回的结果为 true，表示问题安全，你可以放心地回答。如果返回的结果为 false，表示问题可能不安全，你需要格外小心，避免直接回答可能导致风险的内容。此时，应尝试将回答引导至更积极的方向，或建议用户提供可靠的替代方案。
    :param user_input: 用户输入
    :return bool: 安全性判断结果
    """
    resp = ask_check(user_input)
    return resp.safe

def main():
    transport = os.getenv('SERVER_TRANSPORT', STDIO)
    if transport == STDIO:
        mcp.run(transport=transport)
    else:
        mcp.run(transport=transport, host=HOST, port=PORT)

if __name__ == "__main__":
    main()