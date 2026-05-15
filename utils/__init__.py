"""Compatibility package.

The codebase historically imported helper modules as `utils.*` assuming the
`backend/` folder was on `PYTHONPATH`. When running as a proper package
(`python -m backend...`) those imports fail.

This shim keeps existing imports working by re-exporting from `backend.utils`.
"""
