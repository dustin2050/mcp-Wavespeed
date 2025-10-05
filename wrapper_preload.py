# wrapper_preload.py — shim to support codebases that use `@mcp.on_start`
# with older FastMCP versions that don't implement that attribute.
#
# Use Entrypoint in FastMCP Cloud: wrapper_preload.py:mcp

# 1) Patch FastMCP *class* to provide a no-op `on_start` decorator
try:
    from fastmcp import FastMCP
    def _noop_on_start(*args, **kwargs):
        def _decorator(fn):
            return fn
        return _decorator
    if not hasattr(FastMCP, "on_start"):
        setattr(FastMCP, "on_start", _noop_on_start)
except Exception:
    # If fastmcp isn't importable yet, we'll just proceed; server import will fail anyway.
    pass

# 2) Now import your actual server module — decorators are evaluated now,
#    and will find the patched attribute on the class.
from wavespeed_mcp.server import mcp as _mcp

# 3) Re-export for the hosting platform
mcp = _mcp
