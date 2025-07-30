from setuptools import setup
import tomli

# Read dependencies from pyproject.toml
with open("pyproject.toml", "rb") as f:
    pyproject_data = tomli.load(f)

# Get dependencies from pyproject.toml

setup(
    name="aliyun-openapi-mcp-sdk",
    version="1.4.0",
    description="Aliyun Automatic MCP server generator for OpenAPI applications - converts OpenAPI endpoints to MCP tools for LLM integration",
    author="aliyun-openapi-mcp-sdk",
    author_email="aliyun-openapi-mcp-sdk@aliyun.com",
    packages=["aliyun-openapi-mcp-sdk"],
    python_requires=">=3.10",
    install_requires="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords=["openapi", "mcp", "llm", "claude", "ai", "tools", "api", "conversion", "fastapi", "flask", "django"],
    project_urls={
        "PyPI": "https://pypi.org/project/aliyun-openapi-mcp-sdk/"
    },
)
