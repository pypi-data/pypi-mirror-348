#!/usr/bin/env python3
import os
import aiohttp
import mcp.types as types

class DeploymentService:
    def __init__(self, server_url: str, auth_token: str):
        self.server_url = server_url
        self.auth_token = auth_token

    def get_tools(self) -> list[types.Tool]:
        """List available deployment tools."""
        return [
            types.Tool(
                name="deploy-webapp-from-path",
                description="Deploy a website application from a zip file path of the project folder",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "zip_file_path": {
                            "type": "string",
                            "description": "Absolute path to the zip file of the project folder to deploy"
                        },
                        "env_file_path": {
                            "type": "string",
                            "description": "Absolute path to the .env file containing environment variables"
                        },
                        "static": {
                            "type": "boolean",
                            "description": "If the project is doing a static build. If not specified, default to False."
                        }
                    },
                    "required": ["zip_file_path", "env_file_path"],
                },
            ),
            types.Tool(
                name="redeploy-webapp-from-path",
                description="Redeploy a website application to an existing Netlify site from a zip file path",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "zip_file_path": {
                            "type": "string",
                            "description": "Absolute path to the zip file of the distribution folder to deploy"
                        },
                        "env_file_path": {
                            "type": "string",
                            "description": "Absolute path to the .env file containing environment variables"
                        },
                        "site_id": {
                            "type": "string",
                            "description": "ID of the existing Netlify site to redeploy to"
                        },
                        "static": {
                            "type": "boolean",
                            "description": "If the project is doing a static build. If not specified, default to False."
                        }
                    },
                    "required": ["zip_file_path", "env_file_path", "site_id"],
                },
            )
        ]

    async def redeploy_from_path(self, zip_file_path: str, env_file_path: str, site_id: str) -> list[types.TextContent]:
        """Redeploy a website to an existing Netlify site from a zip file path."""
        if not os.path.isabs(zip_file_path):
            raise ValueError("zip_file_path must be an absolute path")
        if not os.path.isabs(env_file_path):
            raise ValueError("env_file_path must be an absolute path")

        try:
            # Read zip file content
            with open(zip_file_path, 'rb') as f:
                zip_content = f.read()

            # Read .env file content as bytes
            with open(env_file_path, 'rb') as f:
                env_content = f.read()

            # Prepare form data
            form = aiohttp.FormData()
            form.add_field('zip_file',
                            zip_content,
                            filename='dist.zip',
                            content_type='application/zip')
            form.add_field('env_file',
                            env_content,
                            filename='.env',
                            content_type='text/plain')
            form.add_field('site_id', site_id)

            # Make POST request to redeployment endpoint
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.server_url}/redeploy-netlify',
                    headers={
                        "Authorization": f"Bearer {self.auth_token}"
                    },
                    data=form
                ) as response:
                    result = await response.text()
                    return [
                        types.TextContent(
                            type="text",
                            text=result
                        )
                    ]

        except FileNotFoundError as e:
            return [
                types.TextContent(
                    type="text",
                    text=str({"error": f"File not found: {str(e)}"})
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=str({"error": str(e)})
                )
            ]

    async def deploy_from_path(self, zip_file_path: str, env_file_path: str) -> list[types.TextContent]:
        """Deploy a website from a zip file path."""
        if not os.path.isabs(zip_file_path):
            raise ValueError("zip_file_path must be an absolute path")
        if not os.path.isabs(env_file_path):
            raise ValueError("env_file_path must be an absolute path")

        try:
            # Read zip file content
            with open(zip_file_path, 'rb') as f:
                zip_content = f.read()

            # Read .env file content as bytes
            with open(env_file_path, 'rb') as f:
                env_content = f.read()

            # Prepare form data
            form = aiohttp.FormData()
            form.add_field('zip_file',
                            zip_content,
                            filename='dist.zip',
                            content_type='application/zip')
            form.add_field('env_file',
                            env_content,
                            filename='.env',
                            content_type='text/plain')

            # Make POST request to deployment endpoint
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.server_url}/deploy-netlify',
                    headers={
                        "Authorization": f"Bearer {self.auth_token}"
                    },
                    data=form
                ) as response:
                    result = await response.text()
                    return [
                        types.TextContent(
                            type="text",
                            text=result
                        )
                    ]

        except FileNotFoundError as e:
            return [
                types.TextContent(
                    type="text",
                    text=str({"error": f"File not found: {str(e)}"})
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=str({"error": str(e)})
                )
            ]