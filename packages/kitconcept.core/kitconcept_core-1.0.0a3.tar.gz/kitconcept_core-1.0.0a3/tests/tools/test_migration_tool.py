from kitconcept.core import __version__
from kitconcept.core.tools.migration import MigrationTool

import pytest


PROFILE_VERSION = "1001"


class TestMigrationTool:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.tool: MigrationTool = portal.portal_migration

    def test_is_instance(self):
        """Test portal_migration uses our class."""
        assert isinstance(self.tool, MigrationTool)

    def test_getSoftwareVersion(self):
        """Test portal_migration.getSoftwareVersion."""

        assert self.tool.getSoftwareVersion() == __version__

    def test_getFileSystemVersion(self):
        """Test portal_migration.getFileSystemVersion."""

        assert self.tool.getFileSystemVersion() == PROFILE_VERSION

    def test_getInstanceVersion(self):
        """Test portal_migration.getFileSystemVersion."""

        assert self.tool.getInstanceVersion() == PROFILE_VERSION

    def test_listUpgrades(self):
        """Test portal_migration.listUpgrades."""
        assert isinstance(self.tool.list_steps(), list)

    def test_list_steps(self):
        """Test portal_migration.list_steps."""
        assert isinstance(self.tool.list_steps(), list)


class TestMigrationToolVersions:
    @pytest.fixture(autouse=True)
    def _setup(self, portal_class):
        self.tool: MigrationTool = portal_class.portal_migration

    @pytest.mark.parametrize(
        "key,expected",
        [
            [
                "core",
                {
                    "name": "kitconcept.core",
                    "package_version": __version__,
                    "instance_version": "1001",
                    "fs_version": "1001",
                },
            ],
            ["Zope", "5.13"],
            ["CMFPlone", "6.1.1"],
        ],
    )
    def test_coreVersions(self, key: str, expected: str):
        """Test portal_migration.coreVersions."""
        info = self.tool.coreVersions()
        assert isinstance(info, dict)
        assert info[key] == expected

    @pytest.mark.parametrize(
        "key",
        [
            "CMF",
            "CMFPlone",
            "Debug mode",
            "PIL",
            "Platform",
            "Plone File System",
            "Plone Instance",
            "core",
            "Python",
            "Zope",
        ],
    )
    def test_coreVersions_keys(self, key: str):
        """Test portal_migration.coreVersions."""
        info = self.tool.coreVersions()
        assert key in info
