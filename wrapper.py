# wrapper.py — neutralizes `@mcp.on_start` usage for older FastMCP versions
# and re-exports `mcp` for FastMCP Cloud Entrypoint.
# Use Entrypoint: wrapper.py:mcp

from wavespeed_mcp.server import mcp as _mcp

# If FastMCP doesn't have an `on_start` attribute, provide a no-op decorator
if not hasattr(_mcp, "on_start"):
    def _noop_decorator(func):
        # return the function unchanged
        return func
    # attach the no-op to the FastMCP instance
    try:
        setattr(_mcp, "on_start", _noop_decorator)
    except Exception:
        pass

# Re-export for the hosting platform
mcp = _mcp
