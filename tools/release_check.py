"""Client release compatibility checks shared by tests and update clients."""

from .manifest import validate_manifest


def _version(value):
    parts = str(value).split(".")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise ValueError("version must use MAJOR.MINOR.PATCH")
    return tuple(int(part) for part in parts)


def check_release(manifest, *, platform, arch, current_version):
    """Return the update state for one client: current, update, or blocked."""
    validate_manifest(manifest)
    current = _version(current_version)
    candidates = [item for item in manifest["releases"] if item["platform"] == platform and item["arch"] == arch]
    if not candidates:
        return {"state": "current", "release": None}
    release = max(candidates, key=lambda item: _version(item["version"]))
    minimum = _version(release["minimumSupportedVersion"])
    latest = _version(release["version"])
    if current < minimum:
        state = "blocked"
    elif current < latest:
        state = "update"
    else:
        state = "current"
    return {"state": state, "release": release}
