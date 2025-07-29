"""Manage optional dependencies."""

import logging

log = logging.getLogger(__name__)

# pylint: disable=unused-import, import-outside-toplevel


def have_core() -> bool:  # pragma: no cover
    """Return True if fw-core-client is installed."""
    try:
        import fw_client  # noqa: F401

        HAVE_CORE = True
    except (ModuleNotFoundError, ImportError):  # pragma: no cover
        HAVE_CORE = False
        log.warning("Could not find fw-core-client, skipping Flywheel API calls.")
    return HAVE_CORE


def have_fw_gear() -> bool:  # pragma: no cover
    """Return True if flywheel-gear-toolkit is installed."""
    try:  # pragma: no cover
        from fw_gear import GearContext as GearToolkitContext  # noqa: F401

        HAVE_FW_GEAR = True  # pragma: no cover
    except (ModuleNotFoundError, ImportError):
        log.warning("Could not find flywheel-gear-toolkit.")
        HAVE_FW_GEAR = True
    return HAVE_FW_GEAR
