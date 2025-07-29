from pathlib import Path, PurePath
from pymsbuild import File, SourceFile

__all__ = ["AppxManifest", "AppInstaller", "ResourcesXml"]

TARGETS = Path(__file__).absolute().parent / "targets"


class AppxManifest(File):
    options = {
        "IncludeInSdist": True,
        "IncludeInLayout": True,
        "IncludeInWheel": True,
    }


class AppInstaller(File):
    options = {
        "IncludeInSdist": True,
        "IncludeInLayout": True,
        "IncludeInWheel": True,
    }

    def _match(self, key):
        if key.casefold() == "$AppInstaller".casefold():
            return True
        return PurePath(self.name).match(key)


class ResourcesXml(SourceFile):
    def _match(self, key):
        if key.casefold() == "$ResourcesXml".casefold():
            return True
        return PurePath(self.name).match(key)
