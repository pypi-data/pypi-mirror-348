"""Adapter for Flywheel file objects."""

from __future__ import annotations

import logging
import typing as t

from dotty_dict import Dotty

from .. import __version__
from .base import Adapter
from .deps import have_core, have_fw_gear
from .utils import FileInput

log = logging.getLogger(__name__)

HAVE_CORE = have_core()
HAVE_FW_GEAR = have_fw_gear()

if HAVE_CORE:
    from fw_client import ClientError, FWClient, ServerError

if HAVE_FW_GEAR:
    # pylint: disable=unused-import
    from fw_gear import GearContext as GearToolkitContext  # noqa: F401
    # pylint: enable=unused-import

if t.TYPE_CHECKING:  # pragma: no cover
    from fw_client import ClientError, FWClient, ServerError
    from fw_gear import GearContext as GearToolkitContext  # noqa: F401

HIERARCHY_ORDER = ["file", "acquisition", "session", "subject", "project"]
META_EXCLUDE = ["file_id", "type", "version", "origin", "size", "name"]
PARENT_INCLUDE = [
    # General values
    "label",
    "info",
    "uid",
    # Session values
    "age",
    "weight",
    # Subject values
    "sex",
    "cohort",
    "mlset",
    "ethnicity",
    "species",
    "strain",
    "code",
    "firstname",
    "lastname",
]


def get_hierarchy(i_dict: t.Dict[str, t.Any], fw: "FWClient", file: FileInput) -> None:
    """Get hierarchy information."""
    parent_ref = file.hierarchy
    parent = fw.get(f"/api/{parent_ref.type}s/{parent_ref.id}")
    parents_dict = parent["parents"]
    parent = {k: v for k, v in parent.items() if k in PARENT_INCLUDE}
    i_dict[parent_ref.type] = parent
    log.info(f"Running at {parent_ref.type} level")
    level = HIERARCHY_ORDER.index(parent_ref.type) + 1
    log.info(f"Pulling parent levels: {', '.join(HIERARCHY_ORDER[level:])}")
    orig_header = fw.headers["X-Accept-Feature"]
    fw.headers["X-Accept-Feature"] = "Safe-Redirect,Slim-Containers"
    for parent_type in HIERARCHY_ORDER[level:]:
        if parent_type in parents_dict:
            try:
                parent = fw.get(f"/api/{parent_type}s/{parents_dict[parent_type]}")
                parent = {k: v for k, v in parent.items() if k in PARENT_INCLUDE}
                log.info(f"Pulled {parent_type}, id: {parents_dict[parent_type]}")
                i_dict[parent_type] = parent
            except (ClientError, ServerError) as err:
                log.error(err)
    fw.headers["X-Accept-Feature"] = orig_header


class FWAdapter(Adapter):
    """Adapter for Flywheel objects.

    `preprocess`: Pull hierarchy information.
    `postprocess`: Generate .metadata.json
    """

    def __init__(
        self,
        file: t.Dict[str, t.Any],
        gear_context: "GearToolkitContext",
        name: str = "",
        version: str = "",
    ) -> None:
        """Initialize file and information to pull from API."""
        self.fw: t.Optional["FWClient"]
        f_input = FileInput(**file)
        super().__init__(f_input)
        if not (HAVE_FW_GEAR and gear_context):
            raise ValueError("Need `fw_gear` to use this adapter.")
        self.fw_gear = gear_context
        if HAVE_CORE:
            try:
                api_key = gear_context.config.inputs.get("api-key").get("key")
                self.fw = FWClient(
                    api_key=api_key,
                    client_name=(name or "fw-classification"),
                    client_version=(version or __version__),
                )
            except (KeyError, AttributeError):
                log.warning("Could not find api-key.")
                self.fw = None
        else:
            self.fw = None

    def preprocess(self) -> t.Dict[str, t.Any]:
        """Populate hierarchy values."""
        i_dict = {
            "file": {
                "name": self.file.location.name,
                **self.file.object.dict(),
            }
        }
        if HAVE_CORE and self.fw:
            get_hierarchy(i_dict, self.fw, self.file)
        return i_dict

    def postprocess(self, res: bool, out: Dotty) -> bool:
        """Populate metadata for input file and parent container(s)."""
        if res:
            log.info("Generating .metadata.json from classification values.")
            metadata = out.to_dict()
            for key in HIERARCHY_ORDER[1:]:
                if key in metadata:
                    self.fw_gear.metadata.update_container(key, **metadata[key])
            for key in META_EXCLUDE:
                metadata["file"].pop(key, None)
            log.debug(f"Updating file metadata: {self.file.dict()}")
            log.debug(f"Metadata: {metadata['file']}")
            file_info = self.file.dict()
            self.fw_gear.metadata.update_file_metadata(
                file_=file_info,
                container_type=file_info.get("hierarchy").get("type"),
                **metadata["file"],
            )
        return res
