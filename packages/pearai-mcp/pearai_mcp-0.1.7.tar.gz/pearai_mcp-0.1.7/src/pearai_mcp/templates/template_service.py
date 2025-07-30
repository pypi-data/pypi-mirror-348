#!/usr/bin/env python3
import io
import os
import shutil
import zipfile
from pathlib import Path
from typing import List, Dict
import requests
import mcp.types as types
from pearai_mcp.constants import SERVER_URL

class TemplateService:
    def __init__(self, server_url: str = None, auth_token: str = None):
        """Initialize the template service.

        Args:
            server_url: Optional server URL override
            auth_token: Authentication token for API requests
        """
        self.server_url = server_url or SERVER_URL
        self.auth_token = auth_token
        self.headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

    def get_tools(self) -> list[types.Tool]:
        """List available template tools."""
        return [
            types.Tool(
                name="template-feedback",
                description="Record feedback about template usage for a project",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_summary": {
                            "type": "string",
                            "description": "Brief summary of the kind of project being made"
                        },
                        "template_used": {
                            "type": "string",
                            "description": "Name of the template used, or 'None' if no template was used"
                        }
                    },
                    "required": ["project_summary", "template_used"]
                }
            ),
            types.Tool(
                name="list-templates",
                description="Returns a list of available templates with metadata",
                inputSchema={
                    "type": "object",
                    "properties": {},
                }
            ),
            types.Tool(
                name="download-template",
                description="Download a template by URL",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "template_url": {
                            "type": "string",
                            "description": "URL of the template to download"
                        }
                    },
                    "required": ["template_url"]
                }
            ),
            types.Tool(
                name="create-new-project",
                description="Create a new project from a template",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_name": {
                            "type": "string",
                            "description": "Name of the new project"
                        },
                        "template_url": {
                            "type": "string",
                            "description": "URL of the template to download (provided by AI agent)"
                        },
                        "base_dir": {
                            "type": "string",
                            "description": "Base directory to create the project in (defaults to current directory)"
                        }
                    },
                    "required": ["project_name", "template_url"]
                }
            )
        ]

    def template_feedback(self, project_summary: str, template_used: str) -> list[types.TextContent]:
        """Record feedback about template usage.

        Args:
            project_summary: Brief description of the project being created
            template_used: Name of the template used, or "None" if no template was used

        Returns:
            list[types.TextContent]: Status message
        """
        try:
            response = requests.post(
                f"{self.server_url}/templates/template_feedback",
                headers=self.headers,
                json={
                    "project_summary": project_summary,
                    "template_used": template_used
                }
            )

            if response.status_code != 200:
                return [
                    types.TextContent(
                        type="text",
                        text=str({
                            "error": f"Failed to record template feedback: {response.status_code}",
                            "type": "RequestError"
                        })
                    )
                ]

            return [
                types.TextContent(
                    type="text",
                    text=str({
                        "message": "Template feedback recorded successfully",
                        "status": "success"
                    })
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=str({
                        "error": str(e),
                        "type": e.__class__.__name__
                    })
                )
            ]

    def list_templates(self) -> list[types.TextContent]:
        """Return list of available templates with their metadata."""
        response = requests.get(
            f"{self.server_url}/templates/get_templates",
            headers=self.headers
        )
        if response.status_code != 200:
            return [
                types.TextContent(
                    type="text",
                    text=str({"error": "Failed to fetch templates"})
                )
            ]
        templates = response.json()
        return [
            types.TextContent(
                type="text",
                text=str(templates)
            )
        ]
    def fetch_template(self, template_url: str) -> bytes:
        """Fetch a specific template.

        Args:
            template_url: URL of the template to download

        Returns:
            bytes: The template zip file data

        Raises:
            ValueError: If template download fails
        """
        response = requests.get(template_url, headers=self.headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to download template: {response.status_code}")
        return response.content

    def unzip_template(self, zip_data: bytes, destination_path: str) -> None:
        """Unzip template data to destination path."""
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
            zf.extractall(destination_path)

    def create_new_project(self, project_name: str, template_url: str, base_dir: str = None) -> list[types.TextContent]:
        """Create a new project from a template.

        Args:
            project_name: Name of the new project
            template_url: URL of the template to download (provided by AI agent)
            base_dir: Base directory to create the project in (defaults to current directory)

        Returns:
            list[types.TextContent]: Status message or error
        """
        from pathlib import Path
        import os

        try:
            # Validate project name
            if not project_name.isalnum() and not all(c in '-_' for c in project_name if not c.isalnum()):
                raise ValueError("Project name must contain only letters, numbers, hyphens or underscores")

            # Setup paths
            base_path = Path(base_dir if base_dir else os.getcwd())
            destination_path = (base_path / project_name).resolve()
            if destination_path.exists():
                raise ValueError(f"Directory '{project_name}' already exists")

            # Fetch template
            template_data = self.fetch_template(template_url)

            try:
                # Create project directory and extract template
                destination_path.mkdir(parents=True)
                self.unzip_template(template_data, str(destination_path))

                # Initialize git repository if template contains .git directory
                git_dir = destination_path / '.git'
                if git_dir.exists():
                    os.system(f'cd "{destination_path}" && git init')

                return [
                    types.TextContent(
                        type="text",
                        text=str({
                            "message": f"Project '{project_name}' created successfully from template at '{template_url}'",
                            "path": str(destination_path)
                        })
                    )
                ]

            except Exception as e:
                # Cleanup on failure
                if destination_path.exists():
                    import shutil
                    shutil.rmtree(destination_path)
                raise

        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=str({
                        "error": str(e),
                        "type": e.__class__.__name__
                    })
                )
            ]