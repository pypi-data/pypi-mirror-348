"""Salesforce MCP 插件包。用于通过客户名称查询 Salesforce 的 Account 信息。"""
from mcp_server import server

def main():
    server.mcp.run()

if __name__ == "__main__":
    main()