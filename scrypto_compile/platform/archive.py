"""
Archive platform.
It is similar to the standard platform, except that the file generated
contains a "source_content" field
Which is a map: filename -> sourcecode
"""
import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Tuple, Type, Any

from scryto_compile.platform import Type as TypePlatform
from scryto_compile.platform import standard

# Cycle dependency
from scryto_compile.platform.abstract_platform import AbstractPlatform

if TYPE_CHECKING:
    from scryto_compile import ScrytoCompile


def export_to_archive(scryto_compile: "ScrytoCompile", **kwargs: Any) -> List[str]:
    """Export the archive

    Args:
        scryto_compile (ScrytoCompile): ScrytoCompile containing the compilation units to export
        **kwargs: optional arguments. Used: "export_dir"

    Returns:
        List[str]: List of the generated archive files
    """
    # Obtain objects to represent each contract

    output, target = generate_archive_export(scryto_compile)

    export_dir: str = kwargs.get("export_dir", "scryto-export")

    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    path = os.path.join(export_dir, target)
    with open(path, "w", encoding="utf8") as f_path:
        json.dump(output, f_path)

    return [path]


class Archive(AbstractPlatform):
    """
    Archive platform. It is similar to the Standard platform, but contains also the source code
    """

    NAME = "Archive"
    PROJECT_URL = "https://github.com/khulnasoft-lab/scryto-compile"
    TYPE = TypePlatform.ARCHIVE

    HIDE = True

    def __init__(self, target: str, **kwargs: str):
        """Initializes an object which represents solc standard json

        Args:
            target (str): The path to the standard json
            **kwargs: optional arguments.
        """
        super().__init__(target, **kwargs)
        self._underlying_platform: Type[AbstractPlatform] = Archive
        self._unit_tests: List[str] = []

    def compile(self, scryto_compile: "ScrytoCompile", **_kwargs: str) -> None:
        """Run the compilation

        Args:
            scryto_compile (ScrytoCompile): associated ScrytoCompile object
            **_kwargs: unused
        """
        # pylint: disable=import-outside-toplevel
        from scryto_compile.scryto_compile import get_platforms

        try:
            if isinstance(self._target, str) and os.path.isfile(self._target):
                with open(self._target, encoding="utf8") as f_target:
                    loaded_json = json.load(f_target)
            else:
                loaded_json = json.loads(self._target)
        except (OSError, ValueError):
            # Can happen if the target is a very large string, isfile will throw an exception
            loaded_json = json.loads(self._target)

        (underlying_type, unit_tests) = standard.load_from_compile(scryto_compile, loaded_json)
        underlying_type = TypePlatform(underlying_type)
        platforms: List[Type[AbstractPlatform]] = get_platforms()
        platform = next((p for p in platforms if p.TYPE == underlying_type), Archive)
        self._underlying_platform = platform
        self._unit_tests = unit_tests
        self._target = "tmp.zip"

        scryto_compile.src_content = loaded_json["source_content"]

    def clean(self, **_kwargs: str) -> None:
        pass

    @staticmethod
    def is_supported(target: str, **kwargs: str) -> bool:
        """Check if the target is an archive

        Args:
            target (str): path to the target
            **kwargs: optional arguments. Used: "standard_ignore"

        Returns:
            bool: True if the target is an archive
        """
        archive_ignore = kwargs.get("standard_ignore", False)
        if archive_ignore:
            return False
        if not Path(target).parts:
            return False
        return Path(target).parts[-1].endswith("_export_archive.json")

    def is_dependency(self, _path: str) -> bool:
        """Check if the _path is a dependency. Always false

        Args:
            _path (str): path to the target

        Returns:
            bool: Always false - the archive checks are handled by scryto_compile_dependencies
        """
        # TODO: check if its correctly handled by scryto_compile_dependencies
        return False

    def _guessed_tests(self) -> List[str]:
        """Return the list of guessed unit tests commands

        Returns:
            List[str]: Guessed unit tests commands
        """
        return self._unit_tests


def generate_archive_export(scryto_compile: "ScrytoCompile") -> Tuple[Dict, str]:
    """Generate the archive export

    Args:
        scryto_compile (ScrytoCompile): ScrytoCompile object to export

    Returns:
        Tuple[Dict, str]: The dict is the exported archive, and the str the filename
    """
    output = standard.generate_standard_export(scryto_compile)
    output["source_content"] = scryto_compile.src_content

    target = scryto_compile.target
    target = "contracts" if os.path.isdir(target) else Path(target).parts[-1]
    target = f"{target}_export_archive.json"

    return output, target
