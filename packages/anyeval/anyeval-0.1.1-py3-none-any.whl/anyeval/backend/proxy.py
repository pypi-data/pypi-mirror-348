import mimetypes
import os
from pathlib import Path
from urllib.parse import unquote, urlparse

import opendal
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

# Create a router
router = APIRouter(prefix="/api/proxy", tags=["proxy"])

# Cache for operator instances
operators: dict[str, opendal.Operator] = {}

# Get workspace root directory (assuming we're running from the project root)
WORKSPACE_ROOT = Path(os.getcwd()).absolute()

def get_operator(scheme: str, host: str | None = None) -> opendal.Operator:
    """Get or create an opendal Operator for the given scheme."""
    key = f"{scheme}://{host}" if host else scheme

    if key in operators:
        return operators[key]

    if scheme in {"fs", "file"}:
        # For filesystem storage - using default settings without root
        # This will use the OS filesystem directly, and we'll handle paths explicitly
        op = opendal.Operator("fs")
        operators[key] = op
        return op
    if scheme == "s3":
        # For S3 storage (requires credentials)
        if not host:
            host = os.environ.get("S3_ENDPOINT", "s3.amazonaws.com")

        op = opendal.Operator("s3", {
            "root": "/",
            "bucket": host,
            "endpoint": os.environ.get("S3_ENDPOINT", "https://s3.amazonaws.com"),
            "access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
            "secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
            "region": os.environ.get("AWS_REGION", "us-east-1"),
        })
        operators[key] = op
        return op
    # Add more storage backends as needed
    msg = f"Unsupported storage scheme: {scheme}"
    raise ValueError(msg)

def get_mime_type(path: str) -> str:
    """Get the MIME type for a file based on its extension."""
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or "application/octet-stream"

def get_path_from_url(url: str) -> tuple[str, str, str]:
    """Parse a URL and extract the scheme, host (if applicable), and path."""
    parsed = urlparse(url)
    scheme = parsed.scheme or "fs"
    path = parsed.path
    host = parsed.netloc

    # Handle special cases for fs:// protocol
    if scheme == "fs":
        # For fs:// URLs, we want absolute paths for security
        if host:
            if host.startswith("/"):
                # Absolute path from root - use as is
                path = f"{host}{path}"
            else:
                # Relative path - resolve against workspace
                path = os.path.join(WORKSPACE_ROOT, host, path.lstrip("/"))
            host = None
        else:
            # No host provided, ensure path is absolute
            if not path.startswith("/"):
                # Relative path - resolve against workspace
                path = os.path.join(WORKSPACE_ROOT, path)

    # Decode URL encoding
    path = unquote(path)

    return scheme, host, path

@router.get("/resource")
async def proxy_resource(url: str, request: Request):
    """Proxy a resource from any supported storage backend.

    Args:
        url: The URL to the resource, e.g., fs://path/to/file, s3://bucket/path/to/file

    """
    try:
        scheme, host, path = get_path_from_url(url)

        # For filesystem scheme, resolve to absolute path
        if scheme in {"fs", "file"}:
            # Path is already absolute by this point
            abs_path = path

            # Check if file exists directly using os.path
            if not os.path.exists(abs_path):
                raise HTTPException(status_code=404, detail=f"Resource not found: {url}, resolved path: {abs_path}")

            # Use FileResponse directly for filesystem files instead of OpenDAL
            # This is more direct and likely to work better with the local filesystem
            from fastapi.responses import FileResponse
            return FileResponse(
                abs_path,
                media_type=get_mime_type(abs_path),
                headers={
                    "Cache-Control": "max-age=86400",  # Cache for 24 hours
                    "Access-Control-Allow-Origin": "*",
                },
            )

        # For other schemes like S3, use OpenDAL
        op = get_operator(scheme, host)

        # Check if file exists
        if not await op.is_exist(path):
            raise HTTPException(status_code=404, detail=f"Resource not found: {url}, resolved path: {path}")

        # Get file stats for content type and size
        stat = await op.stat(path)
        size = stat.content_length()
        mime_type = get_mime_type(path)

        # Stream the file content
        async def content_iterator():
            # Read the file in chunks to avoid loading large files into memory
            with await op.reader(path) as reader:
                while chunk := await reader.read(8192):  # 8KB chunks
                    yield chunk

        return StreamingResponse(
            content_iterator(),
            media_type=mime_type,
            headers={
                "Content-Length": str(size),
                "Cache-Control": "max-age=86400",  # Cache for 24 hours
                "Access-Control-Allow-Origin": "*",
            },
        )

    except Exception as e:
        # More detailed error for debugging
        import traceback
        error_detail = f"Error: {e!s}\nURL: {url}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

def rewrite_resource_url(url: str | None, request: Request) -> str | None:
    """Rewrite resource URLs to go through the proxy.

    Args:
        url: The original URL (fs://, s3://, etc.)
        request: The current request for building the proxy URL

    Returns:
        The rewritten URL pointing to the proxy endpoint

    """
    if not url:
        return None

    # If already a HTTP URL, return as is
    if url.startswith(("http://", "https://")):
        return url

    # Build the proxy URL
    base_url = str(request.base_url).rstrip("/")
    return f"{base_url}/api/proxy/resource?url={url}"
