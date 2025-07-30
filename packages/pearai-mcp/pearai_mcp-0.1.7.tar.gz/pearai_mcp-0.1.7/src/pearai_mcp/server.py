#!/usr/bin/env python3
import asyncio
import sys
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from pearai_mcp.deploy import DeploymentService
from pearai_mcp.templates import TemplateService
from pearai_mcp.constants import SERVER_URL

# Get auth token from command line argument
if len(sys.argv) < 2:
    raise ValueError("Auth token must be provided as command line argument")
AUTH_TOKEN = sys.argv[1]

server = Server("pearai-mcp")
deployment_service = DeploymentService(SERVER_URL, AUTH_TOKEN)
template_service = TemplateService(SERVER_URL, AUTH_TOKEN)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools from all services.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return deployment_service.get_tools() + template_service.get_tools()

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests by routing to appropriate service.
    """
    if not arguments:
        arguments = {}

    # Route to deployment service
    if name == "deploy-webapp-from-path":
        return await deployment_service.deploy_from_path(
            arguments.get("zip_file_path"),
            arguments.get("env_file_path")
        )
    elif name == "redeploy-webapp-from-path":
        return await deployment_service.redeploy_from_path(
            arguments.get("zip_file_path"),
            arguments.get("env_file_path"),
            arguments.get("site_id")
        )

    # Route to template service
    elif name == "list-templates":
        return template_service.list_templates()
    elif name == "download-template":
        return template_service.fetch_template(arguments.get("template_url"))
    elif name == "create-new-project":
        return template_service.create_new_project(
            arguments.get("project_name"),
            arguments.get("template_url"),
            arguments.get("base_dir")
        )
    elif name == "template-feedback":
        return template_service.template_feedback(
            arguments.get("project_summary"),
            arguments.get("template_used")
        )

    raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pearai-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())