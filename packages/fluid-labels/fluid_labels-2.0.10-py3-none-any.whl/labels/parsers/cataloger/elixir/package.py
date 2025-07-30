import logging

from packageurl import PackageURL
from pydantic import BaseModel, ValidationError

from labels.model.file import Location
from labels.model.package import Language, Package, PackageType
from labels.utils.strings import format_exception

LOGGER = logging.getLogger(__name__)


class ElixirMixLockEntry(BaseModel):
    name: str
    version: str
    pkg_hash: str
    pkg_hash_ext: str


def new_package(entry: ElixirMixLockEntry, locations: Location) -> Package | None:
    name = entry.name
    version = entry.version

    if not name or not version:
        return None

    try:
        return Package(
            name=name,
            version=version,
            type=PackageType.HexPkg,
            locations=[locations],
            p_url=package_url(name, version),
            metadata=entry,
            language=Language.ELIXIR,
            licenses=[],
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types are incorrect.",
            extra={
                "extra": {
                    "exception": format_exception(str(ex)),
                    "location": locations.path(),
                },
            },
        )
        return None


def package_url(name: str, version: str) -> str:
    return PackageURL(  # type: ignore
        type="hex",
        namespace="",
        name=name,
        version=version,
        qualifiers=None,
        subpath="",
    ).to_string()
