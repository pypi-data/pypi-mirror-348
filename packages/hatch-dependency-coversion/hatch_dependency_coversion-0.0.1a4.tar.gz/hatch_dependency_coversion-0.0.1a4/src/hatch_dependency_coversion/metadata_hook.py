# SPDX-FileCopyrightText: 2024-present Opentrons Engineering <engineering@opentrons.com>
#
# SPDX-License-Identifier: Apache-2.0

"""A metadata hook for hatchling that can force dependencies to be coversioned."""
from __future__ import annotations
import inspect
from typing import Any

from packaging.requirements import Requirement, SpecifierSet

from hatchling.metadata.plugin.interface import MetadataHookInterface
from hatch_dependency_coversion.const import PLUGIN_NAME as _PLUGIN_NAME


class DependencyCoversionMetadataHook(MetadataHookInterface):
    PLUGIN_NAME = _PLUGIN_NAME
    root: str
    config: dict

    def _maybe_update_dep(
        self, depspec: str, version: str, which_dependencies: list[str]
    ) -> str:
        requirement = Requirement(depspec)
        if requirement.name not in which_dependencies:
            return depspec
        requirement.specifier = SpecifierSet(f"=={version}")
        return str(requirement)

    def _update_dependency_versions(
        self,
        dependencies_metadata: list[str],
        version: str,
        which_dependencies: list[str],
    ) -> list[str]:
        """Do the actual dependency update"""
        return [
            self._maybe_update_dep(depspec, version, which_dependencies)
            for depspec in dependencies_metadata
        ]

    def _update_optional_dependency_versions(
        self,
        optional_dependencies_metadata: dict[str, list[str]],
        version: str,
        which_dependencies: list[str],
    ) -> dict[str, list[str]]:
        """Do the actual optional dependency update"""
        return {
            extra: [
                self._maybe_update_dep(depspec, version, which_dependencies)
                for depspec in optional_dep_list
            ]
            for extra, optional_dep_list in optional_dependencies_metadata.items()
        }

    def update(self, metadata: dict[str, Any]) -> None:
        """Update metadata for coversioning."""
        # this is from https://github.com/flying-sheep/hatch-docstring-description/blob/main/src/hatch_docstring_description/read_description.py
        # and would prevent surprise recursions, and if that author is worried about it then so am I
        if ("update", __file__) in (
            (frame.function, frame.filename) for frame in inspect.stack()[1:]
        ):
            return
        if "override-versions-of" not in self.config:
            return
        if not isinstance(self.config["override-versions-of"], list):
            raise RuntimeError(
                "tool.hatch.metadata.hooks.dependency-coversion.override-versions-of must be an array of strings"
            )
        override_of: list[str] = self.config["override-versions-of"]
        if "dependencies" in metadata:
            metadata["dependencies"] = self._update_dependency_versions(
                metadata.get("dependencies", []), metadata["version"], override_of
            )
        if "optional-dependencies" in metadata:
            metadata[
                "optional-dependencies"
            ] = self._update_optional_dependency_versions(
                metadata.get("optional-dependencies", {}),
                metadata["version"],
                override_of,
            )

    def get_known_classifiers(self) -> list[str]:
        """Dummy function that is part of the hook interface."""
        return []
