import importlib.metadata

class VersionUtil:

    def get_version():
        for name in ["lib_version_team17", "lib_version"]:
            try:
                return importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError:
                continue
        return "unknown"