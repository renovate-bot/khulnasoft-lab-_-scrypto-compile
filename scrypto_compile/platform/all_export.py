"""
Module containing all the supported export functions
"""
from scryto_compile.platform.archive import export_to_archive
from scryto_compile.platform.solc import export_to_solc
from scryto_compile.platform.standard import export_to_standard
from scryto_compile.platform.truffle import export_to_truffle

PLATFORMS_EXPORT = {
    "standard": export_to_standard,
    "scryto-compile": export_to_standard,
    "solc": export_to_solc,
    "truffle": export_to_truffle,
    "archive": export_to_archive,
}
